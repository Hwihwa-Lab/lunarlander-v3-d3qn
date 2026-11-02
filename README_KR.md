---
language:
- en
- ko
license: mit
library_name: pytorch
pipeline_tag: reinforcement-learning
description: "LunarLander-v3 D3QN: 60FPS 인터랙티브 오실로스코프 조종석 및 정밀 항법 항공전자 시스템을 탑재한 달 착륙선 자율 하강 및 연착륙 강화학습 모델 (Hwihwa Lab)."
tags:
- reinforcement-learning
- deep-reinforcement-learning
- deep-rl
- dqn
- d3qn
- dueling-dqn
- double-dqn
- deep-q-network
- q-learning
- value-based-rl
- off-policy
- model-free-rl
- experience-replay
- lunarlander
- lunar-lander
- lunarlander-v3
- box2d
- gymnasium
- farama-foundation
- openai-gym
- pytorch
- robotics
- space-robotics
- aerospace
- autonomous-landing
- soft-landing
- touchdown
- attitude-control
- reaction-control-system
- rcs-thruster
- cold-gas-thrusters
- flight-control
- guidance-navigation-control
- lunar-descent
- apollo
- lunar-module
- spacecraft
- space-exploration
- physical-ai
- embodied-ai
- simulation
- sim-to-real
- on-device-ai
- edge-ai
- autonomous-agents
- hwihwalab
- korean-ai-research
- south-korea
metrics:
- reward
- success-rate
model-index:
- name: lunarlander-v3-d3qn
  results:
  - task:
      type: reinforcement-learning
      name: Reinforcement Learning
    dataset:
      name: Gymnasium Box2D LunarLander-v3
      type: gymnasium/lunar-lander-v3
    metrics:
    - type: mean_reward
      value: 311.16
      name: Peak Mean Evaluation Reward
    - type: success_rate
      value: 100.0
      name: Lunar Landing Success Rate
---

# 🚀 LunarLander-v3 D3QN // Mission Control Deck v2.0

