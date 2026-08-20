# 📊 데이터 스키마 (Data Schema Specification)

본 문서는 `Lunalander` 프로젝트의 WebSocket 메시지 규격, REST API 응답 포맷, DQN 상태/행동 벡터 규격을 정의합니다. **여기에 정의되지 않은 변수나 Key 값을 임의로 상상하여 변경하지 마십시오.**

---

## 1. WebSocket Telemetry Message (실시간 비행 프레임)
`training_manager.py` $\to$ `static/js/app.js`

```json
{
  "type": "telemetry",
  "mode": "training | turbo | showcase | manual",
  "episode": "number (1 ~ 1000)",
  "step": "number",
  "x": "number (-1.0 ~ 1.0, 수평 위치)",
  "y": "number (0.0 ~ 1.4, 고도)",
  "vx": "number (수평 속도)",
  "vy": "number (수직 속도)",
  "angle": "number (기체 기울기 라디안)",
  "pitch_angle": "number (도 단위 Degree)",
  "angular_vel": "number (각속도 rad/s)",
  "left_leg": "boolean (좌측 다리 지면 접촉 여부)",
  "right_leg": "boolean (우측 다리 지면 접촉 여부)",
  "action": "enum (0: IDLE, 1: LEFT, 2: MAIN, 3: RIGHT)",
  "current_score": "number (현재 에피소드 누적 보상)",
  "raw_reward": "number",
  "shaped_reward": "number",
  "q_values": ["number", "number", "number", "number"],
  "epsilon": "number (0.05 ~ 1.0)",
  "loss": "number (MSE/Huber Loss)",
  "done": "boolean",
  "success": "boolean",
  "status_text": "string (IN FLIGHT | LANDED SUCCESS | CRASHED)"
}
```

---

## 2. WebSocket Episode Summary Message (에피소드 종료 요약)
```json
{
  "type": "episode_summary",
  "episode": "number",
  "reward": "number",
  "moving_avg": "number (최근 100회 이동평균)",
  "epsilon": "number (퍼센트 단위)",
  "loss": "number",
  "steps": "number",
  "success": "boolean",
  "stats": {
    "current_episode": "number",
    "max_episodes": 1000,
    "total_steps": "number",
    "current_score": "number",
    "epsilon": "number",
    "best_reward": "number",
    "moving_avg": "number",
    "success_count": "number",
    "success_rate": "number (%)",
    "mode": "string",
    "is_training": "boolean",
    "is_paused": "boolean",
    "speed": "number",
    "loss": "number"
  }
}
```

---

## 3. Client Command Schema (클라이언트 $\to$ 서버 명령)
```json
{
  "command": "start | pause | resume | stop | reset | set_mode | set_speed | load_best | manual_action",
  "mode": "training | turbo | showcase | manual (optional)",
  "speed": "1.0 | 2.0 | 5.0 | -1.0 (optional)",
  "action": "0 | 1 | 2 | 3 (optional, manual_action 시)"
}
```
