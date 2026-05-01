# 🚨 SECURITY.md — 비상 매뉴얼

> API 키 노출, 계정 탈취, 의심스러운 활동이 감지되면 **이 문서 순서대로** 대응합니다.
> Claude Code에게 "키 노출 의심"이라고 말하면 자동으로 이 문서를 따라 안내합니다.

---

## 🔴 STEP 0 — 침착하게 상황 판단 (30초)

먼저 다음을 확인하세요:

- [ ] 어떤 키가 노출되었는가? (OpenRouter? Oracle SSH? WordPress? AWS? GitHub?)
- [ ] 어디에 노출되었는가? (GitHub public repo? Slack? 스크린샷? 로그?)
- [ ] 언제 노출되었을 가능성이 있는가? (방금? 몇 시간 전? 며칠 전?)

> ⏱ **핵심: 속도가 전부입니다.** 노출 시점부터 자동 스캐너가 키를 수집하기까지 보통 **수 분**밖에 걸리지 않습니다.

---

## 🔴 STEP 1 — 즉시 키 폐기 (Revoke)

각 서비스별 **폐기(revoke)** 경로입니다. **재발급보다 폐기가 먼저입니다.**

### OpenRouter
1. https://openrouter.ai/keys 접속
2. 노출된 키 찾아서 **Delete** 클릭
3. 새 키는 나중에 만들기

### Oracle Cloud (SSH 키)
1. Oracle Cloud Console → Compute → Instances → 해당 인스턴스
2. 인스턴스 접속 후 `~/.ssh/authorized_keys`에서 해당 공개키 라인 삭제
3. 또는 Mac 로컬에서 `~/.ssh/oracle-server.key` 삭제 + 새 키 생성

### WordPress
1. wp-admin → 사용자 → 프로필 → **애플리케이션 비밀번호** 전체 폐기
2. 관리자 비밀번호 변경
3. 2FA가 없다면 지금 활성화

### AWS / GCP / Azure
1. IAM 콘솔 → 해당 액세스 키 **비활성화(Deactivate)** → **삭제(Delete)**
2. CloudTrail / Audit Log에서 이상 활동 확인

### GitHub Personal Access Token
1. https://github.com/settings/tokens → 해당 토큰 **Delete**
2. Settings → Security log에서 이상 활동 확인

### API 서비스 일반 (Anthropic, OpenAI, Stripe 등)
1. 해당 서비스 대시보드 → API Keys → **Revoke / Delete**
2. 사용 이력(Usage) 확인 — 내가 쓴 것보다 많다면 악용됨

---

## 🔴 STEP 2 — 새 키 발급 + 환경변수 교체

폐기가 끝났다면 새 키를 만듭니다.

```bash
# .env 파일 편집
nano ~/claude-workspace/.env

# 기존 키 라인을 새 키로 교체
# 예: OPENROUTER_API_KEY=sk-or-v1-새로운키...
```

**체크리스트:**
- [ ] `.env`에 새 키 저장
- [ ] `.env`가 `.gitignore`에 포함되어 있는지 확인
- [ ] 키를 사용하는 스크립트/앱 재시작
- [ ] 새 키가 정상 작동하는지 테스트

---

## 🔴 STEP 3 — 노출 경로 차단

### GitHub에 커밋된 경우
```bash
# 1. 로컬에서 키 제거 후 다시 커밋하는 것만으로는 부족함
# 2. git history에 남아있으므로 완전히 지워야 함

# 옵션 A: 해당 레포가 private이고 본인만 사용 → 새 키만 발급해도 충분
# 옵션 B: public이거나 여러 명 사용 → history 재작성 필요
git filter-repo --path-glob '*.env' --invert-paths
git push --force origin main  # 주의: 팀과 협의 필수
```

> ⚠️ GitHub에 한 번이라도 올라간 키는 **반드시 폐기**하세요. history에서 지웠다고 안전한 것이 아닙니다.

### Slack / Discord / 채팅에 올린 경우
1. 해당 메시지 삭제
2. 하지만 **이미 스크래핑됐을 가능성**이 있으므로 키 폐기 필수

### 스크린샷에 포함된 경우
1. 스크린샷이 올라간 곳 확인 (Twitter, 블로그, 문서)
2. 해당 이미지 삭제 또는 모자이크 처리
3. 키 폐기 필수 (이미지 OCR로 자동 수집되는 봇이 존재)

---

## 🔴 STEP 4 — 피해 조사 (Forensics)

### 사용 이력 확인
| 서비스 | 확인 방법 |
|-------|---------|
| OpenRouter | 대시보드 → Activity |
| Oracle | Cloud Console → Audit → Events |
| WordPress | 플러그인: WP Activity Log |
| AWS | CloudTrail |
| GitHub | Settings → Security log |

**확인 포인트:**
- 내가 기억하지 못하는 API 호출이 있는가?
- 모르는 IP에서 접근한 기록이 있는가?
- 비정상적으로 큰 요금이 발생했는가?

### 요금 확인
- [ ] 크레딧/요금 대시보드 확인
- [ ] 이상 사용이 있다면 **즉시 서비스 고객지원에 연락** (보통 환불 가능)

---

## 🛡️ STEP 5 — 재발 방지

### 1. `.gitignore` 점검
```bash
cat ~/claude-workspace/.gitignore
```
다음 패턴이 포함되어야 합니다:
```
.env
.env.*
*.key
*.pem
id_rsa
id_ed25519
credentials*
secrets*
```

### 2. `git-secrets` / `gitleaks` 설치 (커밋 전 자동 검사)
```bash
brew install gitleaks
cd ~/claude-workspace
gitleaks detect --source . --verbose
```

### 3. pre-commit 훅 추가
```bash
# .git/hooks/pre-commit
#!/bin/bash
gitleaks protect --staged --verbose || exit 1
```

### 4. 환경변수만 사용 — 하드코딩 금지
```python
# ❌ 나쁜 예
api_key = "sk-or-v1-abc123..."

# ✅ 좋은 예
import os
api_key = os.environ["OPENROUTER_API_KEY"]
```

### 5. 키 마스킹 습관
- 스크린샷 찍을 때 키 부분 가리기
- Claude Code에게도 "키 보여줘"라고 하지 말기 — 마스킹해서만 확인

---

## 📞 긴급 연락처

| 서비스 | 지원 채널 |
|-------|---------|
| Anthropic | support@anthropic.com |
| OpenRouter | Discord 서버 / support@openrouter.ai |
| Oracle Cloud | Console → Help → Contact Support |
| GitHub | https://support.github.com |
| AWS | Console → Support Center |

---

## ✅ 사후 체크리스트 (사건 종료 후)

- [ ] 모든 노출 키 폐기 완료
- [ ] 새 키 발급 + 환경변수 교체 완료
- [ ] 사용 이력 확인 — 이상 없음 or 환불 처리 중
- [ ] `.gitignore` 및 secret 스캐너 재정비
- [ ] `tasks/progress.md`에 사건 개요와 교훈 기록
- [ ] 같은 실수를 반복하지 않기 위한 체크리스트 추가

---

> 💬 **기억하세요:** 키 노출은 실수가 아니라 **확률의 문제**입니다. 한 번이라도 겪으면 그 다음부터는 자동화된 방어 장치를 반드시 마련하세요.
