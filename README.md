# Pokémon TCG Checker

Deze webapp checkt regelmatig de Pokémon Center UK site op nieuwe TCG-producten en stuurt een Telegrammelding bij een update.

## 🎯 Deploy instructies (Render.com)

1. Maak een nieuwe *Web Service* aan op Render.
2. Verbind een GitHub-repo met bovenstaande structuur.
3. Build command:  
   pip install -r requirements.txt
4. Start command:  
   python app.py
5. Na uitrollen is de app beschikbaar op jouw Render‑URL.

## ⚙️ Configuratie aanpassen
- BOT_TOKEN en CHAT_ID in app.py kun je aanpassen naar jouw gegevens.
- CHECK_INTERVAL bepaalt hoe vaak automatisch wordt gecontroleerd (in seconden).

## 🚀 Gebruik
- Open de Render‑URL in je browser.
- Klik op *“Check nu”* om direct te controleren.
- Bij nieuwe producten ontvang je automatisch een Telegram‑bericht.


