#!/usr/bin/env python3
"""
서울 강남구 날씨 및 미세먼지 정보 수집
- 날씨: open-meteo.com (API 키 불필요)
- 미세먼지: air-quality-api.open-meteo.com (API 키 불필요)
"""

import json
import os
import sys
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError

# 서울 강남구 좌표
LAT = 37.5172
LON = 127.0473
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "weather.txt")


def load_env():
    """프로젝트 루트의 .env 파일을 읽어 환경변수로 등록"""
    env_path = os.path.join(SCRIPT_DIR, ".env")
    if not os.path.exists(env_path):
        return
    with open(env_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())

# WMO 날씨 코드 → 한국어
WEATHER_CODES = {
    0: "맑음",
    1: "대체로 맑음",
    2: "구름 조금",
    3: "흐림",
    45: "안개",
    48: "안개 (서리)",
    51: "가벼운 이슬비",
    53: "이슬비",
    55: "강한 이슬비",
    61: "가벼운 비",
    63: "비",
    65: "강한 비",
    71: "가벼운 눈",
    73: "눈",
    75: "강한 눈",
    77: "눈발",
    80: "소나기 (약)",
    81: "소나기",
    82: "강한 소나기",
    85: "눈 소나기 (약)",
    86: "눈 소나기",
    95: "뇌우",
    96: "우박 동반 뇌우",
    99: "강한 우박 동반 뇌우",
}


def grade_pm10(value):
    """PM10 미세먼지 등급 (환경부 기준)"""
    if value is None:
        return "측정불가"
    if value <= 30:
        return "좋음 🟢"
    elif value <= 80:
        return "보통 🟡"
    elif value <= 150:
        return "나쁨 🟠"
    else:
        return "매우나쁨 🔴"


def grade_pm25(value):
    """PM2.5 초미세먼지 등급 (환경부 기준)"""
    if value is None:
        return "측정불가"
    if value <= 15:
        return "좋음 🟢"
    elif value <= 35:
        return "보통 🟡"
    elif value <= 75:
        return "나쁨 🟠"
    else:
        return "매우나쁨 🔴"


def embed_color(weather_code, pm25):
    """날씨/미세먼지 상태에 따른 Discord embed 색상 (10진수)"""
    if pm25 is not None and pm25 > 75:
        return 0xE74C3C  # 빨강 — 매우나쁨
    if pm25 is not None and pm25 > 35:
        return 0xE67E22  # 주황 — 나쁨
    if weather_code in (61, 63, 65, 80, 81, 82):
        return 0x95A5A6  # 회색 — 비
    if weather_code in (71, 73, 75, 77, 85, 86):
        return 0xAED6F1  # 하늘 — 눈
    if weather_code in (95, 96, 99):
        return 0x8E44AD  # 보라 — 뇌우
    if weather_code in (45, 48):
        return 0xBDC3C7  # 연회색 — 안개
    if weather_code == 0:
        return 0xF1C40F  # 노랑 — 맑음
    return 0x3498DB  # 파랑 — 기본


