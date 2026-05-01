# claude-workspace

> Jerome의 Claude Code 메인 작업 공간입니다.
> 이 폴더는 Claude Code가 작업할 때 자동으로 읽는 **컨텍스트와 규칙**의 허브입니다.

---

## 📂 폴더 구조

```
claude-workspace/
│
├── CLAUDE.md             ← Claude Code 지침서 (세션 시작 시 자동 로드)
├── README.md             ← 이 파일 (폴더 구조 안내)
├── SECURITY.md           ← 🚨 비상 매뉴얼 (키 노출 대응)
├── .gitignore            ← Git 제외 목록 (.env, 로그, 캐시 등)
│
├── tasks/                ← 작업 관리
│   ├── todo.md           ←   오늘 할 일 (체크리스트)
│   └── progress.md       ←   완료한 일 (append-only 로그)
│
├── docs/                 ← 샘플/참고 문서
│   ├── resume.pdf        ←   샘플 이력서 PDF
│   └── sales.csv         ←   샘플 매출 데이터
│
├── logs/                 ← 실행 로그 (git 제외)
│
├── fetch_weather.py      ← 날씨 → Discord 전송 스크립트 (.env 사용)
├── setup_cron.sh         ← cron 등록 헬퍼 스크립트
├── weather.txt           ← fetch_weather.py 실행 결과 샘플
├── portfolio.html        ← 포트폴리오 페이지 샘플
│
└── .env                  ← (git 제외) 환경변수 / API 키
                              ⚠️ 절대 커밋 금지
```

---

## 📄 파일 역할 요약

| 파일 / 폴더 | 누가 읽나 | 언제 수정하나 |
|------------|---------|------------|
| `CLAUDE.md` | Claude Code (세션 시작 시 자동 로드) | 지침/규칙을 바꿀 때 |
| `README.md` | 사람 (나) | 폴더 구조가 바뀔 때 |
| `SECURITY.md` | 사람, 비상시 Claude Code | 새 서비스 추가 / 대응 절차 개선 시 |
| `.gitignore` | Git | 새 민감 파일 패턴이 생겼을 때 |
| `tasks/todo.md` | 사람 + Claude Code | 작업 시작 전 계획 작성 |
| `tasks/progress.md` | 사람 + Claude Code | 작업 완료 후 기록 (append-only) |
| `docs/` | 사람 | 샘플 파일 추가/교체 시 |
| `fetch_weather.py` | 사용자 / cron | 기능 변경 시 |
| `setup_cron.sh` | 사람 | cron 일정 변경 시 |
| `.env` | 스크립트 | 새 API 키 발급 시 |

---

## 🚀 Claude Code 사용 워크플로우

### 1. 새 작업 시작할 때
```
"[작업 내용] 해줘"
   ↓
Claude Code가 tasks/todo.md 확인
   ↓
3단계 이상이면 todo.md에 계획부터 작성
   ↓
내가 OK하면 실행 시작
```

### 2. 작업 중
- Claude Code는 한 단계씩 작업하고 중간에 보고
- 에러 나면 멈추고 원인부터 분석 (`CLAUDE.md` Rule #3)
- 위험한 작업(`rm -rf`, `git push --force` 등)은 먼저 물어봄

### 3. 작업 끝날 때
- `tasks/todo.md` 항목을 `- [x]`로 체크
- `tasks/progress.md`에 한 일 요약 추가
- 실제로 돌려보고 확인 후 "다 했다" 선언

---

## 🔒 보안 원칙 (요약)

> 전체 내용은 [`SECURITY.md`](./SECURITY.md) 참조

1. **API 키는 항상 마스킹** — `sk-or-v1-***`
2. **`.env`는 절대 커밋 금지** — `.gitignore`에 등록 필수
3. **키는 코드에 하드코딩 금지** — `os.environ["..."]`만 사용
4. **키 노출 의심 시 즉시 폐기** — 재발급보다 폐기가 먼저
5. 비상시: `SECURITY.md`를 단계별로 따라가기

---

## 🛠 자주 쓰는 명령어

```bash
# 작업 공간으로 이동
cd ~/claude-workspace

# 오늘 할 일 확인
cat tasks/todo.md

# 최근 작업 기록 확인
tail -50 tasks/progress.md

# Claude Code 실행
claude

# 환경변수 로드 (필요 시)
set -a && source .env && set +a

# 날씨 스크립트 수동 실행
python3 fetch_weather.py
```

---

## 🔗 관련 경로

| 항목 | 경로 |
|------|------|
| Claude Code 전역 설정 | `~/.claude/` |
| Claude Code 전역 규칙 | `~/.claude/CLAUDE.md`, `~/.claude/rules/` |
| Oracle SSH 키 | `~/.ssh/oracle-server.key` |
| Oracle 서버 SSH 별칭 | `oracle-server` |

---

## 📝 변경 이력

- **2026-04-14** — 초기 셋업: `tasks/`, `SECURITY.md`, `README.md` 생성
- **2026-05-01** — GitHub private 레포 등록, `.gitignore` 강화, README 폴더 구조 재정리

---

*폴더 구조나 파일 역할이 바뀌면 이 README도 함께 업데이트해 주세요.*
