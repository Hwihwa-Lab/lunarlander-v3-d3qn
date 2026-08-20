# 🎨 UI & Design Specification (디자인 및 레이아웃 불변 명세서)

본 문서는 `Lunalander` 프로젝트의 **3단 조종석 관제 콘솔(Mission Control Deck)** 디자인 표준을 정의하며, AI가 임의로 디자인을 바꾸지 못하도록 고정하는 기준 명세서입니다.

---

## 🖥️ 1. 원스크린(One-Screen) 노스크롤 기본 원칙
- **해상도 기준**: `1536 x 762` (및 일반적인 1080p 브라우저 뷰포트)
- **스크롤 정책**: 메인 대시보드 화면에 **세로 스크롤바가 전혀 생기지 않는 `overflow: hidden; height: 100vh;` 원스크린 핏** 유지.
- **폰트 가독성**: 글자가 찌그러지거나 너무 작아지지 않도록 수치 `0.9rem~1.25rem`, 라벨 `0.65rem~0.75rem`의 시원시원한 시인성 유지.

---

## 🏛️ 2. 3-Column Deck 레이아웃 구조

```
+---------------------------------------------------------------------------------------------+
| 🚀 HEADER BAR (46px) : Brand | EPISODE (0/1000) | EXPLORATION (ε) | BEST SCORE              |
+------------------------------+-------------------------------+------------------------------+
| 👈 LEFT COLUMN (290px)       | 🛸 CENTER COLUMN (1.22fr)     | 👉 RIGHT COLUMN (330px)      |
| [FLIGHT TELEMETRY HUD]       | [SIMULATION STREAM]           | [DQN TRAINING ANALYTICS]     |
|                              |                               |                              |
| 1. ATTITUDE & PITCH GYRO     | 1. High-FPS Canvas (410px+)   | 1. 4 Metric Cards (2x2 Grid) |
|    - 원형 인공수평선 그래픽   |    - Apollo/SpaceX Lander     |    - CURRENT SCORE           |
|    - Pitch Angle / Omega     |    - Neon Jet Particle Trail  |    - SMA 100 AVG             |
| 2. VELOCITY VECTORS          |    - Lunar Terrain & Flag     |    - SUCCESS RATE            |
|    - Vy (Vertical) Bar       | 2. Mission Control Deck       |    - TRAINING LOSS           |
|    - Vx (Horizontal) Bar     |    - [▶ START MISSION] (Green)| 2. 3-Tier Multi Charts       |
| 3. COORDINATES & SENSORS     |    - [⏸ PAUSE] (Orange)      |    - Chart 1: Reward & 100-MA|
|    - Altitude (Y) / Offset(X)|    - [🔄 RESET] (Red)          |    - Chart 2: Epsilon Decay  |
|    - Left/Right Leg Contacts |    - [📥 LOAD BEST MODEL]     |    - Chart 3: MSE Loss       |
| 4. DQN ACTION Q-VALUES       |    - MODE Tabs (4 Types)      |                              |
|    - 0: IDLE (COAST)         |    - SPEED Selector (1x~MAX)  |                              |
|    - 1: LEFT THRUSTER        |                               |                              |
|    - 2: MAIN THRUSTER        |                               |                              |
|    - 3: RIGHT THRUSTER       |                               |                              |
+------------------------------+-------------------------------+------------------------------+
```

---

## 🌐 3. 표준 영문 텍스트 규격 (Aerospace English)

### 1) 좌측 HUD:
- `0: IDLE (COAST)`
- `1: LEFT THRUSTER`
- `2: MAIN THRUSTER`
- `3: RIGHT THRUSTER`
- `PITCH ANGLE`, `ANGULAR VEL`, `VERTICAL VEL (Vy)`, `HORIZONTAL VEL (Vx)`, `ALTITUDE (Y)`, `OFFSET (X)`, `LEFT LEG SENSOR`, `RIGHT LEG SENSOR`

### 2) 중앙 컨트롤 덱:
- **Buttons**: `▶ START MISSION`, `⏸ PAUSE`, `🔄 RESET`, `📥 LOAD BEST MODEL`
- **Modes**: `⚡ LIVE TRAINING`, `⏩ TURBO SPEED`, `✨ STYLISH DEMO`, `🎮 MANUAL FLIGHT`
- **Speeds**: `1x`, `2x`, `5x`, `⚡ MAX`

### 3) 우측 분석 덱:
- `CURRENT SCORE`, `SMA 100 AVG`, `SUCCESS RATE`, `TRAINING LOSS`
- `EPISODE REWARD & 100-MA (Goal: > 200)`, `EPSILON (100% → 5% DECAY)`, `MSE LOSS PROGRESSION`

---

## 🎨 4. 컬러 시스템 (Cyberpunk Aerospace Palette)
- **배경**: `#060913` (Primary Dark), `#0b1120` (Secondary Navy)
- **카드 배경**: `rgba(15, 23, 42, 0.85)` (Glassmorphism Blur 14px)
- **시안 네온**: `#00f2fe` / `#38bdf8` (테두리 및 메인 하이라이트)
- **그린 네온**: `#10b981` (착륙 성공, 정상 상태, 스타트 버튼)
- **앰버/옐로우 네온**: `#fbbf24` (경고, 탐색률 Epsilon, SMA 100)
- **퍼플 네온**: `#c084fc` (고급 모델, 손실함수 Loss)
- **레드 네온**: `#ef4444` (충돌, 위험, 리셋 버튼)
