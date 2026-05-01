#!/bin/bash
# 매일 오전 9시 날씨 자동 수집 cron 등록

SCRIPT_PATH="$HOME/claude-workspace/fetch_weather.py"
LOG_PATH="$HOME/claude-workspace/weather_cron.log"

# 등록할 cron 라인 (매일 09:00 실행)
CRON_LINE="0 9 * * * /usr/bin/python3 $SCRIPT_PATH >> $LOG_PATH 2>&1"
CRON_MARKER="fetch_weather.py"

# 기존 등록 여부 확인
if crontab -l 2>/dev/null | grep -q "$CRON_MARKER"; then
    echo "이미 등록되어 있습니다:"
    crontab -l | grep "$CRON_MARKER"
    echo ""
    read -p "다시 등록할까요? (y/N): " answer
    if [[ "$answer" != "y" && "$answer" != "Y" ]]; then
        echo "취소했습니다."
        exit 0
    fi
    # 기존 항목 제거 후 재등록
    (crontab -l 2>/dev/null | grep -v "$CRON_MARKER"; echo "$CRON_LINE") | crontab -
else
    # 신규 등록
    (crontab -l 2>/dev/null; echo "$CRON_LINE") | crontab -
fi

echo ""
echo "✅ 등록 완료!"
echo "   실행 시각 : 매일 오전 9:00"
echo "   스크립트  : $SCRIPT_PATH"
echo "   결과 파일 : $HOME/claude-workspace/weather.txt"
echo "   실행 로그 : $LOG_PATH"
echo ""
echo "현재 crontab:"
crontab -l
