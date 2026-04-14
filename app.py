import streamlit as st
import pandas as pd
import os
import uuid # لإصدار ID فريد لكل موظف

# Configuration
FILE_NAME = "hotel_management.xlsx"

# Page styling
st.set_page_config(page_title="Hotel Recruitment System", layout="wide")

# Function to save data
def save_data(data):
    if os.path.isfile(FILE_NAME):
        df_existing = pd.read_excel(FILE_NAME)
        df_new = pd.DataFrame([data])
        df_final = pd.concat([df_existing, df_new], ignore_index=True)
        df_final.to_excel(FILE_NAME, index=False)
    else:
        df = pd.DataFrame([data])
        df.to_excel(FILE_NAME, index=False)

# --- Sidebar Navigation ---
st.sidebar.title("🏨 Novotal")
page = st.sidebar.radio("Go to:", ["Job Application", "Admin Dashboard"])

# --- PAGE 1: Job Application ---
if page == "Job Application":
    st.title("🏨 International Hotel - Job Portal")
    st.info("Please fill out the form below to apply for a position.")

    with st.container():
        with st.form("application_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                employee_id = st.text_input("Employee ID ")
                name = st.text_input("Full Name")
                email = st.text_input("Email Address")
                position = st.selectbox("Desired Position", 
                                     ["Receptionist", "Housekeeping", "Manager", "Kitchen Staff", "IT Support"])
            
            with col2:
                phone = st.text_input("Phone Number")
                experience = st.number_input("Years of Experience", min_value=0, max_value=40)
                
            notes = st.text_area("Additional Professional Summary")
            
            submit = st.form_submit_button("Submit Application")

            if submit:
                if name and phone:
                    # Use provided ID or generate a unique one
                    if employee_id.strip():
                        applicant_id = employee_id.strip().upper()
                    else:
                        applicant_id = str(uuid.uuid4())[:8].upper()
                    
                    data = {
                        "Employee ID": applicant_id,
                        "Name": name,
                        "Phone": phone,
                        "Email": email,
                        "Position": position,
                        "Experience": experience,
                        "Notes": notes
                    }
                    save_data(data)
                    st.success(f"Successfully Submitted! Your Application ID is: **{applicant_id}**")
                else:
                    st.warning("Please fill in the required fields (Name & Phone).")

# --- PAGE 2: Admin Dashboard ---
elif page == "Admin Dashboard":
    st.title("📊 Admin Control Panel")
    
    if os.path.isfile(FILE_NAME):
        df = pd.read_excel(FILE_NAME)
        
        # Dashboard Stats
        st.write("### Quick Stats")
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Total Applicants", len(df))
        kpi2.metric("Most Wanted Job", df['Position'].mode()[0] if not df.empty else "N/A")
        kpi3.metric("Avg. Experience", f"{df['Experience'].mean():.1f} Years" if not df.empty else "0")

        st.divider()
        
        # Advanced Search
        search = st.text_input("🔍 Search by ID, Name, or Position")
        if search:
            results = df[df.apply(lambda row: search.lower() in row.astype(str).str.lower().values, axis=1)]
            st.dataframe(results, use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)
            
        # Download button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export to CSV", data=csv, file_name="applicants_report.csv", mime="text/csv")
    else:
        st.info("No applications received yet.")
        