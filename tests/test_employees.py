import pytest
from src.services.employee_service import EmployeeService


def test_get_employee_invalid_id():
    service = EmployeeService()

    with pytest.raises(ValueError):
        service.get_employee(0)


def test_get_employees_invalid_department_id():
    service = EmployeeService()

    with pytest.raises(ValueError):
        service.get_employees(0)


def test_create_employee_missing_required_field():
    service = EmployeeService()

    data = {
        "first_name": "Test",
        "last_name": "User",
        "department_id": 1,
        "salary": 800000
        # hire_date missing
    }

    with pytest.raises(ValueError):
        service.create_employee(data)


def test_create_employee_negative_salary():
    service = EmployeeService()

    data = {
        "first_name": "Test",
        "last_name": "User",
        "department_id": 1,
        "salary": -100,
        "bonus": None,
        "hire_date": "2025-01-01"
    }

    with pytest.raises(ValueError):
        service.create_employee(data)