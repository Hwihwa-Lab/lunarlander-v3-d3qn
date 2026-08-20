# 🚀 Lunar Lander Cyberpunk Mission Control (DQN RL Dashboard)

루나랜더(LunarLander-v3)의 세련되고 안정적인("간지나는") 착륙을 위한 **Dueling Double DQN (D3QN)** 강화학습 시스템 및 실시간 우주선 관제 센터 웹 대시보드입니다.

---

## 🌟 핵심 특징

1. **Dueling Double DQN (D3QN) 강화학습 알고리즘**:
   - 가치(Value) & 이점(Advantage) 스트림 분리 구조
   - Double DQN 타깃 분리로 과대추정 방지
   - Huber Loss & Gradient Clipping으로 학습 안정성 극대화

2. **간지나는(Stylish) 착륙을 위한 커스텀 리워드 쉐이핑**:
   - 기체 수평 자세 유지($|\theta| < 0.08$) 및 회전 억제($|\omega| < 0.1$)
   - 지면 근접 시 부드러운 하강 속도(Soft Landing) 유도
   - 착륙 패드 정중앙 양다리 동시 터치다운 웰스타일 보너스

3. **입실론 감쇠(Epsilon Exploration)**:
   - 초기 $\epsilon = 1.0$ ($100\%$) 탐색 $\to$ 1,000 에피소드에 걸쳐 $\epsilon = 0.05$ ($5\%$)로 감쇠

4. **사이버네틱 관제 센터 웹 대시보드**:
   - **실시간 2D 캔버스 시뮬레이터**: 아폴로 착륙선 그래픽, 플라즈마 분사 화염 파티클, 비행 궤적 네온 트레일, 분화구 및 달 표면 지형, 깃발 및 축하 폭죽 이펙트
   - **실시간 텔레메트리 HUD**: 고도, $V_x$, $V_y$, 각도, 각속도, 좌/우 착륙 기어 센서
   - **AI Brain 분석**: 4개 행동(NOOP, Left, Main, Right)의 실시간 Q-Value 바 차트
   - **학습 곡선 차트**: 에피소드 리워드 & 100회 이동평균선 실시간 그래프 (Chart.js)
   - **미션 컨트롤**: [Start Mission / Pause], [Reset], 1x~10x & ⚡ MAX 배속 조절
   - **Showcase AI 모드**: 현재 학습된 최고 지능으로 0% 탐색 완벽 착륙 시연
   - **Manual Flight 모드**: 키보드 방향키(↑, ←, →)로 직접 착륙선을 조종해보는 인간 vs AI 모드

---

## 🚀 실행 방법

### 웹 관제 센터 실행 (권장)
```bash
python run.py
```
브라우저에서 `http://localhost:8000` 접속 후 **[Start Mission]** 버튼을 클릭하면 실시간 학습과 착륙 화면이 펼쳐집니다!

### CLI 학습 직접 실행
```bash
python dqn_lunalander.py --cli-train
```
