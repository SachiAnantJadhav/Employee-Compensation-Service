from src.services.compensation_service import CompensationService


def test_total_bonus():
    service = CompensationService()

    result = service.get_total_bonus()

    assert isinstance(result, float)
    assert result >= 0


def test_employees_without_bonus():
    service = CompensationService()

    result = service.get_employees_without_bonus()

    assert isinstance(result, list)

    for employee in result:
        assert employee["bonus"] is None


def test_bonus_percentage():
    service = CompensationService()

    result = service.get_bonus_percentage()

    assert isinstance(result, list)

    for employee in result:
        assert "employee_id" in employee
        assert "bonus_percentage" in employee
        assert employee["bonus_percentage"] >= 0


def test_high_bonus_departments():
    service = CompensationService()

    result = service.get_high_bonus_departments()

    assert isinstance(result, list)

    for department in result:
        assert department["total_bonus"] > department["average_salary"]


def test_bonus_ranking():
    service = CompensationService()

    result = service.get_bonus_ranking()

    assert isinstance(result, list)

    # Employees with bonuses should come before employees with NULL bonuses.
    seen_null_bonus = False

    for employee in result:
        if employee["bonus"] is None:
            seen_null_bonus = True
        else:
            assert not seen_null_bonus


def test_highest_salary():
    service = CompensationService()

    result = service.get_highest_salary_employee()

    assert result is not None
    assert "employee_id" in result
    assert "salary" in result
    assert "total_compensation" in result
    assert "also_highest_total_compensation" in result