[![Language: English](https://img.shields.io/badge/Language-English-007ACC)](https://huggingface.co/hwihwalab/lunarlander-v3-d3qn) [![Language: 한국어](https://img.shields.io/badge/Language-한국어-7cb342)](https://huggingface.co/hwihwalab/lunarlander-v3-d3qn/blob/main/README_KR.md) [![🤗 실시간 인터랙티브 관제덱](https://img.shields.io/badge/🤗%20Live%20Space-Mission%20Control-blue)](https://huggingface.co/spaces/hwihwalab/lunarlander-v3-d3qn) [![Hugging Face Model Hub](https://img.shields.io/badge/🤗%20Model%20Hub-LunarLander--D3QN-orange)](https://huggingface.co/hwihwalab/lunarlander-v3-d3qn) [![🏎️ 후속 연구: Roadster D3QN](https://img.shields.io/badge/진화모델-Roadster%20D3QN-purple)](https://huggingface.co/hwihwalab/tesla-roadster-flip-landing-d3qn) [![🎯 후속 연구: Roadster PPO](https://img.shields.io/badge/진화모델-Roadster%20PPO-orange)](https://huggingface.co/hwihwalab/tesla-roadster-flip-landing-ppo) [![GitHub](https://img.shields.io/badge/GitHub-Hwihwa--Lab-181717?logo=github)](https://github.com/Hwihwa-Lab/lunarlander-v3-d3qn) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://huggingface.co/hwihwalab/lunarlander-v3-d3qn/blob/main/LICENSE)

[![PyTorch](https://img.shields.io/badge/PyTorch-D3QN-red)](https://pytorch.org) [![Gymnasium](https://img.shields.io/badge/Gymnasium-v1.0-darkgreen)](https://gymnasium.farama.org/environments/box2d/lunar_lander/) [![Benchmark](https://img.shields.io/badge/공식성공점수-%2B311.16점%20(기준%20압도적%20초과)-10B981)](https://huggingface.co/hwihwalab/lunarlander-v3-d3qn) [![Aerodynamics](https://img.shields.io/badge/물리역학-6--DoF%20달중력%20%26%20RCS-E11D48)](https://huggingface.co/hwihwalab/lunarlander-v3-d3qn) [![Telemetry](https://img.shields.io/badge/텔레메트리-실시간%20웹소켓%2050Hz-06B6D4)](https://huggingface.co/hwihwalab/lunarlander-v3-d3qn) [![Research Lab](https://img.shields.io/badge/연구개발-Hwihwa%20Lab-d0f991?labelColor=050807)](https://github.com/Hwihwa-Lab)

> “**LunarLander-v3 D3QN // Mission Control: 달 표면 자율 연착륙 & 항공우주 텔레메트리 HUD | HWIHWA LAB**  
> Dueling Double Deep Q-Network(D3QN) 신경망과 냉가스 RCS 스러스터 역학을 활용한 초정밀 자세 안정화, 수직 낙하 속도 감쇄 및 달 착륙 깃발 사이 완벽 소프트 랜딩.  
>  
> 🏛️ **원천 연구 베이스라인 (Foundational Baseline)**: 본 프로젝트는 Hwihwa Lab의 상위 항공우주 제어 연구인 테슬라 로드스터 180° 공중 전복 복구 플립 착륙의 핵심 알고리즘 및 물리적 모태가 되는 원천 연구입니다:  
> ([🏎️ D3QN](https://huggingface.co/hwihwalab/tesla-roadster-flip-landing-d3qn) & [🎯 PPO](https://huggingface.co/hwihwalab/tesla-roadster-flip-landing-ppo)).  
>  
> 🌐 [English Documentation](https://huggingface.co/hwihwalab/lunarlander-v3-d3qn) | 🇰🇷 [한국어 매뉴얼](https://huggingface.co/hwihwalab/lunarlander-v3-d3qn/blob/main/README_KR.md) | 🚀 [실시간 라이브 관제덱 (Space)](https://huggingface.co/spaces/hwihwalab/lunarlander-v3-d3qn)”  
> *Developed by [Hwihwa Lab](https://github.com/Hwihwa-Lab) · AI × Automation × Aesthetics ✨*

세련되고 안정적인("간지나는") 착륙을 위한 **Dueling Double DQN (D3QN)** 강화학습 시스템 및 원스크린(One-Screen) 3단 항공우주 관제 덱입니다.

---

## 📊 모델 스펙 및 벤치마크 평가 성과

| 항목 (Parameter) | 사양 및 달성 수치 (Specification) |
| :--- | :--- |
| **물리 환경 (Environment)** | Gymnasium Box2D `LunarLander-v3` |
| **상태 공간 (Observation Space)** | 8차원 연속 벡터 ($X, Y, V_x, V_y, \theta, \omega, \text{Leg}_L, \text{Leg}_R$) |
| **행동 공간 (Action Space)** | 4개 이산 행동 (`0: IDLE`, `1: LEFT`, `2: MAIN`, `3: RIGHT`) |
| **강화학습 알고리즘** | **Dueling Double Deep Q-Network (D3QN)** with Soft Target Update ($\tau = 0.001$) |
| **신경망 구조** | Value Stream ($8 \to 128 \to 128 \to 64 \to 1$) + Advantage Stream ($8 \to 128 \to 128 \to 64 \to 4$) + LayerNorm |
| **탐색률 (Epsilon)** | $1.0$ (100%) $\to$ $0.05$ (5%) 점진 감쇠 |
| **공식 환경 해결 기준 (Solved)** | 평균 점수 $\ge +200.0$ 점 |
| **최고 달성 착륙 점수 (Peak Score)** | **`+311.16 점`** *(환경 해결 기준 압도적 초과 달성 🏆)* |

---

## 🌟 핵심 개발 기능 및 아키텍처

### 1. 🧠 Dueling Double DQN (D3QN) 알고리즘
- **Dueling Architecture**: 상태 가치($V(s)$)와 각 행동 이점($A(s, a)$)을 독립적인 스트림으로 분리하여 학습 수렴성 극대화 ($8 \to 128 \to 128 \to 64 \to 4$)
- **Double DQN**: 행동 선택(Online Net)과 가치 평가(Target Net)를 분리하여 Q-Value 과대추정(Overestimation) 방지
- **Robust Optimization**: Soft Target Update ($\tau = 0.001$), Huber Loss (Smooth L1), AdamW, Gradient Clipping 적용

### 2. ✨ 세련된 착륙을 위한 커스텀 리워드 쉐이핑 (`shape_stylish_reward`)
- **자세 및 회전 억제**: 기체 수평 자세 유지($|\theta| < 0.08$) 및 급격한 회전 방지($|\omega| < 0.1$)
- **소프트 터치다운**: 지면 근접 시 완벽한 감속($-0.3 \le V_y \le 0.0$) 유도
- **정중앙 착지 보너스**: 착륙 패드 정중앙 양다리 동시 안착 시 대폭 추가 보상

### 3. 📉 입실론 감쇠 (Epsilon Exploration)
- **100% 탐색에서 5%로 감쇠**: 초기 $\epsilon = 1.0$ (100%) $\to$ 1,000 에피소드에 걸쳐 $\epsilon = 0.05$ (5%)로 점진 감쇠

---

## 🖥️ 3단 조종석 관제 덱 (One-Screen Fitted Design)

마우스 휠 스크롤 없이 **1536x762 화면에 100% 꽉 차는 원스크린(No-Scroll) 관제 콘솔**로 구축되었습니다.

```
+---------------------------------------------------------------------------------------------+
| 🚀 HEADER BAR : Brand | EPISODE (0/1000) | EXPLORATION (ε: 100%→5%) | BEST SCORE (+311.16)  |
+------------------------------+-------------------------------+------------------------------+
| 👈 LEFT: FLIGHT HUD          | 🛸 CENTER: SIMULATION STREAM  | 👉 RIGHT: TRAINING ANALYTICS |
| - Attitude & Pitch Gyro      | - High-FPS Apollo 2D Canvas   | - 4 Stats (Score, SMA, etc.) |
| - Velocity Gauges (Vy, Vx)   | - Mission Control Action Deck | - Chart 1: Reward & 100-MA   |
| - Coordinates & Leg Sensors  | - Autopilot / Manual / Train  | - Chart 2: Epsilon Decay     |
| - 4-Action DQN Q-Values      | - Time Warp Speed Multipliers | - Chart 3: MSE Loss Progress |
| - Mission Avionics Specs     | - Strict Quality Tiers Banner | - D3QN Architecture Specs    |
+------------------------------+-------------------------------+------------------------------+
```

### 1) 👈 Left Column: FLIGHT TELEMETRY HUD
- **인공수평선(Pitch Gyro)**: 자세 각도(`Pitch Angle`) 및 각속도(`Angular Vel`)에 따른 실시간 자이로 회전
- **속도 벡터 게이지**: 수직 속도($V_y$) 및 수평 속도($V_x$) 실시간 프로그레스 바 (위험 속도 시 색상 경고)
- **좌표 및 센서**: 고도(Altitude Y), 착륙 오프셋(Offset X), 좌/우 다리 지면 접촉 센서
- **DQN Action Q-Values**: 4개 행동 실시간 Q값 및 활성화 바 (`0: IDLE`, `1: LEFT THRUSTER`, `2: MAIN THRUSTER`, `3: RIGHT THRUSTER`)
- **MISSION AVIONICS & SENSORS 스펙 카드**: 관성측정장치(IMU), 라이다 고도계(LIDAR), 극저온 솔레노이드 밸브 등 하드웨어 텔레메트리 제원

### 2) 🛸 Center Column: SIMULATION STREAM & CONTROLS
- **실시간 GPU 가속 2D 캔버스**: 아폴로/스페이스X 캡슐 렌더링, 메인/보조 플라즈마 화염 파티클, 네온 비행 궤적 잔상, 물리 좌표와 100% 일치하는 달 표면 착륙 패드 및 깃발($|X| \le 0.20$), 골드 축하 폭죽
- **통합 제어 버튼**:
  - `[▶ START MISSION]`: 클릭 즉시 테슬라 로드스터와 동일하게 학습 완료된 최적 지능으로 무한 연속 자율 착륙 비행(Autopilot) 수행
  - `[⏸ PAUSE]`, `[🔄 RESET]`, `[📥 LOAD BEST MODEL]`
- **3대 통합 비행 운용 모드**:
  - `🤖 AUTOPILOT (DEMO)` *(기본값)*: 검증된 30개 미션 시드를 순환하며 사전 학습된 최고 모델($\epsilon=0.0$)로 100% 성공률의 완벽 정중앙 착륙을 무한 연속 시연 (착륙 후 1.2초 축하 대기 후 다음 비행 자동 진입)
  - `🎮 MANUAL FLIGHT`: 키보드(`W`/`A`/`D`, 방향키, 스페이스바)로 조종사가 직접 착륙을 제어하는 인간 수동 비행
  - `⚡ LIVE TRAINING`: 실시간 입실론 감쇠($1.0 \to 0.05$) 및 경험 리플레이 가중치 업데이트가 동반되는 실전 강화학습
- **시간 왜곡 배속 제어**: `1x`, `2x`, `5x`, `⚡ MAX`
- **정밀 착륙 품질 판정 시스템 (오인 판정 0% 방어)**:
  - `PERFECT SOFT TOUCHDOWN! 🏆`: 깃발 정중앙($|X| \le 0.08$), 초저속 감속($|V_y| \le 0.35$), 양다리 동시 안착
  - `TOUCHDOWN SUCCESS! 🎉`: 착륙 패드 깃발 내부 안착($|X| \le 0.20$), 안전 수직 속도($|V_y| \le 0.55$), 다리 센서 접촉
  - `OFF-PAD LANDING (OUT OF BOUNDS) ⚠️`: 선체 충돌 없이 서서 멈췄으나 깃발 바깥 거친 암반에 착지한 경우 (패드 이탈 경고)
  - `CRASH DETECTED 💥`: 착지 속도 초과, 기체 전복, 선체 직접 충돌

### 3) 👉 Right Column: DQN TRAINING ANALYTICS
- **4대 핵심 지표**: `CURRENT SCORE`, `SMA 100 AVG`, `SUCCESS RATE (%)`, `TRAINING LOSS`
- **3-Tier 실시간 독립 차트 (Chart.js)**:
  1. `EPISODE REWARD & 100-MA` (공식 해결 기준선 > 200)
  2. `EPSILON (100% → 5% DECAY)` (탐색률 감쇠 곡선)
  3. `MSE LOSS PROGRESSION` (신경망 학습 손실 추이)
- **D3QN ARCHITECTURE SPECS 스펙 카드**: 신경망 레이어 구조, 소프트 타겟 업데이트($\tau=1\text{e-}3$), AdamW 옵티마이저 등 AI 엔진 스펙 명시

---

## 🎮 키보드 조작 가이드 (`🎮 MANUAL FLIGHT` 모드)

| 키 | 동작 (Action) |
| :--- | :--- |
| **`↑` / `W` / `Space`** | **메인 엔진 분사 (MAIN THRUSTER)** - 상승 및 하강 감속 |
| **`←` / `A`** | **좌측 엔진 분사 (LEFT THRUSTER)** - 우측으로 기울임 |
| **`→` / `D`** | **우측 엔진 분사 (RIGHT THRUSTER)** - 좌측으로 기울임 |
| **키를 뗌** | **엔진 정지 (IDLE COAST)** |

---

## 📂 저장소 파일 구성 (Repository Contents)

- `best_model.pth`: 공식 해결 기준(+200.0)을 압도적으로 초과 달성한 D3QN 최적 모델 가중치 (+311.16점)
- `config.json`: 모델 신경망 구조, 하이퍼파라미터 및 Box2D 환경 설정 파일
- `dqn_agent.py`: 독립 실행 가능한 PyTorch 기반 `DQNAgent` 및 `DuelingQNetwork` 신경망 아키텍처 원본 소스코드
- `README.md`: 글로벌 배포용 공식 영문 모델 카드 및 벤치마크 가이드
- `README_KR.md`: 한국어 종합 미션 컨트롤 기술 매뉴얼 및 텔레메트리 관제 명세서
- `LICENSE`: MIT 오픈소스 라이선스 전문

---

## 🚀 빠른 시작 가이드

### 1. 원클릭 통합 실행 (권장)
```bash
python run.py
```
실행 후 브라우저에서 **[http://localhost:8000](http://localhost:8000)**에 접속하시면 즉시 실시간 관제 콘솔을 이용하실 수 있습니다.

### 2. CLI 고속 학습 단독 실행
```bash
python dqn_lunalander.py --cli-train
```

### 3. 허깅페이스 원클릭 배포
```bash
python deploy_to_hf.py
```

---

## 👤 Hwihwa Lab 소개 (About Hwihwa Lab)

> **“AI × Automation × Aesthetics — Crafting tools you'll love ✨”**  
> 휘화랩(Hwihwa Lab)은 온디바이스 인공지능, 자율 운영 에이전트, 그리고 세련된 인터랙티브 미학을 융합하는 1인 독립 AI 연구소입니다. 반복적이고 소모적인 운영 부담을 덜어냄으로써 솔로프리너와 창작자가 본질적인 창작과 비즈니스의 즐거움에 집중할 수 있는 견고한 시스템을 설계합니다.

### 🔬 핵심 연구 및 엔지니어링 영역
- **Zero-Cost Edge Operations**: 지속적인 클라우드 API 비용 없는 완전 독립 온디바이스 AI 파이프라인 구축.
- **Autonomous Decision OS & Micro-ERP**: 일상적인 운영 결정과 프로세스를 체계적으로 조율하는 전두엽 스타일의 결정 지능 아키텍처.
- **Embodied AI & Domain-Specific Robotics**: 시뮬레이션 기반 강화학습(RL), 물리적 기동 제어 두뇌 및 실세계 서비스 환경을 위한 특화 데이터 엔지니어링.
- **Interactive Creative Aesthetics**: 기능적 자동화에 정교한 비주얼 크래프트와 현대적 디자인 철학을 결합한 매력적인 도구 제작.

### 🌐 공식 채널 & 항공우주 강화학습(Aerospace RL) 연구 계보
- **Research Studio**: [🤗 Hugging Face (@hwihwalab)](https://huggingface.co/hwihwalab) · [🐙 GitHub (@Hwihwa-Lab)](https://github.com/Hwihwa-Lab)
- **🚀 자율 비행 & 착륙 제어 연구 라인업**:
  - 🌕 **Phase 1 · 클래식 달 표면 연착륙 (본 모델 / 원천 베이스라인)**: [lunarlander-v3-d3qn Model Hub](https://huggingface.co/hwihwalab/lunarlander-v3-d3qn)
  - 🛸 **Phase 1 · 실시간 웹 관제덱**: [lunarlander-v3-d3qn Spaces](https://huggingface.co/spaces/hwihwalab/lunarlander-v3-d3qn) (*Zero-server 60fps 웹 브라우저 비행 덱*)
  - 🏎️ **Phase 2 · 공중 180° 전복 반전 복구 (D3QN)**: [tesla-roadster-flip-landing-d3qn](https://huggingface.co/hwihwalab/tesla-roadster-flip-landing-d3qn) (*신중한 가치 기반 제어로 100% 무결점 착륙 달성*)
  - 🎯 **Phase 2 · 초고속 탄도 반전 복구 (PPO)**: [tesla-roadster-flip-landing-ppo](https://huggingface.co/hwihwalab/tesla-roadster-flip-landing-ppo) (*53% 빠른 애자일 기동으로 98% 연착륙 달성*)
  - 🛸 **듀얼 엔진 실시간 3D 콕핏**: [tesla-roadster-flip-landing](https://huggingface.co/spaces/hwihwalab/tesla-roadster-flip-landing) (*웹 브라우저 60fps 텔레메트리 관제 덱*)

---

## 📄 라이선스 (License)
본 프로젝트는 MIT 라이선스에 따라 자유롭게 사용 및 수정할 수 있습니다. 자세한 내용은 [LICENSE](https://github.com/Hwihwa-Lab/lunarlander-v3-d3qn/blob/main/LICENSE) 파일을 참조하십시오.

---

*Trained and deployed with [LunarLander Mission Control](https://huggingface.co/hwihwalab/lunarlander-v3-d3qn) by **HWIHWALAB**.*
