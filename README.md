# Employee Compensation Service

A backend service for managing employee compensation data and generating compensation-related reports.

The service is implemented using **Python Azure Functions** with **Azure SQL Database** as the persistent data store. Clients interact with the system through HTTP APIs and do not access the database directly.

---

## 1. Tech Stack

| Technology         | Purpose                                                |
| ------------------ | ------------------------------------------------------ |
| Python 3.12        | Application development                                |
| Azure Functions    | HTTP API / serverless backend                          |
| Azure SQL Database | Relational database                                    |
| mssql-python       | Direct SQL database connectivity                       |
| SQL                | Database schema, CRUD operations and reporting queries |
| pytest             | Automated testing                                      |
| Postman            | API testing                                            |
| Git / GitHub       | Version control and source repository                  |

---

## 2. Architecture

The application follows a layered structure:

```text
Client / Postman
       |
       v
Azure Functions (HTTP APIs)
       |
       v
Service Layer
       |
       v
Repository Layer
       |
       v
mssql-python
       |
       v
Azure SQL Database
```

### Layers

- **Function Layer** – Handles HTTP requests, responses, status codes and error handling.
- **Service Layer** – Handles validation and application/business logic.
- **Repository Layer** – Handles SQL queries and database operations.
- **Database Layer** – Provides the database connection.
- **Azure SQL Database** – Stores employee and department data.

---

## 3. Project Structure

```text
FUSION_PRACTICES_ASSIGNMENT/
│
├── sql/
│   ├── create_tables.sql
│   └── seed_data.sql
│
├── src/
│   ├── database/
│   │   └── connection.py
│   │
│   ├── models/
│   │   ├── department.py
│   │   └── employee.py
│   │
│   ├── repositories/
│   │   ├── employee_repository.py
│   │   └── report_repository.py
│   │
│   └── services/
│       ├── employee_service.py
│       └── compensation_service.py
│
├── tests/
│   ├── conftest.py
│   ├── test_employees.py
│   └── test_reports.py
│
├── function_app.py
├── host.json
├── requirements.txt
├── .gitignore
├── .funcignore
└── README.md
```

---

## 4. Database

The database contains two tables:

### Department

```text
DepartmentID
DepartmentName
Location
```

### Employee

```text
EmployeeID
FirstName
LastName
DepartmentID
Salary
Bonus
HireDate
```

`Employee.DepartmentID` is a foreign key referencing `Department.DepartmentID`.

The database schema is available in:

```text
sql/create_tables.sql
```

Sample data is available in:

```text
sql/seed_data.sql
```

---

## 5. Setup

### Prerequisites

Install the following:

- Python 3.12
- Azure Functions Core Tools
- Azure CLI
- Git
- Postman (for API testing)

An Azure subscription with access to Azure Functions and Azure SQL Database is also required for cloud deployment.

---

### a. Clone the Repository

```bash
git clone https://github.com/SachiAnantJadhav/Employee-Compensation-Service.git
cd FUSION_PRACTICES_ASSIGNMENT
```

---

### b. Create a Virtual Environment

### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

---

### c. Install Dependencies

```bash
pip install -r requirements.txt
```

The main dependencies are:

```text
azure-functions
mssql-python
pytest
```

---

### d. Database Setup

Create an Azure SQL Database and execute:

```bash
sql/create_tables.sql
```

to create the required tables.

Then execute:

```bash
sql/seed_data.sql
```

to insert the initial department and employee data.

---

### e. Configuration

Database credentials and connection strings are **not hardcoded in the source code**.

For local development, create `local.settings.json`:

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "DATABASE_CONNECTION_STRING": "YOUR_DATABASE_CONNECTION_STRING"
  }
}
```

Replace the placeholder with the appropriate Azure SQL connection string.

## 6. Security

`local.settings.json` is included in `.gitignore` and must **not be committed to GitHub**, because it contains sensitive configuration.

For Azure deployment, `DATABASE_CONNECTION_STRING` is configured as an **Application Setting / Environment Variable** in the Azure Function App.

---

## 7. Run Locally

Start the Azure Functions host from the project root:

```bash
func start
```

The local APIs will be available through the URLs shown by Azure Functions Core Tools.

---

## 8. API Endpoints

### Employee APIs

| Method | Endpoint                            | Description                 |
| ------ | ----------------------------------- | --------------------------- |
| POST   | `/api/employees`                    | Create an employee          |
| GET    | `/api/employees/{employee_id}`      | Get an employee by ID       |
| GET    | `/api/employees`                    | Get all employees           |
| GET    | `/api/employees?department_id={id}` | Get employees by department |
| PUT    | `/api/employees/{employee_id}`      | Update an employee          |
| DELETE | `/api/employees/{employee_id}`      | Delete an employee          |

---

### Compensation Reports

| Method | Endpoint                              | Description                                           |
| ------ | ------------------------------------- | ----------------------------------------------------- |
| GET    | `/api/reports/total-bonus`            | Total bonus paid across employees                     |
| GET    | `/api/reports/no-bonus`               | Employees who have never received a bonus             |
| GET    | `/api/reports/bonus-percentage`       | Bonus as a percentage of salary                       |
| GET    | `/api/reports/high-bonus-departments` | Departments where total bonus exceeds average salary  |
| GET    | `/api/reports/bonus-ranking`          | Employees ranked by bonus                             |
| GET    | `/api/reports/highest-salary`         | Highest base salary and total compensation comparison |

---

## 9. Example API Requests

### Create Employee

**POST**

```text
/api/employees
```

Request body:

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "department_id": 1,
  "salary": 800000,
  "bonus": 50000,
  "hire_date": "2026-09-07"
}
```

