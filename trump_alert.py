import requests
import time
import schedule
from bs4 import BeautifulSoup

BOT_TOKEN = "7908320961:AAGbLze727I4OCZrM30RTs-9kKMAuCjFQHk"
CHAT_ID = "-4646262059"

last_trump_posts = {
    "twitter": "",
    "truthsocial": ""
}

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)

def check_trump_twitter():
    url = "https://nitter.net/realDonaldTrump"
    try:
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        post = soup.select_one("div.timeline-item .tweet-content").text.strip()

        if post != last_trump_posts["twitter"]:
            last_trump_posts["twitter"] = post
            send_telegram_message(f"📢 [트위터 새 게시글]\n{post}")
    except Exception as e:
        print("트위터 확인 오류:", e)

def check_trump_truthsocial():
    url = "https://truthsocial.com/@realDonaldTrump"
    try:
        html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).text
        soup = BeautifulSoup(html, "html.parser")
        content_tags = soup.find_all("div", {"class": "post-body"})
        if not content_tags:
            return
        post = content_tags[0].text.strip()

        if post != last_trump_posts["truthsocial"]:
            last_trump_posts["truthsocial"] = post
            send_telegram_message(f"📢 [Truth Social 새 게시글]\n{post}")
    except Exception as e:
        print("Truth Social 확인 오류:", e)

def main():
    check_trump_twitter()
    check_trump_truthsocial()

schedule.every(30).minutes.do(main)

send_telegram_message("✅ 트럼프 새 게시글 감시 봇 시작됨 (30분 간격)")

while True:
    schedule.run_pending()
    time.sleep(1)
