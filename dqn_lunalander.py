# -*- coding: utf-8 -*-
"""
Lunar Lander Stylish Landing with Dueling Double DQN (D3QN)
Includes 1000 Episodes Training, Epsilon Decay (100% -> 5%), 
Stylish Reward Shaping, and Web Mission Control Dashboard Integration.
"""

import os
import sys
import time
import argparse
from typing import List

import gymnasium as gym
import numpy as np
import torch

from dqn_agent import DQNAgent, shape_stylish_reward

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
BEST_MODEL_PATH = os.path.join(MODEL_DIR, "best_model.pth")


def train_dqn(
    n_episodes: int = 1000,
    max_t: int = 1000,
    eps_start: float = 1.0,
    eps_end: float = 0.05,
    eps_decay: float = 0.99626,
    render: bool = False
):
    """
    Train Dueling Double DQN Agent on LunarLander-v3 for 1000 episodes.
    Epsilon starts at 100% (1.0) and decays to 5% (0.05).
    """
    print("=" * 65)
    print("🚀 [Lunar Lander] Dueling Double DQN Stylish Training Initiated")
    print(f"📊 Total Episodes: {n_episodes}")
    print(f"🎯 Exploration (Epsilon): {eps_start * 100:.1f}% -> {eps_end * 100:.1f}% (Decay: {eps_decay})")
    print("=" * 65)

    render_mode = "human" if render else None
    env = gym.make("LunarLander-v3", render_mode=render_mode)
    agent = DQNAgent(state_size=8, action_size=4, seed=42)

    scores = []
    scores_window = []
    eps = eps_start
    best_score = -float("inf")

    for i_episode in range(1, n_episodes + 1):
        state, _ = env.reset(seed=42 + i_episode)
        score = 0.0

        for t in range(max_t):
            action, _ = agent.act(state, eps)
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated

            # Apply stylish landing reward shaping
            shaped_reward = shape_stylish_reward(next_state, reward, action, terminated, truncated)

            agent.step(state, action, shaped_reward, next_state, done)
            state = next_state
            score += reward

            if done:
                break

        scores_window.append(score)
        if len(scores_window) > 100:
            scores_window.pop(0)

        scores.append(score)
        eps = max(eps_end, eps * eps_decay)  # Smooth decay to 5%

        avg_score = np.mean(scores_window)

        # Save best model
        if score > best_score:
            best_score = score
            agent.save(BEST_MODEL_PATH)

        # Periodic Log
        if i_episode % 20 == 0 or i_episode == n_episodes:
            print(
                f"Episode {i_episode:4d}/{n_episodes} | "
                f"Score: {score:7.2f} | "
                f"100-Ep Avg: {avg_score:7.2f} | "
                f"Epsilon: {eps*100:5.1f}% | "
                f"Best: {best_score:7.2f}"
            )

        if avg_score >= 200.0 and i_episode >= 100:
            print(f"\n🎉 [Environment Solved] in {i_episode} episodes! Average Score: {avg_score:.2f}")

    env.close()
    print("\n✅ Training Complete. Best model saved to:", BEST_MODEL_PATH)
    return scores


def evaluate_agent(n_episodes: int = 5):
    """Demonstrates greedy landing performance."""
    print("=" * 60)
    print("🛸 [Showcase Mode] Evaluating Trained Agent (Greedy Epsilon = 0.0)")
    print("=" * 60)

    env = gym.make("LunarLander-v3", render_mode="human")
    agent = DQNAgent(state_size=8, action_size=4, seed=42)

    if os.path.exists(BEST_MODEL_PATH):
        agent.load(BEST_MODEL_PATH)
        print(f"Loaded checkpoint from: {BEST_MODEL_PATH}")
    else:
        print("⚠️ No checkpoint found. Running with untrained agent.")

    for i in range(1, n_episodes + 1):
        state, _ = env.reset(seed=100 + i)
        score = 0.0
        done = False
        while not done:
            action, _ = agent.act(state, eps=0.0)
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            state = next_state
            score += reward
            time.sleep(0.02)
        print(f"Demo Episode {i}: Score = {score:.2f}")

    env.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lunar Lander DQN Training & Web Server")
    parser.add_argument("--web", action="store_true", default=True, help="Launch Web Mission Control Dashboard")
    parser.add_argument("--cli-train", action="store_true", help="Run CLI training directly")
    parser.add_argument("--eval", action="store_true", help="Run graphical evaluation demo")
    parser.add_argument("--port", type=int, default=8000, help="Web server port")

    args = parser.parse_args()

    if args.cli_train:
        train_dqn(n_episodes=1000)
    elif args.eval:
        evaluate_agent()
    else:
        from server import run_server
        print(f"🌟 Starting Lunar Lander Mission Control Dashboard at http://localhost:{args.port}")
        run_server(port=args.port)