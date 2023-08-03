import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
from st_aggrid import AgGrid,GridOptionsBuilder,GridUpdateMode
import plotly.graph_objects as go


names = ["Anusha P", "Satya"]
usernames = ["polaki", "anusha"]
passwords = ["abc", "abc"]
hashed_passwords = stauth.Hasher(passwords).generate()

credentials = {
    'usernames': {username: {'name': name, 'password': hashed_password} for username, name, hashed_password in zip(usernames, names, hashed_passwords)}
}
cookie_name = "streamlit"
cookie_key = "abc"

authenticator = stauth.Authenticate(credentials, cookie_name, cookie_key,cookie_expiry_days=0)

name, authentication_status, username = authenticator.login('Login', 'main')

if st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')
if st.session_state["authentication_status"] == None:
    st.warning('Please enter your username and password')

if st.session_state["authentication_status"]:

    st.title('Bacardi Demand Forecasting')

    df=pd.read_excel('scenarios.xlsx')
    gd = GridOptionsBuilder.from_dataframe(df)
    gd.configure_selection(selection_mode='multiple', use_checkbox=True)
    gridoptions = gd.build()

    grid_table = AgGrid(df, height=250, gridOptions=gridoptions,update_mode=GridUpdateMode.SELECTION_CHANGED,allow_unsafe_jscode=True,
                            theme='streamlit')

    selected_row = grid_table["selected_rows"]

    if selected_row:

        new_df=pd.DataFrame(selected_row)
        new_df = new_df[["Name", "revenue", "cost", "profit"]]
        numeric_columns = ["revenue", "cost", "profit"]

        st.markdown("Comparison of Selected Scenarios")

        fig = go.Figure()
        for col in numeric_columns:
            fig.add_trace(go.Bar(x=new_df['Name'],y=new_df[col]))

        fig.update_layout(
                xaxis_title="Name",
                yaxis_title="Amount",
                title="Scenario Comparison")

        st.plotly_chart(fig)
    else:
        st.write("Select rows to display the plot.")



