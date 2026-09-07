from src.repositories.report_repository import ReportRepository


class CompensationService:
    def __init__(self):
        self.repository = ReportRepository()

    def get_total_bonus(self):
        return self.repository.get_total_bonus()

    def get_employees_without_bonus(self):
        return self.repository.get_employees_without_bonus()

    def get_bonus_percentage(self):
        return self.repository.get_bonus_percentage()

    def get_high_bonus_departments(self):
        return self.repository.get_high_bonus_departments()

    def get_bonus_ranking(self):
        return self.repository.get_bonus_ranking()

    def get_highest_salary_employee(self):
        return self.repository.get_highest_salary_employee()