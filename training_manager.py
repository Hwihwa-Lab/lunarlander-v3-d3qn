"""
Training Manager for DQN LunarLander.
Manages asynchronous training, demonstration, manual control, multi-history tracking, and WebSocket streaming.
"""

import asyncio
import os
import time
import threading
import traceback
from typing import Dict, Any, List, Optional
import numpy as np
import gymnasium as gym

from dqn_agent import DQNAgent, shape_stylish_reward

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
BEST_MODEL_PATH = os.path.join(MODEL_DIR, "best_model.pth")
LATEST_MODEL_PATH = os.path.join(MODEL_DIR, "latest_model.pth")


class TrainingManager:
    def __init__(self):
        self.agent = DQNAgent(state_size=8, action_size=4, seed=42)
        
        # Load existing best checkpoint if available
        if os.path.exists(BEST_MODEL_PATH):
            self.agent.load(BEST_MODEL_PATH)
            print(f"[TrainingManager] Loaded existing model from {BEST_MODEL_PATH}")

        # Training Hyperparameters
        self.max_episodes = 1000
        self.eps_start = 1.0
        self.eps_end = 0.05
        self.eps_decay = 0.99626
        self.epsilon = self.eps_start

        # State & Control Flags
        self.is_training = False
        self.is_paused = False
        self.mode = "training"  # "training", "turbo", "showcase", "manual", "idle"
        self.speed_multiplier = 1.0  # 1.0, 2.0, 5.0, -1 (turbo)
        
        # Metrics & History
        self.current_episode = 0
        self.total_steps = 0
        self.current_score = 0.0
        self.rewards_history: List[float] = []
        self.moving_avg_history: List[float] = []
        self.epsilon_history: List[float] = []
        self.loss_history: List[float] = []
        self.best_reward = 0.0
        self.success_count = 0
        self.consecutive_success = 0
        
        # Real-time frame data for UI
        self.manual_action = 0

        # Event Loop & Queues for WebSocket
        self.subscribers: set = set()
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self._worker_thread: Optional[threading.Thread] = None
        self._stop_requested = False

    def set_event_loop(self, loop: asyncio.AbstractEventLoop):
        self.loop = loop

    def add_subscriber(self, ws):
        self.subscribers.add(ws)

    def remove_subscriber(self, ws):
        self.subscribers.discard(ws)

    def broadcast_sync(self, message: dict):
        """Broadcast message to all connected WebSockets safely from thread."""
        if not self.loop or not self.subscribers:
            return

        async def _send():
            disconnected = []
            for ws in list(self.subscribers):
                try:
                    await ws.send_json(message)
                except Exception:
                    disconnected.append(ws)
            for ws in disconnected:
                self.subscribers.discard(ws)

        try:
            if not self.loop.is_closed():
                asyncio.run_coroutine_threadsafe(_send(), self.loop)
        except Exception as e:
            pass

    def start_training(self):
        print(f"[TrainingManager] start_training called. Thread alive: {self._worker_thread.is_alive() if self._worker_thread else False}")
        self.is_training = True
        self.is_paused = False
        self._stop_requested = False
        self.mode = "training"

        if self._worker_thread is None or not self._worker_thread.is_alive():
            self._worker_thread = threading.Thread(target=self._training_loop, daemon=True)
            self._worker_thread.start()
            print("[TrainingManager] Worker thread successfully started.")

    def pause_training(self):
        print("[TrainingManager] Training paused.")
        self.is_paused = True

    def resume_training(self):
        print("[TrainingManager] Training resumed.")
        self.is_paused = False

    def stop_training(self):
        print("[TrainingManager] Training stopped.")
        self._stop_requested = True
        self.is_training = False
        self.is_paused = False

    def reset_training(self):
        print("[TrainingManager] Training reset.")
        self.stop_training()
        time.sleep(0.1)
        self.agent = DQNAgent(state_size=8, action_size=4, seed=42)
        self.current_episode = 0
        self.total_steps = 0
        self.current_score = 0.0
        self.epsilon = self.eps_start
        self.rewards_history.clear()
        self.moving_avg_history.clear()
        self.epsilon_history.clear()
        self.loss_history.clear()
        self.best_reward = 0.0
        self.success_count = 0
        self.consecutive_success = 0
        
        self.broadcast_sync({
            "type": "reset_complete",
            "stats": self.get_summary_stats()
        })

    def set_speed(self, speed: float):
        print(f"[TrainingManager] Speed set to: {speed}")
        self.speed_multiplier = speed

    def set_mode(self, mode: str):
        print(f"[TrainingManager] Mode changed to: {mode}")
        self.mode = mode
        if mode == "turbo":
            self.speed_multiplier = -1
            self.start_training()
        elif mode == "training":
            if self.speed_multiplier <= 0:
                self.speed_multiplier = 1.0
            self.start_training()
        elif mode == "showcase":
            self.start_showcase()
        elif mode == "manual":
            self.start_manual_mode()

    def set_manual_action(self, action: int):
        self.manual_action = max(0, min(3, action))

    def load_best_model(self) -> bool:
        success = self.agent.load(BEST_MODEL_PATH)
        if success:
            print(f"[TrainingManager] Loaded best model successfully.")
            self.broadcast_sync({
                "type": "model_loaded",
                "status": "success",
                "stats": self.get_summary_stats()
            })
        return success

    def start_showcase(self):
        """Run single demo episode with greedy policy (Epsilon = 0.0)."""
        if self._worker_thread and self._worker_thread.is_alive() and self.is_training:
            self.pause_training()

        self.mode = "showcase"
        threading.Thread(target=self._run_showcase_episode, daemon=True).start()

    def start_manual_mode(self):
        """Run interactive episode controlled by human."""
        if self._worker_thread and self._worker_thread.is_alive() and self.is_training:
            self.pause_training()

        self.mode = "manual"
        threading.Thread(target=self._run_manual_episode, daemon=True).start()

    def get_summary_stats(self) -> Dict[str, Any]:
        moving_avg = self.moving_avg_history[-1] if self.moving_avg_history else 0.0
        success_rate = (self.success_count / max(1, self.current_episode)) * 100
        latest_loss = self.loss_history[-1] if self.loss_history else self.agent.last_loss
        return {
            "current_episode": self.current_episode,
            "max_episodes": self.max_episodes,
            "total_steps": self.total_steps,
            "current_score": round(self.current_score, 1),
            "epsilon": self.epsilon,
            "best_reward": round(self.best_reward, 1),
            "moving_avg": round(moving_avg, 1),
            "success_count": self.success_count,
            "success_rate": round(success_rate, 1),
            "mode": self.mode,
            "is_training": self.is_training,
            "is_paused": self.is_paused,
            "speed": self.speed_multiplier,
            "loss": round(latest_loss, 3),
        }

    def _training_loop(self):
        """Core training loop running for 1000 episodes."""
        print("[TrainingManager] Entered _training_loop.")
        try:
            env = gym.make("LunarLander-v3")
            
            while self.current_episode < self.max_episodes and not self._stop_requested:
                if self.is_paused:
                    time.sleep(0.08)
                    continue

                self.current_episode += 1
                state, _ = env.reset()
                episode_reward = 0.0
                step_count = 0
                done = False
                
                # Smoothly decay epsilon: from 100% (1.0) down to 5% (0.05)
                self.epsilon = max(self.eps_end, self.epsilon * self.eps_decay)
                self.epsilon_history.append(self.epsilon)

                while not done and not self._stop_requested:
                    if self.is_paused:
                        time.sleep(0.05)
                        continue

                    # Action selection
                    action, q_values = self.agent.act(state, self.epsilon)
                    
                    # Step environment
                    next_state, raw_reward, terminated, truncated, _ = env.step(action)
                    done = terminated or truncated
                    
                    # Stylish reward shaping
                    shaped_reward = shape_stylish_reward(next_state, raw_reward, action, terminated, truncated)
                    
                    # Agent step (Memory + Learn)
                    self.agent.step(state, action, shaped_reward, next_state, done)
                    
                    state = next_state
                    episode_reward += raw_reward
                    self.current_score = episode_reward
                    step_count += 1
                    self.total_steps += 1

                    pitch_angle_deg = round(float(state[4] * (180 / np.pi)), 2)

                    # Stream telemetry frame
                    telemetry = {
                        "type": "telemetry",
                        "mode": self.mode,
                        "episode": self.current_episode,
                        "step": step_count,
                        "x": float(state[0]),
                        "y": float(state[1]),
                        "vx": float(state[2]),
                        "vy": float(state[3]),
                        "angle": float(state[4]),
                        "pitch_angle": pitch_angle_deg,
                        "angular_vel": float(state[5]),
                        "left_leg": bool(state[6] > 0.5),
                        "right_leg": bool(state[7] > 0.5),
                        "action": int(action),
                        "current_score": round(float(self.current_score), 1),
                        "raw_reward": round(float(raw_reward), 2),
                        "shaped_reward": round(float(shaped_reward), 2),
                        "q_values": [round(float(q), 2) for q in q_values],
                        "epsilon": round(float(self.epsilon), 4),
                        "loss": round(float(self.agent.last_loss), 3),
                        "done": done,
                        "success": bool(raw_reward >= 100 and terminated),
                        "status_text": "IN FLIGHT" if not done else ("LANDED SUCCESS" if (raw_reward >= 100 and terminated) else "CRASHED"),
                    }
                    
                    # Frame throttling based on speed multiplier
                    if self.speed_multiplier > 0:
                        self.broadcast_sync(telemetry)
                        delay = max(0.002, 0.025 / self.speed_multiplier)
                        time.sleep(delay)
                    else:
                        # Turbo mode: broadcast periodically
                        if step_count % 4 == 0 or done:
                            self.broadcast_sync(telemetry)

                # Record episode metrics
                self.rewards_history.append(episode_reward)
                recent_100 = self.rewards_history[-100:]
                moving_avg = float(np.mean(recent_100))
                self.moving_avg_history.append(moving_avg)
                self.loss_history.append(self.agent.last_loss)

                # Landing success check
                is_success = episode_reward >= 150 or (raw_reward >= 100 and terminated)
                if is_success:
                    self.success_count += 1
                    self.consecutive_success += 1
                else:
                    self.consecutive_success = 0

                # Save best model
                if episode_reward > self.best_reward:
                    self.best_reward = episode_reward
                    self.agent.save(BEST_MODEL_PATH)

                # Periodic latest save
                if self.current_episode % 50 == 0:
                    self.agent.save(LATEST_MODEL_PATH)

                # Broadcast episode summary
                self.broadcast_sync({
                    "type": "episode_summary",
                    "episode": self.current_episode,
                    "reward": round(episode_reward, 1),
                    "moving_avg": round(moving_avg, 1),
                    "epsilon": round(self.epsilon * 100, 1),
                    "loss": round(self.agent.last_loss, 3),
                    "steps": step_count,
                    "success": is_success,
                    "stats": self.get_summary_stats()
                })

            env.close()
        except Exception as err:
            print(f"[TrainingManager] Error in _training_loop: {err}")
            traceback.print_exc()
        finally:
            self.is_training = False
            self.agent.save(LATEST_MODEL_PATH)
            
            self.broadcast_sync({
                "type": "training_finished",
                "stats": self.get_summary_stats()
            })

    def _run_showcase_episode(self):
        """Showcases the trained model with 0% epsilon."""
        print("[TrainingManager] Starting showcase episode.")
        try:
            env = gym.make("LunarLander-v3")
            state, _ = env.reset()
            done = False
            step_count = 0
            total_reward = 0.0

            while not done and self.mode == "showcase":
                action, q_values = self.agent.act(state, eps=0.0)
                next_state, reward, terminated, truncated, _ = env.step(action)
                done = terminated or truncated
                state = next_state
                total_reward += reward
                self.current_score = total_reward
                step_count += 1

                pitch_angle_deg = round(float(state[4] * (180 / np.pi)), 2)

                self.broadcast_sync({
                    "type": "telemetry",
                    "mode": "showcase",
                    "episode": self.current_episode,
                    "step": step_count,
                    "x": float(state[0]),
                    "y": float(state[1]),
                    "vx": float(state[2]),
                    "vy": float(state[3]),
                    "angle": float(state[4]),
                    "pitch_angle": pitch_angle_deg,
                    "angular_vel": float(state[5]),
                    "left_leg": bool(state[6] > 0.5),
                    "right_leg": bool(state[7] > 0.5),
                    "action": int(action),
                    "current_score": round(float(self.current_score), 1),
                    "raw_reward": round(float(reward), 2),
                    "shaped_reward": round(float(reward), 2),
                    "q_values": [round(float(q), 2) for q in q_values],
                    "epsilon": 0.0,
                    "loss": 0.0,
                    "done": done,
                    "success": bool(reward >= 100 and terminated),
                    "status_text": "IN FLIGHT" if not done else ("LANDED SUCCESS" if (reward >= 100 and terminated) else "CRASHED"),
                })
                time.sleep(0.025)

            env.close()
            self.broadcast_sync({
                "type": "showcase_complete",
                "total_reward": round(total_reward, 1),
                "success": bool(total_reward >= 150)
            })
        except Exception as err:
            print(f"[TrainingManager] Error in showcase: {err}")
            traceback.print_exc()
        finally:
            self.mode = "training" if self.is_training else "idle"

    def _run_manual_episode(self):
        """Runs human-controlled flight mode."""
        print("[TrainingManager] Starting manual control episode.")
        try:
            env = gym.make("LunarLander-v3")
            state, _ = env.reset()
            done = False
            step_count = 0
            total_reward = 0.0

            while not done and self.mode == "manual":
                action = self.manual_action
                _, q_values = self.agent.act(state, eps=0.0)
                
                next_state, reward, terminated, truncated, _ = env.step(action)
                done = terminated or truncated
                state = next_state
                total_reward += reward
                self.current_score = total_reward
                step_count += 1

                pitch_angle_deg = round(float(state[4] * (180 / np.pi)), 2)

                self.broadcast_sync({
                    "type": "telemetry",
                    "mode": "manual",
                    "episode": self.current_episode,
                    "step": step_count,
                    "x": float(state[0]),
                    "y": float(state[1]),
                    "vx": float(state[2]),
                    "vy": float(state[3]),
                    "angle": float(state[4]),
                    "pitch_angle": pitch_angle_deg,
                    "angular_vel": float(state[5]),
                    "left_leg": bool(state[6] > 0.5),
                    "right_leg": bool(state[7] > 0.5),
                    "action": int(action),
                    "current_score": round(float(self.current_score), 1),
                    "raw_reward": round(float(reward), 2),
                    "shaped_reward": round(float(reward), 2),
                    "q_values": [round(float(q), 2) for q in q_values],
                    "epsilon": 0.0,
                    "loss": 0.0,
                    "done": done,
                    "success": bool(reward >= 100 and terminated),
                    "status_text": "IN FLIGHT" if not done else ("LANDED SUCCESS" if (reward >= 100 and terminated) else "CRASHED"),
                })
                time.sleep(0.025)

            env.close()
            self.broadcast_sync({
                "type": "manual_complete",
                "total_reward": round(total_reward, 1),
                "success": bool(total_reward >= 150)
            })
        except Exception as err:
            print(f"[TrainingManager] Error in manual mode: {err}")
            traceback.print_exc()
        finally:
            self.mode = "training" if self.is_training else "idle"
