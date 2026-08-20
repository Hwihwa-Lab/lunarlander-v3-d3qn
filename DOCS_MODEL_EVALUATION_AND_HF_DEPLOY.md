# 🚀 Model Evaluation & Hugging Face Deployment Guide
> **DQN Lunar Lander 모델 성능 평가 기준 및 허깅페이스(Hugging Face Hub) 배포 가이드**

---

## 📌 1. 핵심 원칙: 1000 에피소드 완주 불필요 (Early Convergence)

강화학습에서 1,000 에피소드는 모델이 극도로 정밀해지도록 설정된 최대 상한선일 뿐이며, **1,000번을 모두 채우지 않아도 최적의 시점에 모델을 배포(Hugging Face 업로드)할 수 있습니다.**

1. **최고 모델 자동 저장 (`Auto-Save Best Model`)**:
   - `training_manager.py` 및 `dqn_agent.py`는 훈련 도중 역대 최고 점수(Best Score)를 갱신할 때마다 `models/best_model.pth` 파일에 즉시 가중치를 저장합니다.
2. **조기 해결 (Early Solved)**:
   - `LunarLander-v3` 환경은 일반적으로 **300 ~ 500 에피소드 내외**에서도 200점 이상의 완벽하고 안정적인 착륙 지능에 도달합니다.

---

## 🎯 2. 허깅페이스 배포 '골든 타이밍' 3대 기준

아래 3가지 조건 중 **핵심 기준(Condition 1)**을 만족하면 즉시 허깅페이스에 업로드하기 가장 좋은 타이밍입니다.

| 지표 (Metric) | 기준 수치 (Threshold) | 의미 및 판단 근거 |
| :--- | :--- | :--- |
| **1. SMA 100 AVG** (핵심) | **$\ge$ 200.0 점** | Gymnasium 공식 '환경 해결(Solved)' 기준 달성 |
| **2. Success Rate** | **$\ge$ 80%** | 최근 비행 중 불시착/충돌 없이 안정적 착륙 성공 |
| **3. Exploration ($\epsilon$)** | **$\le$ 15% (0.15)** | 무작위 탐색을 줄이고 학습된 정책(Policy)으로 비행 |

---

## 🤖 3. AI 에이전트 자동 모니터링 프로토콜

AI 에이전트는 사용자를 대신하여 훈련 진행 상황을 실시간으로 감시하고 최적의 배포 타이밍을 포착하여 보고합니다.

```
[백그라운드 훈련 루프] ──▶ [/api/stats 모니터링] ──▶ [골든 타이밍 감지 (SMA 100 >= 200)]
                                                              │
                                                              ▼
                                               [AI 에이전트: 배포 알림 및 리포트 발행]
                                                              │
                                                              ▼
                                               [허깅페이스 Hub 원클릭 업로드 실행]
```

### 1) 모니터링 대상
- `GET /api/stats` : `moving_avg`, `success_rate`, `best_reward`, `loss`
- `models/best_model.pth` : 가중치 파일 갱신 여부 및 용량/무결성 점검

### 2) 골든 타이밍 달성 시 보고 항목
- 훈련 에피소드 수 (예: Episode 385 / 1000)
- 최고 점수 (Best Score) 및 100회 이동평균 점수 (SMA 100)
- 간지 착륙 시연(`✨ STYLISH DEMO`) 성공 여부
- 허깅페이스 모델 카드 자동 생성 제안

---

## 📦 4. 허깅페이스 배포 패키지 구성 (Model Card Artifacts)

허깅페이스 레포지토리(Model Hub)에 업로드되는 표준 패키지 구조입니다:

```
HuggingFace_Repo/ (예: Hwihwa-Lab/lunarlander-dueling-dqn)
├── README.md                 # 📄 모델 설명 카드 (하이퍼파라미터, 보상 곡선, 평가 점수)
├── best_model.pth            # 🧠 PyTorch Dueling Double DQN 신경망 가중치
├── config.json               # ⚙️ 모델 아키텍처 및 하이퍼파라미터 메타데이터
└── demonstration.gif         # 🛸 실제 착륙 성공 시연 애니메이션 (선택)
```

---

## 🚀 5. 원클릭 허깅페이스 업로드 파이프라인

`huggingface_hub` 라이브러리를 통해 CLI 명령어 또는 Python 스크립트 한 줄로 배포를 완료합니다.

```bash
# 예시 실행 명령어 (스크립트 지원 예정)
python deploy_to_hf.py --repo-id "Hwihwa-Lab/lunarlander-dueling-dqn" --model-path "models/best_model.pth"
```
