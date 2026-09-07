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
        
def test_create_employee_with_bonus():
    service = EmployeeService()
    data = {
        "first_name": "Test",
        "last_name": "Bonus",
        "department_id": 1,
        "salary": 800000,
        "bonus": 50000,
        "hire_date": "2026-09-07"
    }

    employee_id = service.create_employee(data)["employee_id"]

    employee = service.get_employee(employee_id)

    assert employee["bonus"] == 50000
    
def test_create_employee_with_zero_bonus():
    service = EmployeeService()
    data = {
        "first_name": "Test",
        "last_name": "Zero",
        "department_id": 1,
        "salary": 800000,
        "bonus": 0,
        "hire_date": "2026-09-07"
    }

    employee = service.create_employee(data)

    assert employee["bonus"] == 0
    
def test_create_employee_without_bonus_uses_five_percent():
    service = EmployeeService()
    data = {
        "first_name": "Test",
        "last_name": "Default",
        "department_id": 1,
        "salary": 800000,
        "hire_date": "2026-09-07"
    }

    employee = service.create_employee(data)

    assert employee["bonus"] == 40000
    
def test_create_employee_with_null_bonus():
    service = EmployeeService()
    data = {
        "first_name": "Test",
        "last_name": "Null",
        "department_id": 1,
        "salary": 800000,
        "bonus": None,
        "hire_date": "2026-09-07"
    }

    employee = service.create_employee(data)

    assert employee["bonus"] == 0
    
def test_patch_employee_salary():
    service = EmployeeService()
    employee = service.create_employee({
        "first_name": "Patch",
        "last_name": "Test",
        "department_id": 1,
        "salary": 1000000,
        "bonus": 50000,
        "hire_date": "2026-09-08"
    })

    employee_id = employee["employee_id"]

    updated = service.patch_employee(
        employee_id,
        {
            "salary": 1200000
        }
    )

    assert updated["salary"] == 1200000.0
    assert updated["first_name"] == "Patch"
    assert updated["last_name"] == "Test"
    assert updated["bonus"] == 50000.0   

def test_patch_employee_bonus():
    service = EmployeeService()
    employee = service.create_employee({
        "first_name": "Bonus",
        "last_name": "Test",
        "department_id": 1,
        "salary": 1000000,
        "bonus": 50000,
        "hire_date": "2026-09-08"
    })

    employee_id = employee["employee_id"]

    updated = service.patch_employee(
        employee_id,
        {
            "bonus": 100000
        }
    )

    assert updated["bonus"] == 100000.0
    assert updated["salary"] == 1000000.0