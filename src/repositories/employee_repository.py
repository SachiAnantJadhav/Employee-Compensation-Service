from src.database.connection import get_connection


class EmployeeRepository:

    def create_employee(
        self,
        first_name,
        last_name,
        department_id,
        salary,
        bonus,
        hire_date
    ):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            query = """
                INSERT INTO Employee
                (
                    FirstName,
                    LastName,
                    DepartmentID,
                    Salary,
                    Bonus,
                    HireDate
                )
                OUTPUT INSERTED.EmployeeID
                VALUES (?, ?, ?, ?, ?, ?)
            """

            cursor.execute(
                query,
                (
                    first_name,
                    last_name,
                    department_id,
                    salary,
                    bonus,
                    hire_date
                )
            )

            employee_id = cursor.fetchone()[0]

            connection.commit()

            return employee_id

        finally:
            connection.close()

    def get_employee_by_id(self, employee_id):
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
                WHERE EmployeeID = ?
            """

            cursor.execute(query, (employee_id,))

            row = cursor.fetchone()

            if row is None:
                return None

            return {
                "employee_id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "department_id": row[3],
                "salary": float(row[4]),
                "bonus": float(row[5]) if row[5] is not None else None,
                "hire_date": str(row[6])
            }

        finally:
            connection.close()

    def get_all_employees(self, department_id=None):
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
            """

            parameters = ()

            if department_id is not None:
                query += """
                    WHERE DepartmentID = ?
                """
                parameters = (department_id,)

            query += """
                ORDER BY EmployeeID
            """

            cursor.execute(query, parameters)

            rows = cursor.fetchall()

            employees = []

            for row in rows:
                employees.append({
                    "employee_id": row[0],
                    "first_name": row[1],
                    "last_name": row[2],
                    "department_id": row[3],
                    "salary": float(row[4]),
                    "bonus": float(row[5]) if row[5] is not None else None,
                    "hire_date": str(row[6])
                })

            return employees

        finally:
            connection.close()

    def update_employee(
        self,
        employee_id,
        first_name,
        last_name,
        department_id,
        salary,
        bonus,
        hire_date
    ):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            query = """
                UPDATE Employee
                SET
                    FirstName = ?,
                    LastName = ?,
                    DepartmentID = ?,
                    Salary = ?,
                    Bonus = ?,
                    HireDate = ?
                WHERE EmployeeID = ?
            """

            cursor.execute(
                query,
                (
                    first_name,
                    last_name,
                    department_id,
                    salary,
                    bonus,
                    hire_date,
                    employee_id
                )
            )

            connection.commit()

            return cursor.rowcount > 0

        finally:
            connection.close()

    def delete_employee(self, employee_id):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            query = """
                DELETE FROM Employee
                WHERE EmployeeID = ?
            """

            cursor.execute(query, (employee_id,))

            connection.commit()

            return cursor.rowcount > 0

        finally:
            connection.close()