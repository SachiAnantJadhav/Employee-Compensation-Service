# Employee Compensation Service

This project implements a backend service for managing employee records and generating compensation-related reports. It is built using Azure Functions and Azure SQL, with all data access going through the Functions layer rather than directly from clients.

The service exposes HTTP APIs for employee CRUD operations and reports such as total bonus, bonus percentage, bonus rankings, and salary analysis.

---

## 1. Intro

The goal of the project is to provide a small, production-minded HR backend that:

- stores employee and department data in SQL
- exposes HTTP endpoints through Azure Functions
- validates business rules before writing to the database
- returns readable JSON responses with proper HTTP status codes
- supports reporting on compensation and salary data

This project is designed to follow a clean layered architecture for maintainability and clarity.

---

## 2. Tech Stack

| Technology                 | Purpose                                 |
| -------------------------- | --------------------------------------- |
| Python 3.12                | Backend application development         |
| Azure Functions            | HTTP-triggered serverless APIs          |
| Azure SQL Database         | Persistent database                     |
| mssql-python               | Direct SQL connectivity                 |
| SQL                        | Schema definition and reporting queries |
| pytest                     | Automated testing                       |
| Streamlit                  | Optional frontend UI                    |
| Postman                    | API testing                             |
| Azure Functions Core Tools | Local Azure Functions execution         |
| Git / GitHub               | Version control and repository hosting  |

---

## 3. Architecture

The project follows a layered design:

```text
Client / Postman / Streamlit
          |
          v
Azure Functions (HTTP API)
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

- Function Layer: handles HTTP requests, responses, and status codes
- Service Layer: validates input and applies business rules
- Repository Layer: runs SQL queries and database operations
- Database Layer: manages the SQL connection using environment variables

This keeps database access isolated from direct client interaction.

---

## 4. Project Structure

```text
FUSION_PRACTICES_ASSIGNMENT/
├── frontend/
│   ├── api_client.py
│   |── app.py
|   └── .streamlit/
|       └── secrets.toml
├── sql/
│   ├── create_tables.sql
│   └── seed_data.sql
├── src/
│   ├── database/
│   │   └── connection.py
│   ├── repositories/
│   │   ├── employee_repository.py
│   │   └── report_repository.py
│   └── services/
│       ├── compensation_service.py
│       └── employee_service.py
├── tests/
│   ├── conftest.py
│   ├── test_employees.py
│   └── test_reports.py
├── function_app.py
├── host.json
├── requirements.txt
├── .gitignore
├── .funcignore
├── README.md
├── local.settings.json

```

> Note: `local.settings.json` and `.streamlit/secrets.toml` should not be committed to source control.

---

## 5. Database Structure

The database contains two tables:

### Department

```text
DepartmentID      INT           PRIMARY KEY
DepartmentName    VARCHAR(100)  NOT NULL
Location          VARCHAR(100)  NULL
```

### Employee

```text
EmployeeID        INT           PRIMARY KEY
FirstName         VARCHAR(50)   NOT NULL
LastName          VARCHAR(50)   NOT NULL
DepartmentID      INT           FOREIGN KEY -> Department.DepartmentID
Salary            DECIMAL(12,2) NOT NULL
Bonus             DECIMAL(12,2) NULL
HireDate          DATE          NOT NULL
```

The relationship is:

```text
Employee.DepartmentID -> Department.DepartmentID
```

The SQL scripts for schema and seed data are in:

- `sql/create_tables.sql`
- `sql/seed_data.sql`

---

## 6. Setup and Installation

### Prerequisites

Install the following:

- Python 3.12
- Azure Functions Core Tools
- Azure CLI
- Git
- Postman or another HTTP client
- Azure SQL Database access

---

### 6.1 Clone the repository

```bash
git clone https://github.com/SachiAnantJadhav/Employee-Compensation-Service
cd Employee-Compensation-Service
```

---

### 6.2 Create a virtual environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 6.3 Install dependencies

```bash
pip install -r requirements.txt
```

Typical dependencies include:

```text
azure-functions
mssql-python
pytest
requests
streamlit
```

---

### 6.4 Set up the database

Create your Azure SQL database, then run:

```bash
sql/create_tables.sql
```

Then load the seed data:

```bash
sql/seed_data.sql
```

---

### 6.5 Create local settings for Azure Functions

Create a file named `local.settings.json` in the project root with the following structure:

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "DATABASE_CONNECTION_STRING": "Server=tcp:<server-name>.database.windows.net,1433;Initial Catalog=<database-name>;Persist Security Info=False;User ID=<username>;Password=<password>;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;"
  }
}
```

