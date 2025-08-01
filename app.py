from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup
import json
import threading
import time

app = Flask(_name_)

BOT_TOKEN = '8226538789:AAHnQMsRjXCdTNKjemzrpZSyzcfNk25Mo24'
CHAT_ID = '6220229197'
URL = 'https://www.pokemoncenter.com/en-gb/category/new-releases?category=uk-trading-card-game'
CHECK_INTERVAL = 120  # seconden

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def fetch_products():
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    product_divs = soup.select('.product-card__title')
    products = [div.get_text(strip=True) for div in product_divs]
    return products

def load_previous():
    try:
        with open('products.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_current(products):
    with open('products.json', 'w') as f:
        json.dump(products, f)

def check_for_updates():
    current_products = fetch_products()
    previous_products = load_previous()

    new_items = [item for item in current_products if item not in previous_products]

    if new_items:
        message = "🆕 Nieuwe TCG-producten gevonden op Pokémon Center:\n\n"
        message += "\n".join(f"- {item}" for item in new_items)
        send_telegram_message(message)
        save_current(current_products)
        return new_items
    return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check')
def check():
    new_items = check_for_updates()
    if new_items:
        return jsonify({"new_items": new_items})
    else:
        return jsonify({"new_items": []})

def scheduled_check():
    while True:
        check_for_updates()
        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    thread = threading.Thread(target=scheduled_check, daemon=True)
    thread.start()
    app.run(host='0.0.0.0', port=5000)
