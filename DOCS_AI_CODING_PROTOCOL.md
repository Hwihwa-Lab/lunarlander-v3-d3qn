# 🛡️ AI Coding Protocol (Lunar Lander 마스터 지침서)

본 문서는 AI가 본 `Lunalander` 프로젝트에서 작업할 때 '바이브 코딩(Vibe Coding)' 및 무단 디자인/로직 변경을 방어하기 위한 마스터 가이드입니다.

---

## 📂 문서 맵핑 (Document Mapping)
AI는 코드 및 스타일 작성 전, 작업 내용에 맞춰 아래의 문서를 **반드시 선행 로드**하고 숙지해야 합니다.

* **전체 시스템 및 백엔드 아키텍처 파악 시:** `DOCS_SYSTEM_ARCHITECTURE.md` 필수 확인
* **UI/CSS/HTML 레이아웃 및 디자인 수정 시:** `DOCS_UI_DESIGN_SPEC.md` 필수 확인 (디자인 훼손 방지)
* **데이터 모델, WebSocket 메시지 규격, API 수정 시:** `DOCS_DATA_SCHEMA.md` 필수 확인

---

## 🛑 핵심 방어 수칙

1. **디자인 및 원스크린(One-Screen) 임의 변경 금지**:
   - 사용자가 승인한 3단 그리드 조종석 레이아웃과 폰트 크기, 스크롤 없는(No-Scroll) UI 비율을 임의로 깨뜨리지 마십시오.
2. **영문 표준 준수 (Aerospace English)**:
   - 모든 버튼 라벨, 계기판 이름, 통계 지표는 전문적인 영문 표기를 유지해야 합니다.
3. **JSON 및 WebSocket 스키마 무단 변경 금지**:
   - `telemetry`, `episode_summary`, `stats`의 키 값을 임의로 삭제하거나 축약하지 마십시오.
4. **환각 기능(Dummy Data) 금지**:
   - 실제 모델 연산 및 Gymnasium 환경과 연결되지 않은 가짜 수치를 렌더링하지 마십시오.
5. **사후 문서 자동 동기화 의무**:
   - 기능 변경 시 관련 `DOCS_*.md` 문서를 반드시 스스로 업데이트하십시오.