def send_discord(webhook_url, weather_data, aq_data):
    """Discord Embed 메시지 전송"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 날씨 정보 파싱
    w = weather_data.get("current", {}) if weather_data else {}
    code = w.get("weather_code", 0)
    status = WEATHER_CODES.get(code, "알 수 없음")
    temp = w.get("temperature_2m", "N/A")
    feels = w.get("apparent_temperature", "N/A")
    humidity = w.get("relative_humidity_2m", "N/A")
    rain = w.get("precipitation", 0.0)
    wind = w.get("wind_speed_10m", "N/A")

    # 미세먼지 정보 파싱
    a = aq_data.get("current", {}) if aq_data else {}
    pm10 = a.get("pm10")
    pm25 = a.get("pm2_5")
    pm10_str = f"{pm10:.1f} µg/m³  {grade_pm10(pm10)}" if pm10 is not None else "N/A"
    pm25_str = f"{pm25:.1f} µg/m³  {grade_pm25(pm25)}" if pm25 is not None else "N/A"

    payload = {
        "embeds": [
            {
                "title": "🌤 서울 강남구 날씨",
                "color": embed_color(code, pm25),
                "fields": [
                    {"name": "날씨", "value": status, "inline": True},
                    {"name": "기온", "value": f"{temp}°C (체감 {feels}°C)", "inline": True},
                    {"name": "습도", "value": f"{humidity}%", "inline": True},
                    {"name": "강수량", "value": f"{rain} mm", "inline": True},
                    {"name": "풍속", "value": f"{wind} km/h", "inline": True},
                    {"name": "\u200b", "value": "\u200b", "inline": True},
                    {"name": "미세먼지 PM10", "value": pm10_str, "inline": True},
                    {"name": "초미세먼지 PM2.5", "value": pm25_str, "inline": True},
                ],
                "footer": {"text": f"수집 시각: {now}  |  open-meteo.com"},
            }
        ]
    }

    data = json.dumps(payload).encode("utf-8")
    req = Request(webhook_url, data=data, headers={
        "Content-Type": "application/json",
        "User-Agent": "DiscordBot (weather-notifier, 1.0)",
    })
    try:
        with urlopen(req, timeout=10) as resp:
            if resp.status == 204:
                print("Discord 전송 완료.", file=sys.stderr)
            else:
                print(f"Discord 응답 코드: {resp.status}", file=sys.stderr)
    except URLError as e:
        print(f"[오류] Discord 전송 실패: {e}", file=sys.stderr)


def fetch_json(url):
    try:
        with urlopen(url, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except URLError as e:
        print(f"[오류] 네트워크 연결 실패: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"[오류] 데이터 수신 실패: {e}", file=sys.stderr)
        return None


def fetch_weather():
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={LAT}&longitude={LON}"
        f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,"
        f"precipitation,weather_code,wind_speed_10m"
        f"&timezone=Asia%2FSeoul"
    )
    return fetch_json(url)


def fetch_air_quality():
    url = (
        f"https://air-quality-api.open-meteo.com/v1/air-quality"
        f"?latitude={LAT}&longitude={LON}"
        f"&current=pm10,pm2_5"
        f"&timezone=Asia%2FSeoul"
    )
    return fetch_json(url)


def build_report(weather_data, aq_data):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = []
    lines.append("=" * 50)
    lines.append(f"  서울 강남구 날씨 정보  [{now}]")
    lines.append("=" * 50)

    if weather_data and "current" in weather_data:
        c = weather_data["current"]
        code = c.get("weather_code", 0)
        status = WEATHER_CODES.get(code, f"알 수 없음 (코드 {code})")
        temp = c.get("temperature_2m", "N/A")
        feels = c.get("apparent_temperature", "N/A")
        humidity = c.get("relative_humidity_2m", "N/A")
        rain = c.get("precipitation", 0.0)
        wind = c.get("wind_speed_10m", "N/A")

        lines.append(f"  날씨   : {status}")
        lines.append(f"  기온   : {temp}°C  (체감 {feels}°C)")
        lines.append(f"  습도   : {humidity}%")
        lines.append(f"  강수량 : {rain} mm")
        lines.append(f"  풍속   : {wind} km/h")
    else:
        lines.append("  [날씨 정보 수신 실패]")

    lines.append("-" * 50)

    if aq_data and "current" in aq_data:
        c = aq_data["current"]
        pm10 = c.get("pm10")
        pm25 = c.get("pm2_5")

        pm10_str = f"{pm10:.1f} µg/m³" if pm10 is not None else "N/A"
        pm25_str = f"{pm25:.1f} µg/m³" if pm25 is not None else "N/A"

        lines.append(f"  미세먼지 (PM10)   : {pm10_str}  →  {grade_pm10(pm10)}")
        lines.append(f"  초미세먼지(PM2.5) : {pm25_str}  →  {grade_pm25(pm25)}")
    else:
        lines.append("  [미세먼지 정보 수신 실패]")

    lines.append("=" * 50)
    lines.append("")
    return "\n".join(lines)


def main():
    load_env()

    print("날씨 데이터 수집 중...", file=sys.stderr)
    weather = fetch_weather()

    print("미세먼지 데이터 수집 중...", file=sys.stderr)
    air = fetch_air_quality()

    if weather is None and air is None:
        print("[오류] 모든 데이터 수신 실패. 네트워크를 확인하세요.", file=sys.stderr)
        sys.exit(1)

    report = build_report(weather, air)

    # weather.txt에 저장 (append)
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(report)
    print(report)
    print(f"저장 완료: {OUTPUT_FILE}", file=sys.stderr)

    # Discord 전송 (Webhook URL이 설정된 경우에만)
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL", "")
    if webhook_url and not webhook_url.startswith("여기에"):
        print("Discord 전송 중...", file=sys.stderr)
        send_discord(webhook_url, weather, air)
    else:
        print("Discord Webhook URL 미설정 — 전송 건너뜀.", file=sys.stderr)


if __name__ == "__main__":
    main()
