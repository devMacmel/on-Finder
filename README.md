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
