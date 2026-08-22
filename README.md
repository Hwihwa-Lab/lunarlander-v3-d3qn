# 🚀 LunarLander-v3 D3QN // Mission Control Deck

[![Language: English](https://img.shields.io/badge/Language-English-blue)](README.md)
[![Language: 한국어](https://img.shields.io/badge/Language-한국어-green)](README_KR.md)
[![Hugging Face Model Hub](https://img.shields.io/badge/🤗%20Hugging%20Face-Model%20Hub-orange)](https://huggingface.co/hwihwalab/lunarlander-v3-d3qn)
[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-181717?style=flat&logo=github)](https://github.com/Hwihwa-Lab/lunarlander-v3-d3qn)
[![Gymnasium](https://img.shields.io/badge/Gymnasium-LunarLander--v3-darkgreen)](https://gymnasium.farama.org/environments/box2d/lunar_lander/)
[![Algorithm](https://img.shields.io/badge/Algorithm-DQN-blue)](https://github.com/Hwihwa-Lab/lunarlander-v3-d3qn)
[![PyTorch](https://img.shields.io/badge/PyTorch-D3QN-red)](https://pytorch.org)

> **Gymnasium Box2D `LunarLander-v3` Reinforcement Learning Cockpit & Real-time Aerospace Telemetry Dashboard**  
> *[ 🌐 English Documentation ](README.md) | [ 🇰🇷 한국어 매뉴얼 ](README_KR.md)*

**LunarLander D3QN Mission Control Deck** is an advanced Dueling Double Deep Q-Network (D3QN) reinforcement learning system paired with a zero-scroll, real-time 3-column aerospace telemetry dashboard engineered for high-precision, stylish lunar touchdowns.

---

## 📊 Model Specifications & Benchmark Results

| Parameter | Specification & Achievement |
| :--- | :--- |
| **Environment** | Gymnasium Box2D `LunarLander-v3` |
| **Observation Space** | 8-dimensional continuous state vector ($X, Y, V_x, V_y, \theta, \omega, \text{Leg}_L, \text{Leg}_R$) |
| **Action Space** | 4 discrete actions (`0: IDLE`, `1: LEFT THRUSTER`, `2: MAIN THRUSTER`, `3: RIGHT THRUSTER`) |
| **Algorithm** | **Dueling Double Deep Q-Network (D3QN)** with Polyak Target Updates ($\tau = 0.001$) |
| **Neural Architecture** | Separated Value Stream ($8 \to 128 \to 128 \to 64 \to 1$) + Advantage Stream ($8 \to 128 \to 128 \to 64 \to 4$) with LayerNorm |
| **Exploration ($\epsilon$)** | $1.0$ (100%) $\to$ $0.05$ (5%) smooth decay schedule |
| **Official Solved Benchmark** | Average Score $\ge +200.0$ points |
| **Peak Landing Score Achieved** | **`+311.16 points`** *(Substantially exceeds solved benchmark 🏆)* |

---

## 🌟 Core Algorithmic Highlights

### 1. 🧠 Dueling Double DQN (D3QN) Architecture
- **Dueling Stream Decomposition**: Decomposes Q-values into state-value $V(s)$ and action advantage $A(s, a)$ to accelerate policy convergence on non-action-critical states.
- **Double DQN Value Estimation**: Decouples action selection (Online Network) from value estimation (Target Network) to eliminate severe Q-value overestimation bias.
- **Robust Training Optimization**: Huber Loss (Smooth L1), AdamW optimizer, LayerNorm feature normalization, and gradient clipping.

### 2. ✨ Stylish Landing Custom Reward Shaping (`shape_stylish_reward`)
- **Attitude & Angular Lock**: Enforces horizontal hull orientation ($|\theta| < 0.08$) and penalizes excessive rotational spin ($|\omega| < 0.1$).
- **Soft Touchdown Velocity Damping**: Rewards smooth deceleration upon ground proximity ($-0.3 \le V_y \le 0.0$).
- **Precision Center-Pad Bonus**: Substantial reward incentive for simultaneous dual-leg ground contact directly between landing flags.

---

## 🖥️ 3-Column Mission Control Deck (One-Screen Fitted Design)

Engineered as a **1536x762 zero-scroll, high-density aerospace flight telemetry dashboard** (`overflow: hidden; height: 100vh;`).

```
+---------------------------------------------------------------------------------------------+
| 🚀 HEADER BAR : Brand | EPISODE (0/1000) | EXPLORATION (ε: 100%→5%) | BEST SCORE (+311.16)  |
+------------------------------+-------------------------------+------------------------------+
| 👈 LEFT: FLIGHT HUD          | 🛸 CENTER: SIMULATION STREAM  | 👉 RIGHT: TRAINING ANALYTICS |
| - Attitude & Pitch Gyro      | - High-FPS Apollo 2D Canvas   | - 4 Stats (Score, SMA, etc.) |
| - Velocity Gauges (Vy, Vx)   | - Mission Control Action Deck | - Chart 1: Reward & 100-MA   |
| - Coordinates & Leg Sensors  | - 4 Mode Tabs & Speed Control | - Chart 2: Epsilon Decay     |
| - 4-Action DQN Q-Values      | - Touchdown / Crash Banner    | - Chart 3: MSE Loss Progress |
+------------------------------+-------------------------------+------------------------------+
```

### 1) 👈 Left Column: FLIGHT TELEMETRY HUD
- **Artificial Horizon (Pitch Gyro)**: Dynamic attitude indicator rotating with vessel pitch angle ($\theta$) and angular velocity ($\omega$).
- **Velocity Vector Bars**: Real-time vertical ($V_y$) and horizontal ($V_x$) velocity progress meters with caution/danger color thresholds.
- **Coordinates & Contact Sensors**: Real-time altitude ($Y$), pad offset ($X$), and left/right landing gear contact indicators.
- **4-Action DQN Q-Values**: Live Q-value bars for `0: IDLE (COAST)`, `1: LEFT THRUSTER`, `2: MAIN THRUSTER`, `3: RIGHT THRUSTER`.

### 2) 🛸 Center Column: SIMULATION STREAM & FLIGHT CONTROLS
- **Hardware-Accelerated 2D Canvas**: Apollo/SpaceX lander sprite, plasma exhaust particle engines, neon trajectory motion trails, lunar terrain with craters, landing flags, and golden touchdown fireworks.
- **Integrated Mission Controls**:
  - `[▶ START MISSION]`, `[⏸ PAUSE]`, `[🔄 RESET]`, `[📥 LOAD BEST MODEL]`
- **4 Flight Operating Modes**:
  - `⚡ LIVE TRAINING`: Real-time active RL training and exploration flight.
  - `⏩ TURBO SPEED`: High-speed training with minimal rendering latency.
  - `✨ STYLISH DEMO`: Zero-exploration ($\epsilon=0.0$) showcase of trained best model.
  - `🎮 MANUAL FLIGHT`: Human keyboard manual flight simulator.
- **Speed Multipliers**: `1x`, `2x`, `5x`, `⚡ MAX`.

### 3) 👉 Right Column: DQN TRAINING ANALYTICS
- **4 Real-time Metrics**: `CURRENT SCORE`, `SMA 100 AVG`, `SUCCESS RATE (%)`, `TRAINING LOSS`.
- **3-Tier Synchronized Multi-Charts (Chart.js)**:
  1. `EPISODE REWARD & 100-MA` (Solved Threshold: > 200.0)
  2. `EPSILON (100% → 5% DECAY)` (Exploration decay curve)
  3. `MSE LOSS PROGRESSION` (Neural network loss trajectory)

---

## 🎮 Manual Flight Controls (`🎮 MANUAL FLIGHT` Mode)

| Key Binding | Flight Action |
| :--- | :--- |
| **`↑` / `W` / `Space`** | **Fire Main Engine Thruster** (Ascend & Decelerate Descent) |
| **`←` / `A`** | **Fire Left Thruster** (Tilt Right / Move East) |
| **`→` / `D`** | **Fire Right Thruster** (Tilt Left / Move West) |
| **Release Key** | **Engine Idle / Free Coast** |

---

## 🚀 Quick Start Guide

### 1. Launch Mission Control Dashboard (Recommended)
```bash
python run.py
```
Open your browser and navigate to **[http://localhost:8000](http://localhost:8000)** to access the real-time aerospace control deck.

### 2. Standalone CLI High-Speed Training
```bash
python dqn_lunalander.py --cli-train
```

### 3. Deploy to Hugging Face Model Hub
```bash
python deploy_to_hf.py
```

---

## 💻 Quick Evaluation Snippet

You can load and evaluate this pre-trained agent in 5 lines of Python:

```python
import torch, gymnasium as gym
from dqn_agent import DQNAgent

# 1. Initialize environment & agent
env = gym.make("LunarLander-v3", render_mode="human")
agent = DQNAgent(state_size=8, action_size=4)
agent.load("models/best_model.pth")

# 2. Run greedy landing evaluation
state, _ = env.reset()
done = False
while not done:
    action, _ = agent.act(state, eps=0.0)
    state, reward, terminated, truncated, _ = env.step(action)
    done = terminated or truncated

env.close()
```

---

## 🛡️ AI Vibe-Coding Governance & Documentation Architecture

This repository is strictly protected by automated anti-vibe-coding governance to preserve architecture integrity and prevent regression:

- **[`.cursorrules`](file:///c:/Users/crack/Lunalander/.cursorrules)**: AI Vibe-Coding Defense Master Constitution
- **[`DOCS_AI_CODING_PROTOCOL.md`](file:///c:/Users/crack/Lunalander/DOCS_AI_CODING_PROTOCOL.md)**: Master Coding Protocol & Document Map
- **[`DOCS_UI_DESIGN_SPEC.md`](file:///c:/Users/crack/Lunalander/DOCS_UI_DESIGN_SPEC.md)**: UI/UX Invariance Specification (1536x762 One-Screen 3-Column Deck)
- **[`DOCS_SYSTEM_ARCHITECTURE.md`](file:///c:/Users/crack/Lunalander/DOCS_SYSTEM_ARCHITECTURE.md)**: Full-Stack System Architecture Spec
- **[`DOCS_DATA_SCHEMA.md`](file:///c:/Users/crack/Lunalander/DOCS_DATA_SCHEMA.md)**: WebSocket Telemetry Protocol & Data Schema
- **[`DOCS_MODEL_EVALUATION_AND_HF_DEPLOY.md`](file:///c:/Users/crack/Lunalander/DOCS_MODEL_EVALUATION_AND_HF_DEPLOY.md)**: Evaluation Standards & Hugging Face Hub Pipeline

---

## 📦 Open Source Hubs

- 🐙 **GitHub Repository**: [https://github.com/Hwihwa-Lab/lunarlander-v3-d3qn](https://github.com/Hwihwa-Lab/lunarlander-v3-d3qn)
- 🤗 **Hugging Face Model Hub**: [https://huggingface.co/hwihwalab/lunarlander-v3-d3qn](https://huggingface.co/hwihwalab/lunarlander-v3-d3qn)
