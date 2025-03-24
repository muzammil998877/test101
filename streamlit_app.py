import streamlit as st

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

# Streamlit app
def app():
    # Title of the app
    st.title("Dependent Dropdowns Example")

    # Add session state to handle resetting the form
    if "form_submitted" not in st.session_state:
        st.session_state.form_submitted = False
        st.session_state.mpan = ""
        st.session_state.account = ""
        st.session_state.cohort = ""
        st.session_state.lob = ""
        st.session_state.sub_lob = ""

    # Reset the form after submission
    if st.session_state.form_submitted:
        st.session_state.mpan = ""
        st.session_state.account = ""
        st.session_state.cohort = ""
        st.session_state.lob = ""
        st.session_state.sub_lob = ""
        st.session_state.form_submitted = False
        st.experimental_rerun()  # Force a reset of the app after form submission

    # Dropdown 1 (Cohort)
    cohort = st.selectbox("Select Cohort", options=list(data.keys()), key="cohort")

    # If Cohort is selected, populate LOB dropdown
    if cohort:
        lob_options = list(data[cohort].keys())
        lob = st.selectbox("Select LOB", options=lob_options, key="lob")
    else:
        lob = ""

    # If LOB is selected, populate Sub-LOB dropdown
    if lob:
        sub_lob_options = data[cohort][lob]
        sub_lob = st.selectbox("Select Sub-LOB", options=sub_lob_options, key="sub_lob")
    else:
        sub_lob = ""

    # Add the input boxes at the bottom
    st.subheader("Additional Information")

    # Input Box for MPAN# with placeholder text
    mpan = st.text_input("MPAN#", placeholder="Enter MPAN number", value=st.session_state.mpan)

    # Input Box for Account# with placeholder text
    account = st.text_input("Account#", placeholder="Enter Account number", value=st.session_state.account)

    # Ongoing/Completed Dropdown
    status = st.selectbox("Status", options=["Ongoing", "Completed"])

    # Submit Button
    submit_button = st.button("Submit")

    # Show success message when submit button is clicked
    if submit_button:
        # Validation: Ensure all fields are filled
        if not mpan or not account or not cohort or not lob or not sub_lob:
            st.error("Please fill in all the fields to complete the form.")
        else:
            # Change the button color to green using custom styling
            st.markdown("""
                <style>
                .stButton>button {
                    background-color: #4CAF50; 
                    color: white;
                    border: none;
                }
                </style>
                """, unsafe_allow_html=True)

            # Display a success message (this simulates a popup-like behavior)
            st.success("You have successfully submitted the form. Thank you!")

            # Store the values in session state to keep track of the submission
            st.session_state.form_submitted = True
            st.session_state.mpan = mpan
            st.session_state.account = account
            st.session_state.cohort = cohort
            st.session_state.lob = lob
            st.session_state.sub_lob = sub_lob

if __name__ == "__main__":
    app()
