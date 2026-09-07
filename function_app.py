import json
import logging
import azure.functions as func
from src.services.employee_service import EmployeeService
from src.services.compensation_service import CompensationService

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

employee_service = EmployeeService()
compensation_service = CompensationService()

@app.route(
    route="employees",
    methods=["POST"]
)
def create_employee(req: func.HttpRequest) -> func.HttpResponse:
    """
    Create a new employee.
    POST /api/employees
    """
    try:
        data = req.get_json()

        employee = employee_service.create_employee(data)

        return func.HttpResponse(
            json.dumps(employee),
            status_code=201,
            mimetype="application/json"
        )
    except ValueError as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=400,
            mimetype="application/json"
        )
    except Exception:
        logging.exception("Error creating employee")

        return func.HttpResponse(
            json.dumps({"error": "Internal server error"}),
            status_code=500,
            mimetype="application/json"
        )

@app.route(
    route="employees/{employee_id}",
    methods=["GET"]
)
def get_employee(req: func.HttpRequest) -> func.HttpResponse:
    """
    Retrieve a single employee.
    GET /api/employees/{employee_id}
    """
    try:
        employee_id = req.route_params.get("employee_id")

        employee = employee_service.get_employee(int(employee_id))

        if employee is None:
            return func.HttpResponse(
                json.dumps({"error": "Employee not found"}),
                status_code=404,
                mimetype="application/json"
            )

        return func.HttpResponse(
            json.dumps(employee),
            status_code=200,
            mimetype="application/json"
        )

    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "Invalid employee ID"}),
            status_code=400,
            mimetype="application/json"
        )

    except Exception:
        logging.exception("Error retrieving employee")

        return func.HttpResponse(
            json.dumps({"error": "Internal server error"}),
            status_code=500,
            mimetype="application/json"
        )


@app.route(
    route="employees",
    methods=["GET"]
)
def list_employees(req: func.HttpRequest) -> func.HttpResponse:
    """
    Retrieve employees.

    GET /api/employees

    Optional filtering:

    GET /api/employees?department_id=2
    """

    try:
        department_id = req.params.get("department_id")

        if department_id is not None:
            try:
                department_id = int(department_id)
            except ValueError:
                return func.HttpResponse(
                    json.dumps({"error": "Invalid department_id"}),
                    status_code=400,
                    mimetype="application/json"
                )

        employees = employee_service.get_employees(
            department_id=department_id
        )

        return func.HttpResponse(
            json.dumps(employees),
            status_code=200,
            mimetype="application/json"
        )

    except Exception:
        logging.exception("Error retrieving employees")

        return func.HttpResponse(
            json.dumps({"error": "Internal server error"}),
            status_code=500,
            mimetype="application/json"
        )


@app.route(
    route="employees/{employee_id}",
    methods=["PUT"]
)
def update_employee(req: func.HttpRequest) -> func.HttpResponse:
    """
    Update an existing employee.

    PUT /api/employees/{employee_id}
    """

    try:
        employee_id = req.route_params.get("employee_id")

        data = req.get_json()

        employee = employee_service.update_employee(
            int(employee_id),
            data
        )

        if employee is None:
            return func.HttpResponse(
                json.dumps({"error": "Employee not found"}),
                status_code=404,
                mimetype="application/json"
            )

        return func.HttpResponse(
            json.dumps(employee),
            status_code=200,
            mimetype="application/json"
        )

    except ValueError as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=400,
            mimetype="application/json"
        )

    except Exception:
        logging.exception("Error updating employee")

        return func.HttpResponse(
            json.dumps({"error": "Internal server error"}),
            status_code=500,
            mimetype="application/json"
        )


@app.route(
    route="employees/{employee_id}",
    methods=["DELETE"]
)
def delete_employee(req: func.HttpRequest) -> func.HttpResponse:
    """
    Delete an employee.

    DELETE /api/employees/{employee_id}
    """

    try:
        employee_id = req.route_params.get("employee_id")

        deleted = employee_service.delete_employee(
            int(employee_id)
        )

        if not deleted:
            return func.HttpResponse(
                json.dumps({"error": "Employee not found"}),
                status_code=404,
                mimetype="application/json"
            )

        return func.HttpResponse(
            status_code=204
        )

    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "Invalid employee ID"}),
            status_code=400,
            mimetype="application/json"
        )

    except Exception:
        logging.exception("Error deleting employee")

        return func.HttpResponse(
            json.dumps({"error": "Internal server error"}),
            status_code=500,
            mimetype="application/json"
        )


# ============================================================
# COMPENSATION REPORTS
# ============================================================

