from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup
import json
import os

app = Flask(__name__)

PRODUCTS_FILE = 'products.json'
URL = 'https://www.pokemoncenter.com/en-gb/category/new-releases?category=uk-trading-card-game'
CHECK_INTERVAL = 120  # seconden

BOT_TOKEN = '8226538789:AAHnQMsRjXCdTNKjemzrpZSyzcfNk25Mo24'
CHAT_ID = '6220229197'


def fetch_products():
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all('a', class_='product-card-title')
    return [item.text.strip() for item in items]


def load_previous_products():
    if not os.path.exists(PRODUCTS_FILE):
        return []
    with open(PRODUCTS_FILE, 'r') as f:
        return json.load(f)


def save_products(products):
    with open(PRODUCTS_FILE, 'w') as f:
        json.dump(products, f)


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    requests.post(url, data=payload)


def check_for_updates():
    current_products = fetch_products()
    previous_products = load_previous_products()

    new_items = [item for item in current_products if item not in previous_products]

    if new_items:
        save_products(current_products)
        message = "🆕 Nieuwe TCG-producten gevonden op Pokémon Center:\n\n"
        message += "\n".join(f"- {item}" for item in new_items)
        send_telegram_message(message)

    return new_items


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/check')
def manual_check():
    new_items = check_for_updates()
    return jsonify({'new_items': new_items})


if __name__ == '__main__':
    app.run(debug=True)
