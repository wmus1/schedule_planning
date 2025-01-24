import streamlit as st
import pandas as pd

# Initialize session state to hold employees and schedules
if "employees" not in st.session_state:
    st.session_state["employees"] = []
if "schedules" not in st.session_state:
    st.session_state["schedules"] = pd.DataFrame(columns=["Employee", "Date", "Shift"])

# Sidebar for navigation
st.sidebar.title("Employee Scheduler")
menu = st.sidebar.radio("Menu", ["Add Employees", "Create Schedule", "View Schedule"])

# Add Employees Page
if menu == "Add Employees":
    st.title("Add Employees")

    with st.form("add_employee_form"):
        name = st.text_input("Employee Name")
        role = st.text_input("Role (e.g., Manager, Developer, etc.)")
        add_employee_button = st.form_submit_button("Add Employee")

        if add_employee_button:
            if name:
                st.session_state["employees"].append({"Name": name, "Role": role})
                st.success(f"Added {name} as {role}")
            else:
                st.error("Employee name cannot be empty.")

    # Display current employees
    st.subheader("Current Employees")
    if st.session_state["employees"]:
        employees_df = pd.DataFrame(st.session_state["employees"])
        st.table(employees_df)
    else:
        st.write("No employees added yet.")

# Create Schedule Page
elif menu == "Create Schedule":
    st.title("Create Schedule")

    if not st.session_state["employees"]:
        st.warning("Please add employees first!")
    else:
        employee_names = [emp["Name"] for emp in st.session_state["employees"]]

        with st.form("schedule_form"):
            employee = st.selectbox("Select Employee", employee_names)
            date = st.date_input("Select Date")

            # Define the two 12-hour shifts
            shift_options = ["Day Shift (:700 AM - 7:00 PM)", "Night Shift (7:00 PM - 7:00 AM)"]
            shift = st.selectbox("Select Shift", shift_options)  # Let the user choose a shift

            create_schedule_button = st.form_submit_button("Create Schedule")

            if create_schedule_button:
                new_schedule = {
                    "Employee": employee,
                    "Date": date,
                    "Shift": shift,  # Store the selected shift
                }
                st.session_state["schedules"] = pd.concat(
                    [st.session_state["schedules"], pd.DataFrame([new_schedule])],
                    ignore_index=True,
                )
                st.success(f"Scheduled {employee} on {date} for {shift}.")

# View Schedule Page
elif menu == "View Schedule":
    st.title("View Schedule")

    if st.session_state["schedules"].empty:
        st.write("No schedules created yet.")
    else:
        st.dataframe(st.session_state["schedules"])

        # Download as CSV
        csv_data = st.session_state["schedules"].to_csv(index=False)
        st.download_button(
            label="Download Schedule as CSV",
            data=csv_data,
            file_name="employee_schedule.csv",
            mime="text/csv",
        )
