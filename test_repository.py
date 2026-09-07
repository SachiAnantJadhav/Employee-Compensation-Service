import json
import os

from src.repositories.employee_repository import EmployeeRepository


def load_local_settings():
    with open("local.settings.json", "r") as file:
        settings = json.load(file)

    for key, value in settings["Values"].items():
        os.environ[key] = value


def main():
    load_local_settings()

    repository = EmployeeRepository()
    
    employee_id = repository.create_employee(
        first_name="Test",
        last_name="Employee",
        department_id=1,
        salary=750000,
        bonus=50000,
        hire_date="2026-09-07"
    )

    success = repository.update_employee(
        employee_id=employee_id,
        first_name="Updated",
        last_name="Employee",
        department_id=2,
        salary=800000,
        bonus=75000,
        hire_date="2026-09-07"
    )

    success = repository.delete_employee(employee_id)

    print("Deleted:", success)


if __name__ == "__main__":
    main()