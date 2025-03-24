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

    # Dropdown 1 (Cohort)
    cohort = st.selectbox("Select Cohort", options=list(data.keys()))
    
    # Dropdown 2 (LOB)
    lob_options = list(data[cohort].keys())
    lob = st.selectbox("Select LOB", options=lob_options)

    # Dropdown 3 (Sub-LOB)
    sub_lob_options = data[cohort][lob]
    sub_lob = st.selectbox("Select Sub-LOB", options=sub_lob_options)

    # Add the input boxes at the bottom
    st.subheader("Additional Information")

    # Input Box for MPAN#
    mpan = st.text_input("MPAN#", "Enter MPAN number")

    # Input Box for Account#
    account = st.text_input("Account#", "Enter Account number")

    # Display the values (optional, you can comment this out if you don't want to display them)
    # st.write(f"MPAN#: {mpan}")
    # st.write(f"Account#: {account}")

if __name__ == "__main__":
    app()
