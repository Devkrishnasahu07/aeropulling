import os
import random
import io
import base64
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify

import backend
import vision

# Initialize Flask App
app = Flask(__name__)

# Initialize Database on Start
try:
    backend.init_db()
except Exception as e:
    print(f"Database Initialization Note: {e}")

@app.route("/")
def index():
    """Serves the main AeroPool web interface."""
    return render_template("index.html")

@app.route("/api/analyze-luggage", methods=["POST"])
def analyze_luggage_api():
    """Analyzes luggage image via OpenCV Computer Vision module."""
    try:
        data = request.get_json() or {}
        image_base64 = data.get("image_data")
        
        if not image_base64:
            return jsonify({"success": False, "error": "No image data provided"}), 400

        # Decode base64 image data
        if "," in image_base64:
            image_base64 = image_base64.split(",")[1]
            
        img_bytes = base64.b64decode(image_base64)
        img_file = io.BytesIO(img_bytes)

        # Run OpenCV vision analysis
        luggage_size, luggage_units, surcharge = vision.analyze_luggage(img_file)

        return jsonify({
            "success": True,
            "luggage_size": luggage_size,
            "luggage_units": luggage_units,
            "surcharge": surcharge
        })
    except Exception as e:
        return jsonify({
            "success": True,
            "luggage_size": "Medium",
            "luggage_units": 2,
            "surcharge": 40.0,
            "note": f"Fallback parameters applied: {str(e)}"
        })

@app.route("/api/book", methods=["POST"])
def book_ride_api():
    """Processes ride booking & queries dual-marketplace SQLite matchmaker."""
    try:
        data = request.get_json() or {}
        dropoff_zone = data.get("dropoff_zone")
        is_shared = data.get("is_shared", True)
        
        if not dropoff_zone:
            return jsonify({"success": False, "error": "Drop-off zone is required."}), 400

        passenger_name = f"Traveler-{random.randint(100, 999)}"
        luggage_size = "Medium"

        # If image data is provided, analyze luggage size for DB record
        image_base64 = data.get("image_data")
        if image_base64:
            try:
                if "," in image_base64:
                    image_base64 = image_base64.split(",")[1]
                img_bytes = base64.b64decode(image_base64)
                img_file = io.BytesIO(img_bytes)
                luggage_size, _, _ = vision.analyze_luggage(img_file)
            except Exception:
                pass

        # Save to DB & trigger dual-marketplace matchmaker
        request_id = backend.add_ride_request(passenger_name, dropoff_zone, luggage_size, is_shared)
        db_match_status = backend.find_match(dropoff_zone)

        booking_code = f"RAPID-{''.join(random.choices('123456789ABCDEF', k=5))}"
        eta = (datetime.now() + timedelta(minutes=5)).strftime("%I:%M %p")

        return jsonify({
            "success": True,
            "booking_code": booking_code,
            "eta": eta,
            "request_id": request_id,
            "db_status": db_match_status
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/driver-log", methods=["POST"])
def driver_log_api():
    """Processes daily driver verification photos and activates driver profile."""
    try:
        data = request.get_json() or {}
        driver_id = data.get("driver_id", 1)
        interior_img = data.get("interior_img", "interior_verified.jpg")
        exterior_img = data.get("exterior_img", "exterior_verified.jpg")

        result = backend.process_daily_driver_log(driver_id, interior_img, exterior_img)
        return jsonify({"success": True, "message": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
