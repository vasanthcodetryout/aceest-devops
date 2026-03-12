# app.py — ACEest Fitness & Gym | Flask Web API
# Converted from Tkinter desktop app to Flask REST API for DevOps pipeline
# Author: [Your Name] | Course: Introduction to DevOps (CSIZG514)

from flask import Flask, jsonify, request

app = Flask(__name__)

# =============================================================================
# DATA STORE
# Mirrors the programs dictionary from your Tkinter versions (ver 1.1 onwards)
# In production this would be a database (like your SQLite in ver 2.0+)
# For this assignment, in-memory store keeps things simple and testable
# =============================================================================

PROGRAMS = {
    "Fat Loss (FL)": {
        "workout": (
            "Mon: Back Squat 5x5 + Core | "
            "Tue: EMOM 20min Assault Bike | "
            "Wed: Bench Press + 21-15-9 | "
            "Thu: Deadlift + Box Jumps | "
            "Fri: Zone 2 Cardio 30min"
        ),
        "diet": (
            "Breakfast: Egg Whites + Oats | "
            "Lunch: Grilled Chicken + Brown Rice | "
            "Dinner: Fish Curry + Millet Roti | "
            "Target: ~2000 kcal"
        ),
        "calorie_factor": 22
    },
    "Muscle Gain (MG)": {
        "workout": (
            "Mon: Squat 5x5 | "
            "Tue: Bench 5x5 | "
            "Wed: Deadlift 4x6 | "
            "Thu: Front Squat 4x8 | "
            "Fri: Incline Press 4x10 | "
            "Sat: Barbell Rows 4x10"
        ),
        "diet": (
            "Breakfast: Eggs + Peanut Butter Oats | "
            "Lunch: Chicken Biryani | "
            "Dinner: Mutton Curry + Rice | "
            "Target: ~3200 kcal"
        ),
        "calorie_factor": 35
    },
    "Beginner (BG)": {
        "workout": (
            "Full Body Circuit: Air Squats, Ring Rows, Push-ups | "
            "Focus: Technique & Consistency"
        ),
        "diet": (
            "Balanced Tamil Meals: Idli/Dosa, Rice + Dal | "
            "Protein Target: 120g/day"
        ),
        "calorie_factor": 26
    }
}

# In-memory client list (resets on server restart — fine for testing)
clients = []


# =============================================================================
# ROUTE 1 — Health Check / Home
# =============================================================================

@app.route("/", methods=["GET"])
def home():
    """
    Health check endpoint.
    Used by Docker, Jenkins, and GitHub Actions to verify the app is running.
    """
    return jsonify({
        "message": "ACEest Fitness API is running!",
        "status": "ok",
        "version": "1.0.0"
    }), 200


# =============================================================================
# ROUTE 2 — Get All Programs
# =============================================================================

@app.route("/programs", methods=["GET"])
def get_programs():
    """
    Returns all available fitness program names.
    Equivalent to the Combobox values in your Tkinter UI.
    """
    return jsonify({
        "programs": list(PROGRAMS.keys()),
        "count": len(PROGRAMS)
    }), 200


# =============================================================================
# ROUTE 3 — Get One Program by Name
# =============================================================================

@app.route("/program/<string:name>", methods=["GET"])
def get_program(name):
    """
    Returns workout + diet details for a specific program.
    Equivalent to update_display() / update_program() in your Tkinter versions.

    Example: GET /program/Fat Loss (FL)
    """
    if name not in PROGRAMS:
        return jsonify({"error": f"Program '{name}' not found"}), 404

    return jsonify({
        "program": name,
        "details": PROGRAMS[name]
    }), 200


# =============================================================================
# ROUTE 4 — Get All Clients
# =============================================================================

@app.route("/clients", methods=["GET"])
def get_clients():
    """
    Returns the full list of saved clients.
    Equivalent to the Client List Treeview in ver 1.1.2.
    """
    return jsonify({
        "clients": clients,
        "count": len(clients)
    }), 200


# =============================================================================
# ROUTE 5 — Add a New Client
# =============================================================================

@app.route("/clients", methods=["POST"])
def add_client():
    """
    Saves a new client profile.
    Equivalent to save_client() in all your Tkinter versions.

    Expected JSON body:
    {
        "name": "Arjun",
        "age": 28,
        "weight": 75.5,
        "program": "Muscle Gain (MG)"
    }
    """
    data = request.get_json()

    # Validate required fields
    if not data:
        return jsonify({"error": "Request body is required"}), 400
    if "name" not in data or not data["name"].strip():
        return jsonify({"error": "Client name is required"}), 400
    if "program" not in data:
        return jsonify({"error": "Program is required"}), 400
    if data["program"] not in PROGRAMS:
        return jsonify({"error": f"Invalid program. Choose from: {list(PROGRAMS.keys())}"}), 400

    # Calculate calories (same formula as your Tkinter calorie_factor logic)
    weight = data.get("weight", 0)
    factor = PROGRAMS[data["program"]]["calorie_factor"]
    calories = int(weight * factor) if weight > 0 else 0

    client = {
        "name":     data["name"].strip(),
        "age":      data.get("age", 0),
        "weight":   weight,
        "program":  data["program"],
        "calories": calories
    }

    clients.append(client)

    return jsonify({
        "message": f"Client '{client['name']}' saved successfully",
        "client": client
    }), 201


# =============================================================================
# ROUTE 6 — Calorie Calculator
# =============================================================================

@app.route("/calories", methods=["GET"])
def calculate_calories():
    """
    Calculates daily calorie target given weight and program.
    Equivalent to the calorie_label calculation in your Tkinter versions.

    Example: GET /calories?weight=80&program=Fat Loss (FL)
    """
    weight  = request.args.get("weight",  type=float)
    program = request.args.get("program", type=str)

    if weight is None or weight <= 0:
        return jsonify({"error": "Valid weight (kg) is required"}), 400
    if not program or program not in PROGRAMS:
        return jsonify({"error": f"Valid program is required. Options: {list(PROGRAMS.keys())}"}), 400

    calories = int(weight * PROGRAMS[program]["calorie_factor"])

    return jsonify({
        "weight_kg":      weight,
        "program":        program,
        "calories_kcal":  calories,
        "calorie_factor": PROGRAMS[program]["calorie_factor"]
    }), 200


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    # host="0.0.0.0" makes the app accessible from outside the container
    app.run(host="0.0.0.0", port=5000, debug=True)