Expected response:

```text
201 Created
```

---

### Get Employee

**GET**

```text
/api/employees/1
```

Example response:

```json
{
  "employee_id": 1,
  "first_name": "Aarav",
  "last_name": "Sharma",
  "department_id": 1,
  "salary": 1200000.0,
  "bonus": 150000.0,
  "hire_date": "2022-01-10"
}
```

---

### Update Employee

**PUT**

```text
/api/employees/1
```

Request body:

```json
{
  "first_name": "Aarav",
  "last_name": "Sharma",
  "department_id": 1,
  "salary": 1250000,
  "bonus": 175000,
  "hire_date": "2022-01-10"
}
```

Expected response:

```text
200 OK
```

---

### Delete Employee

**DELETE**

```text
/api/employees/1
```

Expected response:

```text
204 No Content
```

---

## 10. Reporting Logic

### Total Bonus

Calculates the total bonus across all employees.

`NULL` bonuses are treated as zero.

### Employees Without Bonus

Returns employees where:

```sql
Bonus IS NULL
```

### Bonus Percentage

Calculates:

```text
Bonus / Salary × 100
```

and rounds the result to two decimal places.

Employees with `NULL` bonuses are excluded from this report.

### High-Bonus Departments

Returns departments where:

```text
Total Department Bonus > Average Department Salary
```

`NULL` bonuses are treated as zero.

### Bonus Ranking

Employees are ranked based on bonus in descending order.

Employees with `NULL` bonuses appear last.

### Highest Salary

Returns the employee with the highest base salary and also determines whether that employee has the highest total compensation.

Total compensation is calculated as:

```text
Salary + Bonus
```

with `NULL` bonus treated as zero.

---

## 11. Important Design Decisions & Assumptions

> **These decisions were made where the assignment allowed flexibility or required an assumption.**

### 1. Bonus Default Policy

A default bonus of **5% of salary** is considered when a bonus is not explicitly provided.

The default is applied at **write time**, so the calculated bonus is stored in the `Bonus` column.

This keeps compensation values consistent and makes reporting queries straightforward.

### 2. NULL Bonus Handling

A `NULL` bonus represents an employee who has not received a bonus.

For calculations where a numeric bonus is required, `NULL` is treated as:

```text
0
```

For the "employees without bonus" report, the original `NULL` value is preserved.

### 3. Database Access

Clients never access Azure SQL directly.

All database operations go through the Azure Functions API.

### 4. SQL Access

The implementation uses **direct SQL through `mssql-python`**.

No ORM is used.

### 5. Validation

The service validates:

- Required employee fields
- First and last name types and lengths
- Positive department IDs
- Numeric salary and bonus values
- Non-negative salary and bonus values
- Positive employee IDs

Invalid input returns a `400 Bad Request`.

### 6. Not Found Handling

If an employee does not exist:

```text
404 Not Found
```

is returned.

### 7. Authentication

The Azure Functions use **Function-level HTTP authorization**.

Deployed API requests therefore require a valid Azure Function key.

---

## 12. Error Handling

The API uses appropriate HTTP status codes.

| Status | Meaning                             |
| ------ | ----------------------------------- |
| 200    | Successful request                  |
| 201    | Employee successfully created       |
| 204    | Employee successfully deleted       |
| 400    | Invalid request or validation error |
| 404    | Employee not found                  |
| 500    | Unexpected server/database error    |

Errors are handled at the HTTP function layer so that clients receive an appropriate response instead of an unhandled exception.

---

## 13. Testing

Automated tests are implemented using `pytest`.

Run:

```bash
pytest
```

The test suite covers employee validation and compensation reports.

Current test result:

```text
10 passed
```

---

## 14. API Testing with Postman

The deployed Azure Function endpoints can be tested using Postman.

For the deployed Function App, use the Azure-provided function URL and include the required function key.

Recommended testing sequence:

```text
1. Create employee
2. Get employee
3. List employees
4. Filter employees by department
5. Update employee
6. Delete employee

7. Total bonus
8. Employees without bonus
9. Bonus percentage
10. High-bonus departments
11. Bonus ranking
12. Highest salary
```

---

## 15. Azure Deployment

The application is deployed as an **Azure Function App** running Python.

Deployment from the project root is performed using:

```bash
az login
```

followed by:

```bash
func azure functionapp publish employee-compensation-service
```

The database connection string is configured in the Azure Function App's environment variables rather than being included in the source code.

---

## 16. Repository

Source code and project files:

**GitHub:**

https://github.com/SachiAnantJadhav/FUSION_PRACTICES_ASSIGNMENT
