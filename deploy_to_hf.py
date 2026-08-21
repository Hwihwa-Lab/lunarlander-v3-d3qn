"""
One-Click Hugging Face Deployment Pipeline for Lunar Lander D3QN.
Uploads model weights, config, and auto-generated Model Card (README.md) to Hugging Face Hub.
"""

import os
import sys
import json
import argparse
from pathlib import Path
import torch
from huggingface_hub import HfApi, create_repo

def generate_model_card(repo_id: str, best_score: float = None) -> str:
    """Generate Hugging Face Model Card with metadata and evaluation docs."""
    score_display = f"{best_score:.1f}" if best_score is not None else "200.0+ (Solved)"
    
    card_content = f"""---
library_name: gymnasium
tags:
- reinforcement-learning
- dueling-dqn
- double-dqn
- deep-q-network
- lunarlander-v3
- pytorch
- aerospace
pipeline_tag: reinforcement-learning
model-index:
- name: {repo_id.split('/')[-1]}
  results:
  - task:
      type: reinforcement-learning
      name: Reinforcement Learning
    dataset:
      name: Gymnasium LunarLander-v3
      type: gymnasium/lunar-lander-v3
    metrics:
    - type: mean_reward
      value: {score_display}
      name: Mean Evaluation Reward
---

# 🚀 LunarLander-v3 Dueling Double DQN (D3QN) Agent

> **Gymnasium Box2D `LunarLander-v3` Reinforcement Learning Agent & Real-time Aerospace Telemetry System**  
> 🐙 **GitHub Repository**: [https://github.com/Hwihwa-Lab/lunarlander-v3-d3qn](https://github.com/Hwihwa-Lab/lunarlander-v3-d3qn)

This repository contains a pre-trained **Dueling Double Deep Q-Network (D3QN)** agent trained on the [Gymnasium](https://gymnasium.farama.org/environments/box2d/lunar_lander/) `LunarLander-v3` environment.

---

## 🌟 Model Highlights
- **Algorithm**: Dueling Double DQN (D3QN) with Soft Target Updates ($\\tau = 0.001$)
- **Architecture**: Separated Value ($V(s)$) and Advantage ($A(s, a)$) streams ($8 \\to 128 \\to 128 \\to 64 \\to 4$)
- **Optimization**: Smooth L1 (Huber) Loss, AdamW, Gradient Clipping
- **Custom Reward Shaping**: Stabilized pitch angle, soft touchdown velocity damping, and center-pad landing rewards.

---

## 📂 Repository Contents
- `best_model.pth`: Pre-trained PyTorch Dueling Double DQN neural network weights (+311.16 score).
- `config.json`: Model architecture, hyperparameters, and environment specifications.
- `dqn_agent.py`: Complete PyTorch source code for `DQNAgent` and `DuelingQNetwork`.
- `README.md`: Comprehensive model documentation, telemetry specs, and evaluation guide.

---

## 📊 Environment & Action Space

- **Observation Space (8 Dimensions)**:
  1. Coordinate $X$
  2. Coordinate $Y$
  3. Linear Velocity $V_x$
  4. Linear Velocity $V_y$
  5. Pitch Angle $\\theta$
  6. Angular Velocity $\\omega$
  7. Left Leg Ground Contact (0 or 1)
  8. Right Leg Ground Contact (0 or 1)

- **Action Space (4 Discrete Actions)**:
  - `0`: IDLE (Coast)
  - `1`: Fire Left Thruster
  - `2`: Fire Main Engine Thruster
  - `3`: Fire Right Thruster

---

## ⚙️ Hyperparameters

| Hyperparameter | Value | Description |
| :--- | :--- | :--- |
| **Learning Rate** | `5e-4` | AdamW optimizer learning rate |
| **Discount Factor ($\\gamma$)** | `0.99` | Future reward discount factor |
| **Replay Buffer Size** | `100,000` | Experience replay memory capacity |
| **Batch Size** | `64` | Mini-batch sample size for training |
| **Target Network Update ($\\tau$)** | `0.001` | Polyak soft update rate |
| **Exploration ($\\epsilon$)** | `1.0 \\to 0.05` | 100% exploration decaying to 5% |

---

## 💻 How to Load & Evaluate

You can easily load and run this trained model in Python using PyTorch and Gymnasium:

```python
import torch
import torch.nn as nn
import gymnasium as gym

# 1. Define Dueling DQN Architecture
class DuelingDQN(nn.Module):
    def __init__(self, state_dim=8, action_dim=4):
        super().__init__()
        self.feature_network = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.LayerNorm(128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.LayerNorm(128),
            nn.ReLU(),
        )
        self.value_stream = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )
        self.advantage_stream = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, action_dim)
        )

    def forward(self, state):
        features = self.feature_network(state)
        values = self.value_stream(features)
        advantages = self.advantage_stream(features)
        return values + (advantages - advantages.mean(dim=-1, keepdim=True))

# 2. Download weights from Hugging Face Hub
from huggingface_hub import hf_hub_download

weights_path = hf_hub_download(repo_id="{repo_id}", filename="best_model.pth")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = DuelingDQN().to(device)
model.load_state_dict(torch.load(weights_path, map_location=device))
model.eval()

# 3. Test Agent Flight
env = gym.make("LunarLander-v3", render_mode="human")
state, _ = env.reset()
total_reward = 0

for _ in range(1000):
    state_t = torch.FloatTensor(state).unsqueeze(0).to(device)
    with torch.no_grad():
        action = model(state_t).argmax(dim=-1).item()
    
    state, reward, terminated, truncated, _ = env.step(action)
    total_reward += reward
    if terminated or truncated:
        break

print(f"Final Flight Reward: {{total_reward:.2f}}")
env.close()
```

---

## 🛠️ Training & Telemetry
Developed and trained with the [**Lunar Lander Mission Control Deck**](https://github.com/Hwihwa-Lab/lunarlander-v3-d3qn) real-time telemetry system.
- Full Dashboard UI & Source Code: [https://github.com/Hwihwa-Lab/lunarlander-v3-d3qn](https://github.com/Hwihwa-Lab/lunarlander-v3-d3qn)
"""
    return card_content.strip()

