import streamlit as st
import os

from database import (
    save_setting,
    get_setting,
    get_all_work_sessions,
    get_all_bills,
    DB_PATH
)

def get_float_setting(key, default):
    value = get_setting(key, default)

    try:
        return float(value)

    except (TypeError, ValueError):
        return float(default)


def get_bool_setting(key, default):
    value = get_setting(
        key,
        str(default)
    )

    return str(value).lower() == "true"


def show_settings_page():

    st.header("⚙️ Settings")

    st.write(
        "Customize your budgeting and delivery "
        "tracking preferences."
    )

    st.divider()

    default_app = get_setting(
        "default_app",
        "DoorDash"
    )

    track_mileage = get_bool_setting(
        "track_mileage",
        True
    )

    weekly_income_goal = get_float_setting(
        "weekly_income_goal",
        500
    )

    monthly_income_goal = get_float_setting(
        "monthly_income_goal",
        2000
    )

    target_hourly_rate = get_float_setting(
        "target_hourly_rate",
        25
    )

    st.subheader("🚗 Delivery Settings")

    with st.form("delivery_settings_form"):

        app_choices = [
            "DoorDash",
            "Uber Eats",
            "Both",
            "Other"
        ]

        if default_app in app_choices:

            default_index = app_choices.index(
                default_app
            )

        else:

            default_index = 0

        new_default_app = st.selectbox(
            "Default Delivery App",
            app_choices,
            index=default_index
        )

        new_track_mileage = st.checkbox(
            "Track mileage",
            value=track_mileage
        )

        st.caption(
            "Mileage can help you measure earnings per "
            "mile and understand how much driving your "
            "delivery work requires."
        )

        save_delivery = st.form_submit_button(
            "Save Delivery Settings",
            use_container_width=True
        )

    if save_delivery:

        save_setting(
            "default_app",
            new_default_app
        )

        save_setting(
            "track_mileage",
            new_track_mileage
        )

        st.success(
            "Delivery settings saved."
        )

        st.rerun()

    st.divider()

    st.subheader("🎯 Income Goals")

    st.write(
        "Set targets that we can eventually use throughout "
        "the dashboard and analytics pages."
    )

    with st.form("income_goal_settings"):

        new_weekly_goal = st.number_input(
            "Weekly Income Goal ($)",
            min_value=0.0,
            value=weekly_income_goal,
            step=50.0,
            format="%.2f"
        )

        new_monthly_goal = st.number_input(
            "Monthly Income Goal ($)",
            min_value=0.0,
            value=monthly_income_goal,
            step=100.0,
            format="%.2f"
        )

        new_hourly_target = st.number_input(
            "Target Earnings per Hour ($)",
            min_value=0.0,
            value=target_hourly_rate,
            step=1.0,
            format="%.2f"
        )

        save_goals = st.form_submit_button(
            "Save Income Goals",
            use_container_width=True
        )

    if save_goals:

        save_setting(
            "weekly_income_goal",
            new_weekly_goal
        )

        save_setting(
            "monthly_income_goal",
            new_monthly_goal
        )

        save_setting(
            "target_hourly_rate",
            new_hourly_target
        )

        st.success(
            "Income goals saved."
        )

        st.rerun()

    st.divider()

    st.subheader("📈 Current Targets")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Weekly Goal",
            f"${weekly_income_goal:.2f}"
        )

    with col2:

        st.metric(
            "Monthly Goal",
            f"${monthly_income_goal:.2f}"
        )

    with col3:

        st.metric(
            "Target $ / Hour",
            f"${target_hourly_rate:.2f}"
        )

    st.divider()

    st.subheader("💾 Local Data")

    sessions = get_all_work_sessions()
    bills = get_all_bills(
        active_only=False
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Saved Work Sessions",
            len(sessions)
        )

    with col2:

        st.metric(
            "Saved Bills",
            len(bills)
        )

    st.write(
        "**Database:** budget_tracker.db"
    )

    st.caption(
        "Your financial information is stored locally "
        "inside this SQLite database."
    )


    if os.path.exists(DB_PATH):

        database_size = os.path.getsize(
            DB_PATH
        )

        database_size_kb = (
            database_size / 1024
        )

        st.write(
            f"Database size: "
            f"**{database_size_kb:.2f} KB**"
        )


    st.warning(
        "The budget_tracker.db file contains your saved "
        "work sessions, bills, allocations, and settings. "
        "Deleting that file will remove your locally "
        "stored app data."
    )