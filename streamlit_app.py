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
    st.title("Dependent Dropdowns Example")

    # Dropdown 1 (Cohort) - No selection by default
    cohort = st.selectbox("Select Cohort", options=[None] + list(data.keys()), index=0)

    # Dropdown 2 (LOB) - Dependent on Cohort
    if cohort:
        lob_options = [None] + list(data[cohort].keys())  # Add None for no selection
        lob = st.selectbox("Select LOB", options=lob_options, index=0)

        # Dropdown 3 (Sub-LOB) - Dependent on LOB
        if lob:
            sub_lob_options = [None] + data[cohort][lob]  # Add None for no selection
            sub_lob = st.selectbox("Select Sub-LOB", options=sub_lob_options, index=0)
        else:
            sub_lob = None
    else:
        lob = None
        sub_lob = None

    # Add the input boxes at the bottom
    st.subheader("Additional Information")

    # Input Box for MPAN# with placeholder text
    mpan = st.text_input("MPAN#", placeholder="Enter MPAN number")

    # Input Box for Account# with placeholder text
    account = st.text_input("Account#", placeholder="Enter Account number")

    # Ongoing/Completed Dropdown
    status = st.selectbox("Status", options=["Ongoing", "Completed"])

    # Submit Button
    submit_button = st.button("Submit")

    # Show success message when submit button is clicked
    if submit_button:
        # Check if all fields are filled
        if cohort and lob and sub_lob and mpan and account:
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

            # Display a success message
            st.success("You have successfully submitted the form. Thank you!")

            # Reset form fields (for next submit)
            st.experimental_rerun()
        else:
            st.error("Please fill the form completely.")

if __name__ == "__main__":
    app()