@app.route(
    route="reports/total-bonus",
    methods=["GET"]
)
def total_bonus(req: func.HttpRequest) -> func.HttpResponse:
    """
    Return total bonus paid across the company.

    GET /api/reports/total-bonus
    """

    try:
        result = compensation_service.get_total_bonus()

        return func.HttpResponse(
            json.dumps(result),
            status_code=200,
            mimetype="application/json"
        )

    except Exception:
        logging.exception("Error calculating total bonus")

        return func.HttpResponse(
            json.dumps({"error": "Internal server error"}),
            status_code=500,
            mimetype="application/json"
        )


@app.route(
    route="reports/no-bonus",
    methods=["GET"]
)
def employees_without_bonus(req: func.HttpRequest) -> func.HttpResponse:
    """
    Return employees who have never received a bonus.

    GET /api/reports/no-bonus
    """

    try:
        result = compensation_service.get_employees_without_bonus()

        return func.HttpResponse(
            json.dumps(result),
            status_code=200,
            mimetype="application/json"
        )

    except Exception:
        logging.exception("Error retrieving employees without bonus")

        return func.HttpResponse(
            json.dumps({"error": "Internal server error"}),
            status_code=500,
            mimetype="application/json"
        )


@app.route(
    route="reports/bonus-percentage",
    methods=["GET"]
)
def bonus_percentage(req: func.HttpRequest) -> func.HttpResponse:
    """
    Return bonus as percentage of salary
    for employees who have a bonus.

    GET /api/reports/bonus-percentage
    """

    try:
        result = compensation_service.get_bonus_percentage()

        return func.HttpResponse(
            json.dumps(result),
            status_code=200,
            mimetype="application/json"
        )

    except Exception:
        logging.exception("Error calculating bonus percentage")

        return func.HttpResponse(
            json.dumps({"error": "Internal server error"}),
            status_code=500,
            mimetype="application/json"
        )


@app.route(
    route="reports/high-bonus-departments",
    methods=["GET"]
)
def high_bonus_departments(req: func.HttpRequest) -> func.HttpResponse:
    """
    Return departments where total bonus
    exceeds department average salary.

    GET /api/reports/high-bonus-departments
    """

    try:
        result = compensation_service.get_high_bonus_departments()

        return func.HttpResponse(
            json.dumps(result),
            status_code=200,
            mimetype="application/json"
        )

    except Exception:
        logging.exception("Error finding high bonus departments")

        return func.HttpResponse(
            json.dumps({"error": "Internal server error"}),
            status_code=500,
            mimetype="application/json"
        )


@app.route(
    route="reports/bonus-ranking",
    methods=["GET"]
)
def bonus_ranking(req: func.HttpRequest) -> func.HttpResponse:
    """
    Return employees ranked by bonus.

    Employees with NULL bonus appear last.

    GET /api/reports/bonus-ranking
    """

    try:
        result = compensation_service.get_bonus_ranking()

        return func.HttpResponse(
            json.dumps(result),
            status_code=200,
            mimetype="application/json"
        )

    except Exception:
        logging.exception("Error generating bonus ranking")

        return func.HttpResponse(
            json.dumps({"error": "Internal server error"}),
            status_code=500,
            mimetype="application/json"
        )


@app.route(
    route="reports/highest-salary",
    methods=["GET"]
)
def highest_salary(req: func.HttpRequest) -> func.HttpResponse:
    """
    Return the employee with the highest base salary
    and whether they also have the highest total compensation.
    GET /api/reports/highest-salary
    """
    try:
        result = compensation_service.get_highest_salary_employee()
        if result is None:
            return func.HttpResponse(
                json.dumps({"error": "No employees found"}),
                status_code=404,
                mimetype="application/json"
            )
        return func.HttpResponse(
            json.dumps(result),
            status_code=200,
            mimetype="application/json"
        )
    except Exception:
        logging.exception("Error finding highest salary employee")
        return func.HttpResponse(
            json.dumps({"error": "Internal server error"}),
            status_code=500,
            mimetype="application/json"
        )
        
        
@app.route(
    route="employees/{employee_id}",
    methods=["PATCH"]
)
def patch_employee(req: func.HttpRequest) -> func.HttpResponse:

    try:
        employee_id = int(
            req.route_params.get("employee_id")
        )

        data = req.get_json()

        employee = employee_service.patch_employee(
            employee_id,
            data
        )

        if employee is None:
            return func.HttpResponse(
                json.dumps({
                    "error": "Employee not found."
                }),
                status_code=404,
                mimetype="application/json"
            )

        return func.HttpResponse(
            json.dumps(employee),
            status_code=200,
            mimetype="application/json"
        )

    except ValueError as e:
        return func.HttpResponse(
            json.dumps({
                "error": str(e)
            }),
            status_code=400,
            mimetype="application/json"
        )

    except Exception:
        return func.HttpResponse(
            json.dumps({
                "error": "Internal server error."
            }),
            status_code=500,
            mimetype="application/json"
        )