This file contains secrets and must be kept local.

---

### 6.6 Create Streamlit secrets file

For the local frontend, create a `.streamlit/secrets.toml` file with this structure:

```toml
API_BASE_URL = "http://localhost:7071"
FUNCTION_KEY = "your_local_function_key_here"
```

If you are using the deployed app, the values can be replaced with the deployed API URL and function key instead.

> `FUNCTION_KEY` is required only when the Azure Function app is configured with function-level authorization.

---

### 6.7 Run Azure Functions locally

From the project root:

```bash
func start
```

This starts the Azure Functions host and exposes the local endpoints.

---

### 6.8 Run the Streamlit frontend locally (optional)

```bash
streamlit run frontend/app.py
```

---

## 7. Local Endpoints

The following endpoints are exposed by the Azure Function app.

### Employee APIs

| Method | Endpoint                            | Description                   |
| ------ | ----------------------------------- | ----------------------------- |
| POST   | `/api/employees`                    | Create a new employee         |
| GET    | `/api/employees/{employee_id}`      | Get one employee by ID        |
| GET    | `/api/employees`                    | Get all employees             |
| GET    | `/api/employees?department_id={id}` | Get employees by department   |
| PUT    | `/api/employees/{employee_id}`      | Full update of an employee    |
| PATCH  | `/api/employees/{employee_id}`      | Partial update of an employee |
| DELETE | `/api/employees/{employee_id}`      | Delete an employee            |

### Compensation Reports

| Method | Endpoint                              | Description                                          |
| ------ | ------------------------------------- | ---------------------------------------------------- |
| GET    | `/api/reports/total-bonus`            | Total bonus paid across company                      |
| GET    | `/api/reports/no-bonus`               | Employees with no bonus                              |
| GET    | `/api/reports/bonus-percentage`       | Bonus as a percentage of salary                      |
| GET    | `/api/reports/high-bonus-departments` | Departments whose total bonus exceeds average salary |
| GET    | `/api/reports/bonus-ranking`          | Employees ranked by bonus                            |
| GET    | `/api/reports/highest-salary`         | Highest salary employee and compensation comparison  |

---

## 8. Assumptions and Design Decisions

The assignment leaves some details open, so the following assumptions were made to keep behavior consistent and explicit.

### 1. Default bonus is applied at write time

A default bonus equal to 5% of salary is applied when a bonus is not provided during create/update.

Example:

```json
{
  "salary": 1000000
}
```

If no bonus is provided, the system stores:

```text
bonus = 1000000 * 0.05 = 50000
```

This is done when the employee is written to the database, not when reading it.

### 2. PUT is a full update

`PUT /api/employees/{employee_id}` is treated as a full employee update. The request should include all required employee fields.

### 3. PATCH is used for partial updates

Partial updates are allowed through a patch-style flow, where omitted fields are treated as unchanged.

### 4. Explicit null bonus is treated as zero

If the client sends:

```json
{
  "bonus": null
}
```

it is interpreted as `0` for business logic purposes.

### 5. NULL and zero are treated as no bonus in reports

For reporting, both `NULL` and `0` are treated as no bonus.

### 6. Total bonus uses `NULL` as zero

The total company bonus report uses `COALESCE` logic so that `NULL` bonuses do not break the calculation.

---

## 9. Azure and Deployment

This project is designed to run as an Azure Function App.

The deployed version is available here:

https://employee-compensation-service-deployed.streamlit.app/

For Azure deployment, secrets and database connection details are stored as application settings rather than being hardcoded in the source code.

---

## 10. Notes

- Clients do not access the SQL database directly.
- All reads and writes go through Azure Functions endpoints.
- Local secret files are intentionally excluded from source control.
- The project is structured to be easy to test and extend.

---

## 11. Testing

Run the test suite with:

```bash
pytest
```

This validates employee validation rules and the report logic.
