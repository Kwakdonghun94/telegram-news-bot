import openai
import requests
import schedule
import time
from datetime import datetime
from bs4 import BeautifulSoup

# 텔레그램 봇 토큰과 채팅 ID
BOT_TOKEN = "7908320961:AAGbLze727I4OCZrM30RTs-9kKMAuCjFQHk"
CHAT_ID = "-4646262059"

# 이전 글 저장용 변수 (전역)
last_truth_post = ""
last_tweet = ""

# ✅ 텔레그램 메시지 전송 함수
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=data)
    return response.json()

# ✅ GPT 뉴스 요약 함수
def get_news_summary():
    openai.api_key = "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"
    
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
    return f"[📰 세계 정치·경제 뉴스 요약]\n{summary}"

# ✅ 매일 7시에 뉴스 전송
def daily_news():
    message = get_news_summary()
    send_telegram_message(message)

# ✅ 트루스소셜 확인
def check_truth_social():
    global last_truth_post
    url = "https://truthsocial.com/@realDonaldTrump"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        posts = soup.find_all("div", class_="public-DraftStyleDefault-block")
        if posts:
            latest = posts[0].get_text()
            if latest != last_truth_post:
                last_truth_post = latest
                send_telegram_message(f"[📢 트럼프 TruthSocial 새 글]\n\n{latest}")
    except Exception as e:
        print("TruthSocial 에러:", e)

# ✅ 트위터(Nitter) 확인
def check_twitter():
    global last_tweet
    url = "https://nitter.net/realDonaldTrump"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        tweets = soup.find_all("div", {"class": "tweet-content"})
        if tweets:
            latest = tweets[0].get_text(strip=True)
            if latest != last_tweet:
                last_tweet = latest
                send_telegram_message(f"[🐦 트럼프 트위터 새 글]\n\n{latest}")
    except Exception as e:
        print("트위터 에러:", e)

# ✅ 시작 시 연결 확인
send_telegram_message("✅ 동훈이 봇이 정상적으로 시작되었습니다. 연결 성공!")

# ✅ 스케줄 설정
schedule.every().day.at("07:00").do(daily_news)      # 뉴스
schedule.every(30).minutes.do(check_truth_social)     # TruthSocial 감지
schedule.every(30).minutes.do(check_twitter)          # 트위터 감지

# ✅ 메인 루프
while True:
    schedule.run_pending()
    time.sleep(10)
