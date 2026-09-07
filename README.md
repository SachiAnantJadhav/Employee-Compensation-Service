# Employee Compensation Service

A REST API for managing employee information and generating compensation-related reports.

The service is implemented using **Python Azure Functions** with **Azure SQL Database** as the backend database. Clients interact with the database only through the API.

---

## 1. Technology Stack

- **Python 3.12** — Backend programming language
- **Azure Functions** — Serverless HTTP API
- **Azure SQL Database** — Relational database
- **mssql-python** — SQL Server database connectivity
- **T-SQL** — Database schema, seed data, and reporting queries
- **pytest** — Automated testing
- **Postman** — API testing
- **Azure Functions Core Tools** — Local development and execution
- **Azurite** — Local Azure Storage emulator for Azure Functions

---

## 2. Project Overview

The Employee Compensation Service provides APIs for:

### Employee Management

- Create an employee
- Retrieve an employee by ID
- List employees
- Filter employees by department
- Update an employee
- Delete an employee

### Compensation Reports

- Calculate total company bonus
- Find employees who have never received a bonus
- Calculate bonus as a percentage of salary
- Find departments where total bonus exceeds average salary
- Rank employees by bonus
- Find the employee with the highest base salary
- Determine whether the highest-base-salary employee also has the highest total compensation

---

## 3. Architecture

The application follows a layered architecture:

```text
Client
  |
  | HTTP Request
  v
Azure Functions
  |
  v
Service Layer
  |
  v
Repository Layer
  |
  v
Azure SQL Database