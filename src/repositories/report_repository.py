from src.database.connection import get_connection


class ReportRepository:

    def get_total_bonus(self):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            query = """
                SELECT COALESCE(SUM(Bonus), 0)
                FROM Employee
            """

            cursor.execute(query)
            row = cursor.fetchone()

            return float(row[0])

        finally:
            connection.close()

    def get_employees_without_bonus(self):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            query = """
                SELECT
                    EmployeeID,
                    FirstName,
                    LastName,
                    DepartmentID,
                    Salary,
                    Bonus,
                    HireDate
                FROM Employee
                WHERE Bonus IS NULL OR Bonus = 0
                ORDER BY EmployeeID
            """

            cursor.execute(query)
            rows = cursor.fetchall()

            employees = []

            for row in rows:
                employees.append({
                    "employee_id": row[0],
                    "first_name": row[1],
                    "last_name": row[2],
                    "department_id": row[3],
                    "salary": float(row[4]),
                    "bonus": None,
                    "hire_date": str(row[6])
                })

            return employees

        finally:
            connection.close()

    def get_bonus_percentage(self):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            query = """
                SELECT
                    EmployeeID,
                    FirstName,
                    LastName,
                    Salary,
                    Bonus,
                    ROUND((Bonus / Salary) * 100, 2) AS BonusPercentage
                FROM Employee
                WHERE Bonus IS NOT NULL
                  AND Bonus > 0
                  AND Salary > 0
                ORDER BY EmployeeID
            """

            cursor.execute(query)
            rows = cursor.fetchall()

            employees = []

            for row in rows:
                employees.append({
                    "employee_id": row[0],
                    "first_name": row[1],
                    "last_name": row[2],
                    "salary": float(row[3]),
                    "bonus": float(row[4]),
                    "bonus_percentage": float(row[5])
                })

            return employees

        finally:
            connection.close()

    def get_high_bonus_departments(self):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            query = """
                SELECT
                    d.DepartmentID,
                    d.DepartmentName,
                    SUM(COALESCE(e.Bonus, 0)) AS TotalBonus,
                    AVG(e.Salary) AS AverageSalary
                FROM Department d
                INNER JOIN Employee e
                    ON d.DepartmentID = e.DepartmentID
                GROUP BY
                    d.DepartmentID,
                    d.DepartmentName
                HAVING SUM(COALESCE(e.Bonus, 0)) > AVG(e.Salary)
                ORDER BY d.DepartmentID
            """

            cursor.execute(query)
            rows = cursor.fetchall()

            departments = []

            for row in rows:
                departments.append({
                    "department_id": row[0],
                    "department_name": row[1],
                    "total_bonus": float(row[2]),
                    "average_salary": float(row[3])
                })

            return departments

        finally:
            connection.close()

    def get_bonus_ranking(self):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            query = """
                SELECT
                    EmployeeID,
                    FirstName,
                    LastName,
                    Salary,
                    Bonus,
                    RANK() OVER (
                        ORDER BY Bonus DESC
                    ) AS BonusRank
                FROM Employee
                ORDER BY
                    CASE
                        WHEN Bonus IS NULL OR Bonus = 0 THEN 1
                        ELSE 0
                    END,
                    Bonus DESC
            """

            cursor.execute(query)
            rows = cursor.fetchall()

            employees = []

            for row in rows:
                employees.append({
                    "employee_id": row[0],
                    "first_name": row[1],
                    "last_name": row[2],
                    "salary": float(row[3]),
                    "bonus": float(row[4]) if row[4] is not None else None,
                    "rank": row[5]
                })

            return employees

        finally:
            connection.close()

    def get_highest_salary_employee(self):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            query = """
                SELECT TOP 1
                    EmployeeID,
                    FirstName,
                    LastName,
                    Salary,
                    Bonus,
                    Salary + COALESCE(Bonus, 0) AS TotalCompensation
                FROM Employee
                ORDER BY Salary DESC
            """

            cursor.execute(query)
            row = cursor.fetchone()

            if row is None:
                return None

            employee = {
                "employee_id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "salary": float(row[3]),
                "bonus": float(row[4]) if row[4] is not None else None,
                "total_compensation": float(row[5])
            }

            # Separately determine whether this employee
            # also has the highest total compensation.
            total_comp_query = """
                SELECT TOP 1
                    EmployeeID
                FROM Employee
                ORDER BY Salary + COALESCE(Bonus, 0) DESC
            """

            cursor.execute(total_comp_query)
            highest_total_row = cursor.fetchone()

            employee["also_highest_total_compensation"] = (
                highest_total_row is not None
                and highest_total_row[0] == employee["employee_id"]
            )

            return employee

        finally:
            connection.close()