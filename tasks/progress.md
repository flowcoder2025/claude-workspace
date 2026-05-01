# 작업 기록 (PROGRESS)

> 완료한 작업을 **append-only**로 기록합니다. (위에서 아래로 최신순이 아니라, 시간순으로 추가)
> 이전 기록은 **수정하거나 삭제하지 않습니다**. 필요하면 새 항목을 추가합니다.

---

## 2026-04-14 — 작업 환경 초기 셋업

**완료한 일**
1. `tasks/` 폴더 생성
2. `tasks/todo.md` — 체크리스트 파일 생성 (작업 템플릿 포함)
3. `tasks/progress.md` — 이 파일 생성
4. `SECURITY.md` — 키 노출/비상 매뉴얼 작성
5. `README.md` — 폴더 구조 및 사용법 정리

**검증**
- `ls -la ~/claude-workspace/`로 파일 존재 확인
- 각 파일을 다시 읽어 내용이 정상적으로 저장되었는지 확인

**결과**
- 이제 Claude Code가 `~/claude-workspace`에서 작업할 때 `tasks/todo.md`로 계획하고, `tasks/progress.md`에 결과를 남기며, 비상시 `SECURITY.md`를 참조할 수 있음.

**다음에 할 일**
- 실제 작업이 생기면 `tasks/todo.md`에 체크리스트로 추가
- 필요하면 `.env` 파일 생성 (API 키 저장용, 절대 git 커밋 금지)

---

<!-- 여기 아래로 새 항목을 추가하세요. 위 내용은 건드리지 마세요. -->

## 2026-05-01 — claude-workspace를 GitHub private 레포로 등록

**완료한 일**
1. `.gitignore` 강화: `.DS_Store`, `logs/`, `.claude/settings.local.json`, `__pycache__/`, `*.bak` 등 추가 (기존 `.env`, `*.key`, `*.pem`, `id_rsa`, `credentials`, `weather_cron.log` 유지)
2. `README.md` 갱신: 실제 폴더 구조 반영 (`fetch_weather.py`, `setup_cron.sh`, `docs/`, `portfolio.html`, `weather.txt`, `logs/` 추가)
3. `git init -b main` → 12개 파일 스테이징
4. 첫 커밋: `Initial setup`
5. `gh repo create claude-workspace --private --source=. --push` (계정: chrokdaddy-cmd)

**검증**
- `git status --ignored`로 `.env`, `.claude/`, `logs/`, `.DS_Store`가 제외됨을 사전 확인
- 푸시 후 `gh repo view`로 visibility=PRIVATE 확인
- `gh api .../contents/.env` → 404 (원격에 .env 없음 확인)

**결과**
- 레포 URL: https://github.com/chrokdaddy-cmd/claude-workspace (private)
- 기본 브랜치: main
- 커밋된 파일 12개, 민감 파일 0개

**다음에 할 일**
- 평소 작업 후 `git add → commit → push`로 변경사항 백업
- 새 민감 파일 생기면 `.gitignore`에 즉시 추가

---

## 2026-05-01 — portfolio.html 라이트/다크 테마 토글 추가

**완료한 일**
1. 새 브랜치 `feature/theme-toggle` 생성
2. `portfolio.html` CSS:
   - `:root`를 `[data-theme="dark"]`와 통합, `--nav-bg` / `--noise-opacity` 토큰화
   - `[data-theme="light"]` 색 팔레트 추가 (베이지 #FAF7F2 + 다크 텍스트)
   - `.theme-toggle` 버튼 스타일 + 호버 회전, 아이콘 표시 토글
3. HTML: nav-links 마지막에 ☾/☀ 토글 버튼 추가
4. JS: `localStorage` 저장 + `prefers-color-scheme` 시스템 설정 존중
5. 사용자 브라우저 검증 OK 확인
6. `feature/theme-toggle` → `main` fast-forward 머지 → `git push origin main`

**검증**
- HTML 태그 무결성: nav/script/style 1:1 짝 맞음
- 토글 버튼/localStorage 코드 존재 grep 확인
- 사용자가 브라우저에서 토글 동작 확인 후 OK
- push 결과: `baea242..768d152  main -> main`

**결과**
- 변경 라인: +74 / -3 (portfolio.html)
- 커밋: `Add light/dark theme toggle to portfolio` (768d152)
- 시스템 다크모드면 다크로, 라이트면 라이트로 시작 → 토글 시 localStorage에 저장
