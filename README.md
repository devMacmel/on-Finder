# 🚌 Bus Location & Route Info Bot (WhatsApp-Based)

A lightweight Python + Flask-based WhatsApp chatbot for tracking real-time bus locations and viewing route info, departure, and return timings. Integrated with **Traccar GPS client** for location updates and uses **SQLite** for backend data management.

> 📱 Designed for educational institutions or small fleets to help students/staff track bus status easily through WhatsApp.

---

## 🚀 Features

- 📍 Real-time bus location tracking (via Traccar client)
- 🗺️ Retrieve route, departure, and return times by bus number
- 🛠️ Easy admin-side data updates (routes + locations)

---

## 📦 Folder Structure
on-Finder/                                                                                 
│── app.py                                                                                 
│── db.py                                                                                 
│── whatsapp.py                                                                                 
│── config.py                                                                                 
│── requirements.txt                                                                                 
│── templates/                                                                                 
│   ├── login.html                                                                                 
│   ├── index.html                                                                                 
│   ├── edit_bus.html                                                                                 
│   ├── map.html                                                                                 
│   └── style.css                                                                                 
│── .env (create manually)                                                                                 
│── buses.db (auto-created)                                                                                 

---

## 🧠 How It Works

### User Flow:
1. User messages the bot → shown menu:
2. 👋 Welcome! Choose an option:
   1️⃣ View Bus Location
   2️⃣ Bus Route & Timings
2. User sends `1` → asked for bus number → replies with location and last updated time.
3. User sends `2` → asked for bus number → replies with:
   🚌 Route: <Route Info>
   ⏱️ Departure: <Time>
   🔁 Return: <Time>
4. After each operation, bot resets to main menu.

### GPS Updates:
- A Traccar GPS client installed in the bus sends location updates to the backend.
- These are stored in the SQLite DB and used when users request location info.

---

🛠️ Admin Functions
Use these functions from db.py in a Python script or admin panel:
                                                                                                                                                            
- add_bus(bus_no, route, departure, return_time)
- update_location(bus_no, longitude, latitude)                                                                                 
You can integrate Traccar GPS client to periodically send updates to this.
                                                                                 
---
📅 Future Plans                                                                       

✨ Revamp Admin Page UI

🔐 Enhanced Security (login, CSRF protection)

⚡ Performance Optimizations (caching, DB indexing)

📡 IoT Support for GPS modules on buses


## ⚙️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/bus-tracker-bot.git
cd bus-tracker-bot
pip install -r requirements.txt
python -c "from db import init_db; init_db()"
python app.py
```
🧪 WhatsApp Cloud API Setup
Go to Meta Developer Portal.

Create a WhatsApp app and configure webhook URL (https://<yourdomain>/webhook) and verify token.

Use Postman or webhook test messages to trigger the bot.

Make sure your endpoint is accessible (e.g., via Render, Heroku, or ngrok).

---
