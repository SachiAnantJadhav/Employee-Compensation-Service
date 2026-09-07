from src.repositories.employee_repository import EmployeeRepository


class EmployeeService:

    def __init__(self):
        self.repository = EmployeeRepository()

    def create_employee(self, data):
        self._validate_employee_data(data)

        if "bonus" not in data:
            bonus = data["salary"] * 0.05
        else:
            bonus = data["bonus"]

            if bonus is None:
                bonus = 0

        employee_id = self.repository.create_employee(
            first_name=data["first_name"],
            last_name=data["last_name"],
            department_id=data["department_id"],
            salary=data["salary"],
            bonus=bonus,
            hire_date=data["hire_date"]
        )

        return self.repository.get_employee_by_id(employee_id)

    def get_employee(self, employee_id):
        if employee_id <= 0:
            raise ValueError("Employee ID must be positive.")

        return self.repository.get_employee_by_id(employee_id)

    def get_employees(self, department_id=None):
        if department_id is not None and department_id <= 0:
            raise ValueError("Department ID must be positive.")

        return self.repository.get_all_employees(department_id)

    def update_employee(self, employee_id, data):
        if employee_id <= 0:
            raise ValueError("Employee ID must be positive.")

        self._validate_employee_data(data)

        if "bonus" not in data:
            bonus = data["salary"] * 0.05
        else:
            bonus = data["bonus"]

            if bonus is None:
                bonus = 0

        updated = self.repository.update_employee(
            employee_id=employee_id,
            first_name=data["first_name"],
            last_name=data["last_name"],
            department_id=data["department_id"],
            salary=data["salary"],
            bonus=bonus,
            hire_date=data["hire_date"]
        )

        if not updated:
            return None

        return self.repository.get_employee_by_id(employee_id)

    def delete_employee(self, employee_id):
        if employee_id <= 0:
            raise ValueError("Employee ID must be positive.")

        return self.repository.delete_employee(employee_id)
    
    def patch_employee(self, employee_id, data):
        if employee_id <= 0:
            raise ValueError("Employee ID must be positive.")

        if not data:
            raise ValueError("At least one field is required for update.")

        allowed_fields = {
            "first_name",
            "last_name",
            "department_id",
            "salary",
            "bonus",
            "hire_date"
        }

        invalid_fields = set(data.keys()) - allowed_fields

        if invalid_fields:
            raise ValueError(
                f"Invalid fields: {', '.join(invalid_fields)}"
            )

        self._validate_partial_employee_data(data)

        if "bonus" in data and data["bonus"] is None:
            data["bonus"] = 0

        updated = self.repository.patch_employee(
            employee_id,
            data
        )

        if not updated:
            return None

        return self.repository.get_employee_by_id(employee_id)

    def _validate_employee_data(self, data):

        required_fields = [
            "first_name",
            "last_name",
            "department_id",
            "salary",
            "hire_date"
        ]

        for field in required_fields:
            if field not in data or data[field] is None:
                raise ValueError(f"{field} is required.")
            
        if not isinstance(data["department_id"], int):
            raise ValueError("Department ID must be an integer.")

        if not isinstance(data["salary"], (int, float)):
            raise ValueError("Salary must be a number.")

        if data.get("bonus") is not None and not isinstance(
            data["bonus"], (int, float)
        ):
            raise ValueError("Bonus must be a number.")

        if not isinstance(data["first_name"], str):
            raise ValueError("First name must be a string.")

        if not data["first_name"].strip():
            raise ValueError("First name is required.")

        if len(data["first_name"]) > 50:
            raise ValueError(
                "First name cannot exceed 50 characters."
            )

        if not isinstance(data["last_name"], str):
            raise ValueError("Last name must be a string.")

        if not data["last_name"].strip():
            raise ValueError("Last name is required.")

        if len(data["last_name"]) > 50:
            raise ValueError(
                "Last name cannot exceed 50 characters."
            )

        if data["department_id"] <= 0:
            raise ValueError(
                "Department ID must be positive."
            )

        if data["salary"] < 0:
            raise ValueError(
                "Salary must be zero or greater."
            )

        if data.get("bonus") is not None:
            if data["bonus"] < 0:
                raise ValueError(
                    "Bonus must be zero or greater."
                )
        
    def _validate_partial_employee_data(self, data):

        if "first_name" in data:
            if not isinstance(data["first_name"], str):
                raise ValueError("First name must be a string.")

            if not data["first_name"].strip():
                raise ValueError("First name is required.")

            if len(data["first_name"]) > 50:
                raise ValueError(
                    "First name cannot exceed 50 characters."
                )

        if "last_name" in data:
            if not isinstance(data["last_name"], str):
                raise ValueError("Last name must be a string.")

            if not data["last_name"].strip():
                raise ValueError("Last name is required.")

            if len(data["last_name"]) > 50:
                raise ValueError(
                    "Last name cannot exceed 50 characters."
                )

        if "department_id" in data:
            if not isinstance(data["department_id"], int):
                raise ValueError(
                    "Department ID must be an integer."
                )

            if data["department_id"] <= 0:
                raise ValueError(
                    "Department ID must be positive."
                )

        if "salary" in data:
            if not isinstance(data["salary"], (int, float)):
                raise ValueError("Salary must be a number.")

            if data["salary"] < 0:
                raise ValueError(
                    "Salary must be zero or greater."
                )

        if "bonus" in data:
            if data["bonus"] is not None:
                if not isinstance(data["bonus"], (int, float)):
                    raise ValueError("Bonus must be a number.")

                if data["bonus"] < 0:
                    raise ValueError(
                        "Bonus must be zero or greater."
                    )    
            