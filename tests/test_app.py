# tests/test_app.py — ACEest Fitness & Gym | Pytest Test Suite
# Tests every route and edge case in app.py
# Run with:  pytest tests/ -v

import pytest
from app import app, clients, PROGRAMS


# =============================================================================
# FIXTURE — creates a test client that mimics a real HTTP browser/curl call
# Flask's test client lets us call routes without starting a real server
# =============================================================================

@pytest.fixture
def client():
    """
    Sets up Flask in TESTING mode and provides a test HTTP client.
    The 'clients' list is cleared before each test so tests don't interfere.
    """
    app.config["TESTING"] = True
    clients.clear()          # reset in-memory store before every test
    with app.test_client() as c:
        yield c


# =============================================================================
# TEST GROUP 1 — Home / Health Check  (Route: GET /)
# =============================================================================

class TestHome:

    def test_home_status_200(self, client):
        """App must return HTTP 200 on home route."""
        response = client.get("/")
        assert response.status_code == 200

    def test_home_returns_json(self, client):
        """Response must be JSON."""
        response = client.get("/")
        assert response.content_type == "application/json"

    def test_home_message(self, client):
        """JSON body must confirm app is running."""
        data = client.get("/").get_json()
        assert data["status"] == "ok"
        assert "ACEest" in data["message"]

    def test_home_has_version(self, client):
        """Version field must be present."""
        data = client.get("/").get_json()
        assert "version" in data


# =============================================================================
# TEST GROUP 2 — Programs List  (Route: GET /programs)
# =============================================================================

class TestPrograms:

    def test_get_programs_status_200(self, client):
        response = client.get("/programs")
        assert response.status_code == 200

    def test_all_three_programs_returned(self, client):
        data = client.get("/programs").get_json()
        assert "Fat Loss (FL)"   in data["programs"]
        assert "Muscle Gain (MG)" in data["programs"]
        assert "Beginner (BG)"   in data["programs"]

    def test_program_count_is_three(self, client):
        data = client.get("/programs").get_json()
        assert data["count"] == 3


# =============================================================================
# TEST GROUP 3 — Single Program Detail  (Route: GET /program/<name>)
# =============================================================================

class TestProgramDetail:

    def test_valid_fat_loss_program(self, client):
        response = client.get("/program/Fat Loss")
        assert response.status_code == 200

    def test_valid_muscle_gain_program(self, client):
        response = client.get("/program/Muscle Gain")
        assert response.status_code == 200

    def test_valid_beginner_program(self, client):
        response = client.get("/program/Beginner (BG)")
        assert response.status_code == 200

    def test_program_has_workout_field(self, client):
        data = client.get("/program/Fat Loss (FL)").get_json()
        assert "workout" in data["details"]

    def test_program_has_diet_field(self, client):
        data = client.get("/program/Fat Loss (FL)").get_json()
        assert "diet" in data["details"]

    def test_program_has_calorie_factor(self, client):
        data = client.get("/program/Fat Loss (FL)").get_json()
        assert "calorie_factor" in data["details"]

    def test_fat_loss_calorie_factor_is_22(self, client):
        data = client.get("/program/Fat Loss (FL)").get_json()
        assert data["details"]["calorie_factor"] == 22

    def test_muscle_gain_calorie_factor_is_35(self, client):
        data = client.get("/program/Muscle Gain (MG)").get_json()
        assert data["details"]["calorie_factor"] == 35

    def test_invalid_program_returns_404(self, client):
        response = client.get("/program/InvalidProgram")
        assert response.status_code == 404

    def test_invalid_program_error_message(self, client):
        data = client.get("/program/DoesNotExist").get_json()
        assert "error" in data


# =============================================================================
# TEST GROUP 4 — Add & Get Clients  (Routes: POST /clients, GET /clients)
# =============================================================================

class TestClients:

    def _valid_payload(self):
        """Helper: returns a valid client payload."""
        return {
            "name":    "Arjun Kumar",
            "age":     28,
            "weight":  75.0,
            "program": "Muscle Gain (MG)"
        }

    def test_add_client_returns_201(self, client):
        response = client.post("/clients", json=self._valid_payload())
        assert response.status_code == 201

    def test_add_client_name_in_response(self, client):
        data = client.post("/clients", json=self._valid_payload()).get_json()
        assert data["client"]["name"] == "Arjun Kumar"

    def test_add_client_calories_calculated(self, client):
        """75kg × 35 factor = 2625 kcal for Muscle Gain."""
        data = client.post("/clients", json=self._valid_payload()).get_json()
        assert data["client"]["calories"] == 75 * 35

    def test_add_client_fat_loss_calories(self, client):
        """80kg × 22 factor = 1760 kcal for Fat Loss."""
        payload = {"name": "Priya", "weight": 80, "program": "Fat Loss (FL)"}
        data = client.post("/clients", json=payload).get_json()
        assert data["client"]["calories"] == 80 * 22

    def test_add_client_missing_name_returns_400(self, client):
        response = client.post("/clients", json={"program": "Beginner (BG)"})
        assert response.status_code == 400

    def test_add_client_missing_program_returns_400(self, client):
        response = client.post("/clients", json={"name": "Test User"})
        assert response.status_code == 400

    def test_add_client_invalid_program_returns_400(self, client):
        response = client.post("/clients", json={"name": "Test", "program": "InvalidProg"})
        assert response.status_code == 400

    def test_add_client_empty_body_returns_400(self, client):
        response = client.post("/clients", json={})
        assert response.status_code == 400

    def test_get_clients_empty_initially(self, client):
        data = client.get("/clients").get_json()
        assert data["count"] == 0
        assert data["clients"] == []

    def test_get_clients_after_adding_one(self, client):
        client.post("/clients", json=self._valid_payload())
        data = client.get("/clients").get_json()
        assert data["count"] == 1

    def test_get_clients_after_adding_two(self, client):
        client.post("/clients", json=self._valid_payload())
        client.post("/clients", json={"name": "Meena", "weight": 60, "program": "Beginner (BG)"})
        data = client.get("/clients").get_json()
        assert data["count"] == 2


# =============================================================================
# TEST GROUP 5 — Calorie Calculator  (Route: GET /calories)
# =============================================================================

class TestCalories:

    def test_calorie_calculation_fat_loss(self, client):
        response = client.get("/calories?weight=80&program=Fat Loss (FL)")
        assert response.status_code == 200
        data = response.get_json()
        assert data["calories_kcal"] == 80 * 22

    def test_calorie_calculation_muscle_gain(self, client):
        response = client.get("/calories?weight=70&program=Muscle Gain (MG)")
        data = response.get_json()
        assert data["calories_kcal"] == 70 * 35

    def test_calorie_calculation_beginner(self, client):
        response = client.get("/calories?weight=65&program=Beginner (BG)")
        data = response.get_json()
        assert data["calories_kcal"] == 65 * 26

    def test_calorie_missing_weight_returns_400(self, client):
        response = client.get("/calories?program=Fat Loss (FL)")
        assert response.status_code == 400

    def test_calorie_missing_program_returns_400(self, client):
        response = client.get("/calories?weight=70")
        assert response.status_code == 400

    def test_calorie_invalid_program_returns_400(self, client):
        response = client.get("/calories?weight=70&program=BadProgram")
        assert response.status_code == 400

    def test_calorie_response_has_all_fields(self, client):
        data = client.get("/calories?weight=75&program=Beginner (BG)").get_json()
        assert "weight_kg"      in data
        assert "program"        in data
        assert "calories_kcal"  in data
        assert "calorie_factor" in data
