# 🏛️ 시스템 아키텍처 및 폴더 구조 (System Architecture)

본 문서는 `Lunalander` 강화학습 미션 컨트롤 시스템의 백엔드/프론트엔드/알고리즘 구조를 기술합니다.

---

## 1. 시스템 목적 및 개요
Gymnasium `LunarLander-v3` 환경에서 Dueling Double DQN 기반 강화학습을 수행하며, 초경량 실시간 WebSocket 텔레메트리 스트리밍을 통해 브라우저 상에 NASA 스타일의 3단 항공우주 관제 덱을 60FPS로 렌더링하는 시스템입니다.

---

## 2. 기술 스택 (Tech Stack)
*   **Reinforcement Learning**: PyTorch (Dueling Double DQN, Experience Replay, Huber Loss, AdamW)
*   **Simulation Env**: Gymnasium Box2D (`LunarLander-v3`)
*   **Backend Server**: FastAPI, Uvicorn, Python `asyncio` & `threading` (Non-blocking worker)
*   **Communication**: WebSocket (`/ws` 양방향 텔레메트리 및 명령 통신), REST API (`/api/*`)
*   **Frontend**: Vanilla HTML5/CSS3 (Glassmorphism), HTML5 Canvas 2D (GPU 가속 랜더링), Chart.js v4 (3단 실시간 반응형 차트)

---

## 3. 폴더 구조 및 모듈 역할 (Directory Structure)

```
c:\Users\crack\Lunalander\
├── .cursorrules                  # 🛑 AI 바이브 코딩 및 디자인 임의 변경 방어 규칙
├── DOCS_AI_CODING_PROTOCOL.md    # 🛡️ 마스터 코딩 프로토콜 및 문서 맵핑
├── DOCS_UI_DESIGN_SPEC.md        # 🎨 UI/디자인 불변 규격서 (원스크린 3단 덱)
├── DOCS_SYSTEM_ARCHITECTURE.md   # 🏛️ 전체 시스템 아키텍처 명세서
├── DOCS_DATA_SCHEMA.md           # 📊 WebSocket 및 모델 데이터 스키마
├── dqn_agent.py                  # DuelingQNetwork 신경망 및 DQNAgent 강화학습 로직
├── training_manager.py           # 1000 에피소드 관리, 4대 히스토리, 멀티스레드 루프
├── server.py                     # FastAPI 웹 및 WebSocket 서버
├── run.py                        # 원클릭 통합 실행 런처
├── models/                       # 모델 가중치 저장 폴더
│   ├── best_model.pth            # 최고 점수 모델 체크포인트
│   └── latest_model.pth          # 최근 체크포인트
└── static/                       # 프론트엔드 정적 에셋
    ├── index.html                # 원스크린 3단 조종석 HTML 마크업
    ├── css/
    │   └── style.css             # 원스크린 노스크롤 사이버펑크 디자인 시스템
    └── js/
        ├── render.js             # 캔버스 우주선, 파티클, 지형, 화염 렌더러
        └── app.js                # WebSocket 통신, 자이로 회전, Chart.js 3종 제어
```

---

## 4. 핵심 데이터 파이프라인
1. **DQN 에이전트 연산**: `dqn_agent.py`에서 상태(8차원)를 받아 4개 액션의 Q-Value 연산 및 Soft Target Update 진행.
2. **비동기 텔레메트리 브로드캐스트**: `training_manager.py` 스레드에서 `asyncio.run_coroutine_threadsafe`를 통해 WebSocket 구독자에게 JSON 텔레메트리 전송.
3. **클라이언트 렌더링**: `app.js`에서 텔레메트리를 수신하여 `render.js` Canvas에 60FPS로 기체 및 화염 파티클 렌더링, 좌측 Gyro 회전 및 우측 Chart.js 업데이트.
