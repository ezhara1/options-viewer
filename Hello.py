import streamlit as st
from datetime import date
from thetadata import ThetaClient, OptionReqType, OptionRight, DateRange, SecType

# Initialize the ThetaClient (assuming it doesn't require authentication for simplicity)
client = ThetaClient()

# Sidebar: Symbol Selection
with client.connect():
    symbols = client.get_roots(SecType.OPTION)
symbol = st.sidebar.selectbox("Select Symbol", symbols)

# Sidebar: Expiration Date Selection based on selected Symbol
with client.connect():
    expirations = client.get_expirations(symbol)
expiration = st.sidebar.selectbox("Select Expiration Date", expirations)

# Sidebar: Strike Price Selection based on selected Symbol and Expiration Date
with client.connect():
    strikes = client.get_strikes(symbol, expiration)
strike = st.sidebar.selectbox("Select Strike Price", strikes)

# Sidebar: Date Range Selection for Historical Data
start_date = st.sidebar.date_input("Start Date", date(2023, 12, 1))
end_date = st.sidebar.date_input("End Date", date.today())

#provide code to assign default values to symbols = META, expirations = 2024-03-15, strikes = 800 if the user does not select any value
if symbol == None:
    symbol = 'META'
if expiration == None:
    expiration = '2024-03-15'
if strike == None:
    strike = 800


# Display Historical Option Data based on selections
with client.connect():
    data_details = client.get_hist_option(
        req=OptionReqType.EOD,
        root=symbol,
        exp=expiration,
        strike=strike,
        right=OptionRight.CALL,  # Assuming CALL for simplicity, adjust as needed
        date_range=DateRange(start_date, end_date)
    )

# Main window: Show the DataFrame
st.dataframe(data_details)
