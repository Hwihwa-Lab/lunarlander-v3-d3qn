# 🚀 Lunar Lander DQN Mission Control Deck v2.0

> **Gymnasium Box2D `LunarLander-v3` Reinforcement Learning Cockpit & Real-time Aerospace Dashboard**  
> 세련되고 안정적인("간지나는") 착륙을 위한 **Dueling Double DQN (D3QN)** 강화학습 시스템 및 원스크린(One-Screen) 3단 항공우주 관제 덱입니다.

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
| 🚀 HEADER BAR : Brand | EPISODE (0/1000) | EXPLORATION (ε: 100%→5%) | BEST SCORE            |
+------------------------------+-------------------------------+------------------------------+
| 👈 LEFT: FLIGHT HUD          | 🛸 CENTER: SIMULATION STREAM  | 👉 RIGHT: TRAINING ANALYTICS |
| - Attitude & Pitch Gyro      | - High-FPS Apollo 2D Canvas   | - 4 Stats (Score, SMA, etc.) |
| - Velocity Gauges (Vy, Vx)   | - Mission Control Action Deck | - Chart 1: Reward & 100-MA   |
| - Coordinates & Leg Sensors  | - 4 Mode Tabs & Speed Control | - Chart 2: Epsilon Decay     |
| - 4-Action DQN Q-Values      | - Touchdown / Crash Banner    | - Chart 3: MSE Loss Progress |
+------------------------------+-------------------------------+------------------------------+
```

### 1) 👈 Left Column: FLIGHT TELEMETRY HUD
- **인공수평선(Pitch Gyro)**: 자세 각도(`Pitch Angle`) 및 각속도(`Angular Vel`)에 따른 실시간 자이로 회전
- **속도 벡터 게이지**: 수직 속도($V_y$) 및 수평 속도($V_x$) 실시간 프로그레스 바 (위험 속도 시 색상 경고)
- **좌표 및 센서**: 고도(Altitude Y), 착륙 오프셋(Offset X), 좌/우 다리 지면 접촉 센서
- **DQN Action Q-Values**: 4개 행동 실시간 Q값 및 활성화 바 (`0: IDLE`, `1: LEFT THRUSTER`, `2: MAIN THRUSTER`, `3: RIGHT THRUSTER`)

### 2) 🛸 Center Column: SIMULATION STREAM & CONTROLS
- **실시간 GPU 가속 2D 캔버스**: 아폴로/스페이스X 캡슐 렌더링, 메인/보조 플라즈마 화염 파티클, 네온 비행 궤적 잔상, 달 표면 분화구/깃발, 완벽 착륙 축하 골드 폭죽
- **통합 제어 버튼**:
  - `[▶ START MISSION]`, `[⏸ PAUSE]`, `[🔄 RESET]`, `[📥 LOAD BEST MODEL]`
- **4가지 비행 모드**:
  - `⚡ LIVE TRAINING`: 실시간 강화학습 진행 및 탐색 비행
  - `⏩ TURBO SPEED`: 렌더링 딜레이를 최소화한 초고속 1000 에피소드 학습
  - `✨ STYLISH DEMO`: 학습된 최고 지능으로 0% 탐색 완벽 착륙 1회 시연
  - `🎮 MANUAL FLIGHT`: 키보드로 인간이 직접 우주선을 조종하는 비행 모드
- **속도 조절**: `1x`, `2x`, `5x`, `⚡ MAX`

### 3) 👉 Right Column: DQN TRAINING ANALYTICS
- **4대 핵심 지표**: `CURRENT SCORE`, `SMA 100 AVG`, `SUCCESS RATE (%)`, `TRAINING LOSS`
- **3-Tier 실시간 독립 차트 (Chart.js)**:
  1. `EPISODE REWARD & 100-MA` (목표 기준선 > 200)
  2. `EPSILON (100% → 5% DECAY)` (탐색률 감쇠 곡선)
  3. `MSE LOSS PROGRESSION` (신경망 학습 손실 추이)

---

## 🎮 키보드 조작 가이드 (`🎮 MANUAL FLIGHT` 모드)

| 키 | 동작 (Action) |
| :--- | :--- |
| **`↑` / `W` / `Space`** | **메인 엔진 분사 (MAIN THRUSTER)** - 상승 및 하강 감속 |
| **`←` / `A`** | **좌측 엔진 분사 (LEFT THRUSTER)** - 우측으로 기울임 |
| **`→` / `D`** | **우측 엔진 분사 (RIGHT THRUSTER)** - 좌측으로 기울임 |
| **키를 뗌** | **엔진 정지 (IDLE COAST)** |

---

## 🛡️ AI 바이브 코딩 방어 및 문서화 시스템

본 프로젝트는 무단 디자인 변경 및 데이터 스키마 왜곡을 방지하기 위한 체계적인 문서 규칙을 갖추고 있습니다.

- **[`.cursorrules`](file:///c:/Users/crack/Lunalander/.cursorrules)**: AI Vibe-Coding 방어 규칙 (디자인 보존 및 문서 자동 동기화 의무)
- **[`DOCS_AI_CODING_PROTOCOL.md`](file:///c:/Users/crack/Lunalander/DOCS_AI_CODING_PROTOCOL.md)**: 마스터 코딩 프로토콜 및 문서 맵핑
- **[`DOCS_UI_DESIGN_SPEC.md`](file:///c:/Users/crack/Lunalander/DOCS_UI_DESIGN_SPEC.md)**: UI/디자인 불변 규격서 (원스크린 3단 덱)
- **[`DOCS_SYSTEM_ARCHITECTURE.md`](file:///c:/Users/crack/Lunalander/DOCS_SYSTEM_ARCHITECTURE.md)**: 시스템 아키텍처 명세서
- **[`DOCS_DATA_SCHEMA.md`](file:///c:/Users/crack/Lunalander/DOCS_DATA_SCHEMA.md)**: WebSocket 텔레메트리 및 데이터 스키마

---

## 🚀 빠른 시작 가이드

### 1. 원클릭 통합 실행 (권장)
```bash
python run.py
```
실행 후 브라우저에서 **[http://localhost:8000](http://localhost:8000)**에 접속하시면 즉시 실시간 관제 콘솔을 이용하실 수 있습니다.

### 2. CLI 학습만 단독 실행
```bash
python dqn_lunalander.py
```

---

## 📦 GitHub 저장소
- **Repository**: [https://github.com/Hwihwa-Lab/LunarLander-DQN](https://github.com/Hwihwa-Lab/LunarLander-DQN) (Private)
