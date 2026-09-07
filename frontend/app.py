import streamlit as st
from datetime import date

from api_client import (
    create_employee,
    get_employee,
    get_employees,
    update_employee,
    patch_employee,
    delete_employee,
    get_total_bonus,
    get_employees_without_bonus,
    get_bonus_percentage,
    get_high_bonus_departments,
    get_bonus_ranking,
    get_highest_salary,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Employee Compensation Service",
    page_icon="💼",
    layout="wide",
)


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 2.3rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        color: #6b7280;
        margin-bottom: 1.5rem;
    }

    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    .operation-header {
        font-size: 1.25rem;
        font-weight: 600;
        margin-top: 0.5rem;
        margin-bottom: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">Employee Compensation Service</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "Employee management and compensation reporting through Azure Functions."
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# TWO EQUAL COLUMNS
# ============================================================

left, right = st.columns(2, gap="large")


# ============================================================
# LEFT SIDE — EMPLOYEE OPERATIONS
# ============================================================

with left:

    st.markdown(
        '<div class="section-header">Employee Operations</div>',
        unsafe_allow_html=True,
    )

    operation = st.selectbox(
        "Select Operation",
        [
            "Create Employee",
            "Get Employee",
            "List Employees",
            "Update Employee",
            "Patch Employee",
            "Delete Employee",
        ],
    )

    st.divider()

    # ========================================================
    # CREATE EMPLOYEE
    # ========================================================

    if operation == "Create Employee":

        st.markdown(
            '<div class="operation-header">Create Employee</div>',
            unsafe_allow_html=True,
        )

        with st.form("create_employee_form"):

            first_name = st.text_input(
                "First Name *",
                placeholder="Enter first name",
            )

            last_name = st.text_input(
                "Last Name *",
                placeholder="Enter last name",
            )

            department_id = st.number_input(
                "Department ID *",
                min_value=1,
                step=1,
                value=1,
            )

            salary = st.number_input(
                "Salary *",
                min_value=0.0,
                step=10000.0,
                format="%.2f",
            )

            provide_bonus = st.checkbox(
                "Provide a specific bonus",
                value=False,
            )

            bonus = None

            if provide_bonus:
                bonus = st.number_input(
                    "Bonus",
                    min_value=0.0,
                    step=5000.0,
                    format="%.2f",
                )

            hire_date = st.date_input(
                "Hire Date *",
                value=date.today(),
            )

            st.caption(
                "Leave the specific bonus unchecked to apply the "
                "default 5% bonus."
            )

            submitted = st.form_submit_button(
                "Create Employee",
                type="primary",
                use_container_width=True,
            )

        if submitted:

            if not first_name.strip():
                st.error("First Name is required.")

            elif not last_name.strip():
                st.error("Last Name is required.")

            elif salary < 0:
                st.error("Salary must be zero or greater.")

            else:

                data = {
                    "first_name": first_name.strip(),
                    "last_name": last_name.strip(),
                    "department_id": int(department_id),
                    "salary": salary,
                    "hire_date": str(hire_date),
                }

                if provide_bonus:
                    data["bonus"] = bonus

                try:

                    result = create_employee(data)

                    st.success(
                        "Employee created successfully."
                    )

                    st.markdown("#### Response")

                    st.json(result)

                except Exception as error:

                    st.error(str(error))


    # ========================================================
    # GET EMPLOYEE
    # ========================================================

    elif operation == "Get Employee":

        st.markdown(
            '<div class="operation-header">Get Employee</div>',
            unsafe_allow_html=True,
        )

        employee_id = st.number_input(
            "Employee ID *",
            min_value=1,
            step=1,
            value=1,
        )

        if st.button(
            "Get Employee",
            type="primary",
            use_container_width=True,
        ):

            try:

                result = get_employee(
                    int(employee_id)
                )

                st.success("Employee found.")

                st.markdown("#### Response")

                st.json(result)

            except Exception as error:

                st.error(str(error))


    # ========================================================
    # LIST EMPLOYEES
    # ========================================================

    elif operation == "List Employees":

        st.markdown(
            '<div class="operation-header">List Employees</div>',
            unsafe_allow_html=True,
        )

        filter_by_department = st.checkbox(
            "Filter by Department"
        )

        department_id = None

        if filter_by_department:

            department_id = st.number_input(
                "Department ID",
                min_value=1,
                step=1,
                value=1,
            )

        if st.button(
            "Get Employees",
            type="primary",
            use_container_width=True,
        ):

            try:

                result = get_employees(
                    int(department_id)
                    if department_id is not None
                    else None
                )

                st.success(
                    f"{len(result)} employee(s) found."
                )

                st.markdown("#### Response")

                if result:
                    st.json(result)
                else:
                    st.info("No employees found.")

            except Exception as error:

                st.error(str(error))


    # ========================================================
    # UPDATE EMPLOYEE
    # ========================================================

    elif operation == "Update Employee":

        st.markdown(
            '<div class="operation-header">Update Employee</div>',
            unsafe_allow_html=True,
        )

        with st.form("update_employee_form"):

            employee_id = st.number_input(
                "Employee ID *",
                min_value=1,
                step=1,
                value=1,
            )

            first_name = st.text_input(
                "First Name *",
                placeholder="Enter first name",
            )

            last_name = st.text_input(
                "Last Name *",
                placeholder="Enter last name",
            )

            department_id = st.number_input(
                "Department ID *",
                min_value=1,
                step=1,
                value=1,
            )

            salary = st.number_input(
                "Salary *",
                min_value=0.0,
                step=10000.0,
                format="%.2f",
            )

            provide_bonus = st.checkbox(
                "Provide a specific bonus",
                value=False,
            )

            bonus = None

            if provide_bonus:

                bonus = st.number_input(
                    "Bonus",
                    min_value=0.0,
                    step=5000.0,
                    format="%.2f",
                )

            hire_date = st.date_input(
                "Hire Date *",
                value=date.today(),
            )

            st.caption(
                "Leave the specific bonus unchecked to apply the "
                "default 5% bonus based on the new salary."
            )

            submitted = st.form_submit_button(
                "Update Employee",
                type="primary",
                use_container_width=True,
            )

        if submitted:

            if not first_name.strip():
                st.error("First Name is required.")

            elif not last_name.strip():
                st.error("Last Name is required.")

            else:

                data = {
                    "first_name": first_name.strip(),
                    "last_name": last_name.strip(),
                    "department_id": int(department_id),
                    "salary": salary,
                    "hire_date": str(hire_date),
                }

                if provide_bonus:
                    data["bonus"] = bonus

                try:

                    result = update_employee(
                        int(employee_id),
                        data,
                    )

                    st.success(
                        "Employee updated successfully."
                    )

                    st.markdown("#### Response")

                    st.json(result)

                except Exception as error:

                    st.error(str(error))

    # ========================================================
    # PATCH EMPLOYEE
    # ========================================================

    elif operation == "Patch Employee":

        st.markdown(
            '<div class="operation-header">Patch Employee</div>',
            unsafe_allow_html=True,
        )

        st.info(
            "Use PATCH to change only the fields you select. "
            "Fields that are not selected remain unchanged."
        )

        with st.form("patch_employee_form"):

            employee_id = st.number_input(
                "Employee ID *",
                min_value=1,
                step=1,
                value=1,
            )

            st.markdown("#### Select fields to change")

            change_first_name = st.checkbox(
                "Change First Name"
            )

            first_name = None

            if change_first_name:
                first_name = st.text_input(
                    "New First Name",
                    placeholder="Enter new first name",
                )

            change_last_name = st.checkbox(
                "Change Last Name"
            )

            last_name = None

            if change_last_name:
                last_name = st.text_input(
                    "New Last Name",
                    placeholder="Enter new last name",
                )

            change_department = st.checkbox(
                "Change Department"
            )

            department_id = None

            if change_department:
                department_id = st.number_input(
                    "New Department ID",
                    min_value=1,
                    step=1,
                    value=1,
                )

            change_salary = st.checkbox(
                "Change Salary"
            )

            salary = None

            if change_salary:
                salary = st.number_input(
                    "New Salary",
                    min_value=0.0,
                    step=10000.0,
                    format="%.2f",
                )

            change_bonus = st.checkbox(
                "Change Bonus"
            )

            bonus = None

            if change_bonus:
                bonus = st.number_input(
                    "New Bonus",
                    min_value=0.0,
                    step=5000.0,
                    format="%.2f",
                )

            change_hire_date = st.checkbox(
                "Change Hire Date"
            )

            hire_date = None

            if change_hire_date:
                hire_date = st.date_input(
                    "New Hire Date",
                    value=date.today(),
                )

            submitted = st.form_submit_button(
                "Patch Employee",
                type="primary",
                use_container_width=True,
            )

        if submitted:

            data = {}

            if change_first_name:

                if not first_name or not first_name.strip():
                    st.error(
                        "First Name cannot be empty."
                    )
                else:
                    data["first_name"] = first_name.strip()

            if change_last_name:

                if not last_name or not last_name.strip():
                    st.error(
                        "Last Name cannot be empty."
                    )
                else:
                    data["last_name"] = last_name.strip()

            if change_department:
                data["department_id"] = int(department_id)

            if change_salary:
                data["salary"] = salary

            if change_bonus:
                data["bonus"] = bonus

            if change_hire_date:
                data["hire_date"] = str(hire_date)

            if not any([
                change_first_name,
                change_last_name,
                change_department,
                change_salary,
                change_bonus,
                change_hire_date,
            ]):

                st.error(
                    "Select at least one field to change."
                )

            elif (
                change_first_name
                and (not first_name or not first_name.strip())
            ):

                pass

            elif (
                change_last_name
                and (not last_name or not last_name.strip())
            ):

                pass

            else:

                try:

                    result = patch_employee(
                        int(employee_id),
                        data,
                    )

                    st.success(
                        "Employee updated successfully."
                    )

                    st.markdown("#### Response")

                    st.json(result)

                except Exception as error:

                    st.error(str(error))

    # ========================================================
    # DELETE EMPLOYEE
    # ========================================================

    elif operation == "Delete Employee":

        st.markdown(
            '<div class="operation-header">Delete Employee</div>',
            unsafe_allow_html=True,
        )

        employee_id = st.number_input(
            "Employee ID *",
            min_value=1,
            step=1,
            value=1,
        )

        st.warning(
            "This action permanently deletes the employee."
        )

        if st.button(
            "Delete Employee",
            type="primary",
            use_container_width=True,
        ):

            try:

                delete_employee(
                    int(employee_id)
                )

                st.success(
                    "Employee deleted successfully."
                )

            except Exception as error:

                st.error(str(error))


# ============================================================
# RIGHT SIDE — COMPENSATION REPORTS
# ============================================================

with right:

    st.markdown(
        '<div class="section-header">Compensation Reports</div>',
        unsafe_allow_html=True,
    )

    report = st.selectbox(
        "Select Report",
        [
            "Select a report",
            "Total Company Bonus",
            "Employees Without Bonus",
            "Bonus Percentage",
            "High Bonus Departments",
            "Bonus Ranking",
            "Highest Salary",
        ],
    )

    st.divider()


    # ========================================================
    # TOTAL BONUS
    # ========================================================

    if report == "Total Company Bonus":

        st.markdown(
            '<div class="operation-header">'
            "Total Company Bonus"
            "</div>",
            unsafe_allow_html=True,
        )

        st.info(
            "Calculates the total bonus paid across all employees."
        )

        if st.button(
            "Generate Report",
            type="primary",
            use_container_width=True,
        ):

            try:

                result = get_total_bonus()

                st.markdown("#### Result")

                st.metric(
                    "Total Company Bonus",
                    f"₹{result:,.2f}",
                )

            except Exception as error:

                st.error(str(error))


    # ========================================================
    # EMPLOYEES WITHOUT BONUS
    # ========================================================

    elif report == "Employees Without Bonus":

        st.markdown(
            '<div class="operation-header">'
            "Employees Without Bonus"
            "</div>",
            unsafe_allow_html=True,
        )

        st.info(
            "Shows employees whose bonus is NULL or zero."
        )

        if st.button(
            "Generate Report",
            type="primary",
            use_container_width=True,
        ):

            try:

                result = get_employees_without_bonus()

                st.markdown("#### Result")

                if result:
                    st.json(result)
                else:
                    st.success(
                        "All employees have a bonus."
                    )

            except Exception as error:

                st.error(str(error))


    # ========================================================
    # BONUS PERCENTAGE
    # ========================================================

    elif report == "Bonus Percentage":

        st.markdown(
            '<div class="operation-header">'
            "Bonus Percentage"
            "</div>",
            unsafe_allow_html=True,
        )

        st.info(
            "Calculates bonus as a percentage of base salary."
        )

        if st.button(
            "Generate Report",
            type="primary",
            use_container_width=True,
        ):

            try:

                result = get_bonus_percentage()

                st.markdown("#### Result")

                if result:
                    st.json(result)
                else:
                    st.info(
                        "No employees with a bonus were found."
                    )

            except Exception as error:

                st.error(str(error))


    # ========================================================
    # HIGH BONUS DEPARTMENTS
    # ========================================================

    elif report == "High Bonus Departments":

        st.markdown(
            '<div class="operation-header">'
            "High Bonus Departments"
            "</div>",
            unsafe_allow_html=True,
        )

        st.info(
            "Shows departments where total bonus exceeds "
            "the department's average salary."
        )

        if st.button(
            "Generate Report",
            type="primary",
            use_container_width=True,
        ):

            try:

                result = get_high_bonus_departments()

                st.markdown("#### Result")

                if result:
                    st.json(result)
                else:
                    st.info(
                        "No departments matched the criteria."
                    )

            except Exception as error:

                st.error(str(error))


    # ========================================================
    # BONUS RANKING
    # ========================================================

    elif report == "Bonus Ranking":

        st.markdown(
            '<div class="operation-header">'
            "Bonus Ranking"
            "</div>",
            unsafe_allow_html=True,
        )

        st.info(
            "Ranks employees by bonus, with employees "
            "having no bonus placed last."
        )

        if st.button(
            "Generate Report",
            type="primary",
            use_container_width=True,
        ):

            try:

                result = get_bonus_ranking()

                st.markdown("#### Result")

                if result:
                    st.json(result)
                else:
                    st.info(
                        "No employees found."
                    )

            except Exception as error:

                st.error(str(error))


    # ========================================================
    # HIGHEST SALARY
    # ========================================================

    elif report == "Highest Salary":

        st.markdown(
            '<div class="operation-header">'
            "Highest Salary"
            "</div>",
            unsafe_allow_html=True,
        )

        st.info(
            "Identifies the employee with the highest base "
            "salary and checks whether they also have the "
            "highest total compensation."
        )

        if st.button(
            "Generate Report",
            type="primary",
            use_container_width=True,
        ):

            try:

                result = get_highest_salary()

                if result:

                    st.markdown("#### Employee")

                    st.write(
                        f"**{result['first_name']} "
                        f"{result['last_name']}**"
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        st.metric(
                            "Base Salary",
                            f"₹{result['salary']:,.2f}",
                        )

                    with col2:

                        bonus = (
                            result["bonus"]
                            if result["bonus"] is not None
                            else 0
                        )

                        st.metric(
                            "Bonus",
                            f"₹{bonus:,.2f}",
                        )

                    st.metric(
                        "Total Compensation",
                        f"₹{result['total_compensation']:,.2f}",
                    )

                    if result[
                        "also_highest_total_compensation"
                    ]:

                        st.success(
                            "This employee also has the "
                            "highest total compensation."
                        )

                    else:

                        st.warning(
                            "This employee does not have the "
                            "highest total compensation."
                        )

                else:

                    st.info(
                        "No employees found."
                    )

            except Exception as error:

                st.error(str(error))