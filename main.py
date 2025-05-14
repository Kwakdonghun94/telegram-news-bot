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
    openai.api_key = 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
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "너는 세계 정치·경제 뉴스를 요약해주는 기자야. 오늘자 주요 이슈만 간결하게 정리해줘. 3~5줄로."
            },
            {
                "role": "user",
                "content": "오늘 세계 정치 및 경제 뉴스를 요약해줘"
            }
        ],
        temperature=0.5,
        max_tokens=500
    )

    summary = response["choices"][0]["message"]["content"]
    return f"[세계 정치·경제 뉴스 요약]\n{summary}"

def main():
    now = datetime.now()
    if now.hour == 7:
        message = get_news_summary()
        send_telegram_message(message)

if __name__ == "__main__":
    main()
