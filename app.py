import streamlit as st
from views.dashboard import show_dashboard_page
from views.add_income import show_add_income_page
from views.income_history import show_income_history_page
from views.bills import show_bills_page
from views.analytics import show_analytics_page
from views.settings import show_settings_page


st.set_page_config(
    page_title="Delivery Finance",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("💰 Delivery Finance")

st.caption(
    "Track your DoorDash and Uber Eats income, "
    "analyze your driving performance, and manage your bills."
)

st.divider()

with st.sidebar:

    st.header("💰 Delivery Finance")

    st.write(
        "Manage your income and financial goals."
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Add Work Session",
            "Income History",
            "Bills & Goals",
            "Analytics",
            "Settings"
        ]
    )

    st.divider()

    st.caption(
        "Local Financial Management System"
    )

if page == "Dashboard":

    show_dashboard_page()


elif page == "Add Work Session":

    show_add_income_page()


elif page == "Income History":

    show_income_history_page()


elif page == "Bills & Goals":

    show_bills_page()


elif page == "Analytics":

    show_analytics_page()


elif page == "Settings":

    show_settings_page()