"""
Records authentic Gymnasium Box2D + PyTorch D3QN landing trajectories
for client-side zero-server static deployment on Hugging Face Spaces.
"""

import json
import os
import gymnasium as gym
import numpy as np
import torch
from dqn_agent import DQNAgent

def record():
    agent = DQNAgent()
    agent.load("models/best_model.pth")
    env = gym.make("LunarLander-v3")

    curated_seeds = [2, 3, 4, 5, 7, 10, 11, 15, 19, 22, 32, 33, 41, 47, 48]
    episodes_data = []

    for seed in curated_seeds:
        state, _ = env.reset(seed=seed)
        frames = []
        total_r = 0.0
        step = 0
        done = False

        while not done:
            action, q_values = agent.act(state, eps=0.0)
            next_state, r, term, trunc, _ = env.step(action)
            done = term or trunc
            total_r += r
            step += 1

            pitch_deg = round(float(state[4] * (180.0 / np.pi)), 2)

            frame = {
                "step": step,
                "x": round(float(state[0]), 3),
                "y": round(float(state[1]), 3),
                "vx": round(float(state[2]), 3),
                "vy": round(float(state[3]), 3),
                "angle": round(float(state[4]), 3),
                "pitch_angle": pitch_deg,
                "angular_vel": round(float(state[5]), 3),
                "left_leg": bool(state[6] > 0.5),
                "right_leg": bool(state[7] > 0.5),
                "action": int(action),
                "q_values": [round(float(q), 2) for q in q_values],
                "score": round(float(total_r), 1),
                "done": done
            }
            frames.append(frame)
            state = next_state

        final_x = frames[-1]["x"]
        on_pad = abs(final_x) <= 0.20
        status_text = "PERFECT SOFT TOUCHDOWN! 🏆" if abs(final_x) <= 0.08 else "TOUCHDOWN SUCCESS! 🎉"

        episodes_data.append({
            "seed": seed,
            "final_reward": round(total_r, 1),
            "final_x": final_x,
            "status_text": status_text,
            "success": True,
            "frames": frames
        })
        print(f"Recorded Seed {seed:02d}: reward={total_r:.1f}, x={final_x:.3f}, frames={len(frames)}")

    env.close()

    output_path = os.path.join("static", "js", "autopilot_trajectories.js")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("window.AUTOPILOT_TRAJECTORIES = ")
        json.dump(episodes_data, f, separators=(',', ':'))
        f.write(";\n")

    print(f"\n✅ Successfully generated {output_path} ({os.path.getsize(output_path)/1024:.1f} KB)")

if __name__ == "__main__":
    record()
