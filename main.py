import requests
from datetime import datetime

# 텔레그램 봇 토큰과 채팅 ID 직접 삽입
BOT_TOKEN = "7908320961:AAGbLze727I4OCZrM30RTs-9kKMAuCjFQHk"
CHAT_ID = "-4646262059"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=data)
    return response.json()

def get_news_summary():
    # 여기에 뉴스 요약 API나 GPT 요약 로직을 넣을 수 있음
    return "[세계 정치·경제 뉴스 요약]\n- 경제: 미국 금리 동결 가능성\n- 정치: 미중 무역 회담 다음 주 개최\n- 사건: 중동 분쟁 격화 가능성"

def main():
    now = datetime.now()
    if now.hour == 7:
        message = get_news_summary()
        send_telegram_message(message)

if __name__ == "__main__":
    main()