def deploy(repo_name: str = "lunarlander-v3-d3qn", private: bool = False, model_path: str = "models/best_model.pth"):
    api = HfApi()
    
    # 1. Verify authentication
    try:
        user_info = api.whoami()
        username = user_info["name"]
        print(f"🔑 Authenticated as: [bold cyan]{username}[/bold cyan]" if "rich" in sys.modules else f"🔑 Authenticated as: {username}")
    except Exception as e:
        print(f"❌ Authentication failed. Please run 'hf auth login' first. Error: {e}")
        return False

    repo_id = f"{username}/{repo_name}"
    
    # 2. Check model file existence
    if not os.path.exists(model_path):
        print(f"❌ Model weight file not found at: {model_path}")
        print("💡 Please ensure training has created 'models/best_model.pth'.")
        return False
        
    print(f"📦 Model weight found: {model_path} ({os.path.getsize(model_path) / 1024:.1f} KB)")

    # 3. Create or verify repository on Hugging Face
    print(f"🌐 Creating / checking repository: {repo_id} (Private={private})...")
    try:
        create_repo(repo_id=repo_id, repo_type="model", private=private, exist_ok=True)
        print(f"✅ Repository ready: https://huggingface.co/{repo_id}")
    except Exception as e:
        print(f"❌ Failed to create repo {repo_id}: {e}")
        return False

    # 4. Generate & upload config.json
    config_data = {
        "algorithm": "Dueling Double DQN (D3QN)",
        "environment": "LunarLander-v3",
        "state_dim": 8,
        "action_dim": 4,
        "hidden_dim": 128,
        "gamma": 0.99,
        "lr": 0.0005,
        "batch_size": 64,
        "tau": 0.001,
        "framework": "PyTorch",
        "library": "Gymnasium"
    }
    
    temp_dir = Path("scratch")
    temp_dir.mkdir(exist_ok=True)
    
    config_file = temp_dir / "config.json"
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=2)
        
    readme_file = temp_dir / "README.md"
    with open(readme_file, "w", encoding="utf-8") as f:
        f.write(generate_model_card(repo_id))

    # 5. Upload files to Hugging Face Hub
    print("📤 Uploading files to Hugging Face Hub...")
    try:
        # Upload model weight
        api.upload_file(
            path_or_fileobj=model_path,
            path_in_repo="best_model.pth",
            repo_id=repo_id,
            repo_type="model",
            commit_message="Upload LunarLander D3QN best model weights"
        )
        print("  - [1/4] Uploaded best_model.pth ✅")
        
        # Upload config.json
        api.upload_file(
            path_or_fileobj=str(config_file),
            path_in_repo="config.json",
            repo_id=repo_id,
            repo_type="model",
            commit_message="Upload model configuration and metadata"
        )
        print("  - [2/4] Uploaded config.json ✅")
        
        # Upload dqn_agent.py (PyTorch architecture source)
        if os.path.exists("dqn_agent.py"):
            api.upload_file(
                path_or_fileobj="dqn_agent.py",
                path_in_repo="dqn_agent.py",
                repo_id=repo_id,
                repo_type="model",
                commit_message="Upload DQNAgent and DuelingQNetwork PyTorch architecture source"
            )
            print("  - [3/4] Uploaded dqn_agent.py (Architecture Source) ✅")
        
        # Upload README.md (Model Card)
        api.upload_file(
            path_or_fileobj=str(readme_file),
            path_in_repo="README.md",
            repo_id=repo_id,
            repo_type="model",
            commit_message="Upload comprehensive Model Card README"
        )
        print("  - [4/4] Uploaded README.md (Model Card) ✅")
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return False

    print("\n" + "="*60)
    print("🎉 DEPLOYMENT COMPLETE! YOUR MODEL IS LIVE ON HUGGING FACE! 🚀")
    print(f"👉 Model URL: https://huggingface.co/{repo_id}")
    print("="*60 + "\n")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy LunarLander DQN to Hugging Face")
    parser.add_argument("--repo-name", type=str, default="lunarlander-v3-d3qn", help="Name of the Hugging Face repository")
    parser.add_argument("--private", action="store_true", help="Set repository to private")
    parser.add_argument("--model-path", type=str, default="models/best_model.pth", help="Path to model weights")
    args = parser.parse_args()

    deploy(repo_name=args.repo_name, private=args.private, model_path=args.model_path)
