import requests
import streamlit as st


API_BASE_URL = st.secrets["API_BASE_URL"]
FUNCTION_KEY = st.secrets["FUNCTION_KEY"]


def get_headers():
    return {
        "x-functions-key": FUNCTION_KEY
    }


def handle_response(response):
    if response.status_code >= 400:
        try:
            error_data = response.json()
            message = error_data.get("error", "An error occurred.")
        except Exception:
            message = response.text or "An error occurred."

        raise RuntimeError(message)

    if response.status_code == 204:
        return None

    return response.json()


# -------------------------
# Employee APIs
# -------------------------

def create_employee(data):
    response = requests.post(
        f"{API_BASE_URL}/api/employees",
        json=data,
        headers=get_headers(),
        timeout=30
    )

    return handle_response(response)


def get_employee(employee_id):
    response = requests.get(
        f"{API_BASE_URL}/api/employees/{employee_id}",
        headers=get_headers(),
        timeout=30
    )

    return handle_response(response)


def get_employees(department_id=None):
    url = f"{API_BASE_URL}/api/employees"

    params = {}

    if department_id is not None:
        params["department_id"] = department_id

    response = requests.get(
        url,
        params=params,
        headers=get_headers(),
        timeout=30
    )

    return handle_response(response)


def update_employee(employee_id, data):
    response = requests.put(
        f"{API_BASE_URL}/api/employees/{employee_id}",
        json=data,
        headers=get_headers(),
        timeout=30
    )

    return handle_response(response)


def delete_employee(employee_id):
    response = requests.delete(
        f"{API_BASE_URL}/api/employees/{employee_id}",
        headers=get_headers(),
        timeout=30
    )

    return handle_response(response)


# -------------------------
# Compensation Reports
# -------------------------

def get_total_bonus():
    response = requests.get(
        f"{API_BASE_URL}/api/reports/total-bonus",
        headers=get_headers(),
        timeout=30
    )

    return handle_response(response)


def get_employees_without_bonus():
    response = requests.get(
        f"{API_BASE_URL}/api/reports/no-bonus",
        headers=get_headers(),
        timeout=30
    )

    return handle_response(response)


def get_bonus_percentage():
    response = requests.get(
        f"{API_BASE_URL}/api/reports/bonus-percentage",
        headers=get_headers(),
        timeout=30
    )

    return handle_response(response)


def get_high_bonus_departments():
    response = requests.get(
        f"{API_BASE_URL}/api/reports/high-bonus-departments",
        headers=get_headers(),
        timeout=30
    )

    return handle_response(response)


def get_bonus_ranking():
    response = requests.get(
        f"{API_BASE_URL}/api/reports/bonus-ranking",
        headers=get_headers(),
        timeout=30
    )

    return handle_response(response)


def get_highest_salary():
    response = requests.get(
        f"{API_BASE_URL}/api/reports/highest-salary",
        headers=get_headers(),
        timeout=30
    )

    return handle_response(response)

def patch_employee(employee_id, data):
    response = requests.patch(
        f"{API_BASE_URL}/api/employees/{employee_id}",
        headers=get_headers(),
        json=data,
        timeout=30,
    )

    return handle_response(response)