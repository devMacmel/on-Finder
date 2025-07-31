# ===================== START =====================
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from config import ADMIN_PASSWORD, ADMIN_USERNAME
from dotenv import load_dotenv
import json
from db import *
from wa import send_interactive_menu, send_message
from datetime import datetime

load_dotenv()
app = Flask(__name__)
app.secret_key = "Secret"
init_db()

user_states = {}
bus_locations = {}
VERIFY_TOKEN = "" #set coustom token 

# ===================== WHATSAPP BOT =====================
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print("WEBHOOK_VERIFIED")
            return challenge, 200
        else:
            return "Verification token mismatch", 403

    elif request.method == 'POST':
        data = request.get_json()
        print("Incoming WhatsApp Data:", json.dumps(data, indent=2))

        if data.get("entry"):
            for entry in data["entry"]:
                for change in entry["changes"]:
                    value = change.get("value", {})
                    messages = value.get("messages")
                    if messages:
                        msg_data = messages[0]
                        user_id = msg_data["from"]
                        msg_type = msg_data.get("type", "")
                        msg = ""

                        if msg_type == "text":
                            msg = msg_data["text"]["body"].strip().lower()
                        elif msg_type == "interactive":
                            interactive_type = msg_data["interactive"]["type"]
                            if interactive_type == "button_reply":
                                msg = msg_data["interactive"]["button_reply"]["id"]
                            elif interactive_type == "list_reply":
                                msg = msg_data["interactive"]["list_reply"]["id"]
                            print("✅ Raw msg:", repr(msg))
                            print("✅ msg type:", type(msg))

                        if msg == "locate_bus":
                            user_states[user_id] = "awaiting_loc"
                            send_message(user_id, "Please enter your bus no:")
                        elif msg == "route_bus":
                            user_states[user_id] = "awaiting_route"
                            send_message(user_id, "Please enter your bus no:")
                        elif msg == "hi":
                            send_interactive_menu(user_id)
                        elif user_states.get(user_id) == "awaiting_loc":
                            bus_no = msg
                            send_message(user_id, f"📍 Live location of bus no : {bus_no}\n----------------------------------------------\n\n"
                                                  f"https://dummy.com/map?bus_no={bus_no}")
                            send_interactive_menu(user_id)
                            user_states[user_id] = None
                        elif user_states.get(user_id) == "awaiting_route":
                            bus_no = msg
                            route_info = get_route(bus_no)
                            if route_info:
                                route, departure, return_time = route_info
                                send_message(user_id, f"🚌 Bus No : {bus_no} \n--------------------------\nRoute: {route}\n\n--------------------------\n\n➡️ Departure: {departure}\n⬅️ Return: {return_time}")
                            else:
                                send_message(user_id, "❌ No route information found for this bus.")
                            send_interactive_menu(user_id)
                            user_states[user_id] = None
        


        return "EVENT_RECEIVED", 200

# ===================== GPS =====================
@app.route('/update_location', methods=['POST'])
def update_location():
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'No JSON received'}), 400

    bus = data.get('device_id')
    lat = data.get('location', {}).get('coords', {}).get('latitude')
    lon = data.get('location', {}).get('coords', {}).get('longitude')

    print("Bus:", bus, "Lat:", lat, "Lon:", lon)

    if not all([bus, lat, lon]):
        return jsonify({'status': 'error', 'message': 'Missing values'}), 400

    bus_locations[bus] = (lat, lon, datetime.now())
    return jsonify({'status': 'success', 'message': f'Location updated for {bus}'}), 200

# ===================== MAP PAGE =====================
@app.route("/map")
def map_page():
    bus_no = request.args.get("bus_no")
    if not bus_no:
        return "Missing Bus Number", 400
    return render_template("map.html", bus_no=bus_no)

def get_location(bus_no):
    return bus_locations.get(bus_no)

@app.route("/api/bus-location")
def bus_location_api():
    bus_no = request.args.get("bus_no")
    if not bus_no:
        return jsonify({"error": "Missing bus number"}), 400
    loc = get_location(bus_no)
    if not loc:
        return jsonify({"error": "Bus not found"}), 404
    lat, lon, last_updated = loc
    return jsonify({
        "lat": lat,
        "lon": lon,
        "updated": last_updated.strftime("%d-%m-%Y %H:%M:%S")
    })

# ===================== ADMIN PANEL =====================
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form["username"] == ADMIN_USERNAME and request.form["password"] == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin_home"))
        return "Invalid credentials"
    return render_template("login.html")

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login"))

@app.route("/admin")
def admin_home():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    buses = get_all()
    return render_template("index.html", buses=buses)

@app.route("/admin/add", methods=["GET", "POST"])
def admin_add():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    if request.method == "POST":
        add_bus(request.form["bus_no"], request.form["route"], request.form["departure"], request.form["return_time"])
        return redirect(url_for("admin_home"))
    return render_template("bus.html", bus=None)

@app.route("/admin/edit/<bus_no>", methods=["GET", "POST"])
def admin_edit(bus_no):
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    if request.method == "POST":
        update_bus(bus_no, request.form["route"], request.form["departure"], request.form["return_time"])
        return redirect(url_for("admin_home"))
    route = get_route(bus_no)
    return render_template("bus.html", bus=(bus_no, *route) if route else None)

@app.route("/admin/delete/<bus_no>", methods=["GET", "POST"])
def admin_delete(bus_no):
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    delete_bus(bus_no)
    return redirect(url_for("admin_home"))

# ===================== MAIN =====================
if __name__ == '__main__':
    app.run(debug=True)

# ===================== END OF CODE =====================
