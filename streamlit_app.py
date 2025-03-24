import streamlit as st
import pandas as pd
import os

# Data: Mapping Cohorts -> LOB -> Sub-LOB
data = {
    'Exception Management': {
        'HHDC': [
            'A Flag - No', 'A Flag - Yes', 'A Flag UKDC - Fuse - 8 AM & 2 PM',
            'ACCESS & VACANT Report', 'Change of MOP', 'Change of Supplier',
            'Check but no Main Data', 'CoMC', 'COP3 site without a check meter',
            'Creating day +3 & day+8 Report', 'Creating Dial failure Report', 'Creating Edits Report',
            'Creating R&C report', 'D+3.D+8', 'DF - BSCP / nhh/Sub/Spanish',
            'DF - Roaming', 'Dial Failures 93 ACCESS (new report)', 'EM vs FUSE',
            'Exception Management On-Hold (Pending)', 'HH Edits', 'HH Terminations report',
            'HT/HP Report (comms removed, open dial failure)', 'Intermittent process',
            'Main Vs Check Missing Gaps (Meter Exchange only)', 'No Open Action & Incomplete Cases',
            'Non Zero Estimations on a DE site', 'Open cases on de-energised sites',
            'R&C- manage outstanding - not Phased / Proving / Third Party / D0001 Loader',
            'Rejected D0002s', 'RTU Failure Report', 'Time Tolerance'
        ],
        'NHHDC': [
            'Received D0002s - Daily: NHH Faults', 'A Flag - Daily: NHH Faults', 
            'Change of MOP - Weekly: NHH Faults', 'Creating AM and PM A Flag Report (NHH)',
            'Creating received D0002 report', 'D0302 in MOP with Pending EDQ call - Weekly: NHH Faults',
            'EM v FUSE', 'NHH Dial Failures - Code 4: NHHDC', 'NHH Dial Failures - Non-Code 4: NHHDC',
            'NHH Intermittent Comms: NHH Faults', 'On Hold Calls - Daily: NHH Faults', 
            'Referred calls with no open action Daily task - Daily: NHH Faults', 'Rejected D0002 - Daily: NHH Faults',
            'Terminations report - NHH Faults', 'Time tolerance report - Weekly: NHH Faults'
        ]
    },
    'Metering': {
        'Meter Serv BW': [
            'Aborts - SMETS Install', 'Aborts - SMETS Site Investigation', 'D0002: HH', 
            'D0002: NHH', 'D0010: HH', 'D0010: NHH', 'D0131: HH', 'D0131: NHH', 
            'D0142: HH', 'D0142: NHH', 'D0149_D0150_D0313: NHH', 'D0149_D0150_D0313 Report Setup',
            'D0170: HH', 'D0170: NHH', 'D0170 Report Setup', 'D0223: HH', 'D0223: NHH',
            'D0223 Report Setup', 'D0291: HH', 'D0291: NHH', 'D0302 HH NHH', 'D0312: HH', 
            'D0312: NHH', 'D0312 Report Setup', 'D0367: NHH', 'D3045', 'SMETS - Install - Auto: NHH',
            'SMETS - Install - Manual: NHH', 'SMETS - Removals: NHH', 'SMETS D0005', 'SMETS D0005 Report Setup',
            'SMETS Emails'
        ]
    }
}

# Initialize session state for form data storage
if 'form_data' not in st.session_state:
    st.session_state.form_data = []

# Function to get the logged-in username
def get_username():
    try:
        # This will fetch the username of the current user on the machine
        return os.getlogin()
    except Exception as e:
        return f"Unknown ({e})"

# Streamlit app
def app():
    st.title("Dependent Dropdowns Example")

    # Initialize session state for multi-user form
    if 'cohort' not in st.session_state:
        st.session_state.cohort = ""
    if 'lob' not in st.session_state:
        st.session_state.lob = ""
    if 'sub_lob' not in st.session_state:
        st.session_state.sub_lob = ""
    if 'mpan' not in st.session_state:
        st.session_state.mpan = ""
    if 'account' not in st.session_state:
        st.session_state.account = ""
    if 'status' not in st.session_state:
        st.session_state.status = ""

    # Dropdown 1 (Cohort)
    cohort = st.selectbox("Select Cohort", options=[""] + list(data.keys()), index=0)
    st.session_state.cohort = cohort

    if cohort:
        # Dropdown 2 (LOB)
        lob_options = list(data[cohort].keys())
        lob = st.selectbox("Select LOB", options=[""] + lob_options, index=0)
        st.session_state.lob = lob

        if lob:
            # Dropdown 3 (Sub-LOB)
            sub_lob_options = data[cohort][lob]
            sub_lob = st.selectbox("Select Sub-LOB", options=[""] + sub_lob_options, index=0)
            st.session_state.sub_lob = sub_lob

    # Add the input boxes at the bottom
    st.subheader("Additional Information")

    # Input Box for MPAN# with placeholder text
    mpan = st.text_input("MPAN#", placeholder="Enter MPAN number")
    st.session_state.mpan = mpan

    # Input Box for Account# with placeholder text
    account = st.text_input("Account#", placeholder="Enter Account number")
    st.session_state.account = account

    # Ongoing/Completed Dropdown
    status = st.selectbox("Status", options=["", "Ongoing", "Completed"], index=0)
    st.session_state.status = status

    # Submit Button
    submit_button = st.button("Submit")

    # Validation before submit
    if submit_button:
        if not cohort or not lob or not sub_lob or not mpan or not account or not status:
            st.error("Please fill the form completely before submitting.")
        else:
            # Get the logged-in username
            username = get_username()

            # Add the form data to session state, including the username
            form_entry = {
                "Cohort": cohort,
                "LOB": lob,
                "Sub-LOB": sub_lob,
                "MPAN": mpan,
                "Account": account,
                "Status": status,
                "Submitted By": username  # Add username to the form data
            }
            st.session_state.form_data.append(form_entry)

            # Reset the form after submission
            st.session_state.cohort = ""
            st.session_state.lob = ""
            st.session_state.sub_lob = ""
            st.session_state.mpan = ""
            st.session_state.account = ""
            st.session_state.status = ""

            # Show success message after submission
            st.success("Form submitted successfully. Thank you!")

            # Offer to download the CSV file
            if len(st.session_state.form_data) > 0:
                df = pd.DataFrame(st.session_state.form_data)
                # Convert the DataFrame to CSV
                csv = df.to_csv(index=False)

                # Create a download link for the CSV
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="form_data.csv",
                    mime="text/csv"
                )

if __name__ == "__main__":
    app()
