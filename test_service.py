import json
import os

from src.services.employee_service import EmployeeService


def load_local_settings():
    with open("local.settings.json", "r") as file:
        settings = json.load(file)

    for key, value in settings["Values"].items():
        os.environ[key] = value


def main():
    load_local_settings()

    service = EmployeeService()

    try:
        service.create_employee(
            first_name="",
            last_name="Test",
            department_id=1,
            salary=500000,
            bonus=None,
            hire_date="2026-09-07"
        )
    except ValueError as error:
        print("Validation error:", error)


if __name__ == "__main__":
    main()