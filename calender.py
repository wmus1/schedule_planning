import streamlit as st
import pandas as pd

# Initialize session state to hold employees and schedules
if "employees" not in st.session_state:
    st.session_state["employees"] = []
if "schedules" not in st.session_state:
    st.session_state["schedules"] = pd.DataFrame(columns=["Employee", "Date", "Start Time", "End Time"])

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
            start_time = st.time_input("Start Time")
            end_time = st.time_input("End Time")
            create_schedule_button = st.form_submit_button("Create Schedule")
            
            if create_schedule_button:
                if start_time >= end_time:
                    st.error("End time must be later than start time.")
                else:
                    new_schedule = {
                        "Employee": employee,
                        "Date": date,
                        "Start Time": start_time,
                        "End Time": end_time,
                    }
                    st.session_state["schedules"] = pd.concat(
                    [st.session_state["schedules"], pd.DataFrame([new_schedule])],
                    ignore_index=True,
                    )
                    st.success(f"Scheduled {employee} on {date} from {start_time} to {end_time}.")

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
