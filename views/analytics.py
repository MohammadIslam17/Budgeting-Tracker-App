import streamlit as st
import pandas as pd

from database import get_all_work_sessions
from calculations import calculate_period_stats


def show_analytics_page():

    st.header("📊 Delivery Analytics")

    st.write(
        "Analyze your DoorDash and Uber Eats performance "
        "using your saved work sessions."
    )

    st.divider()

    sessions = get_all_work_sessions()

    if not sessions:
        st.info(
            "You don't have any work sessions yet. "
            "Add a work session to start seeing analytics."
        )
        return

    df = pd.DataFrame(sessions)

    df["date"] = pd.to_datetime(df["date"])

    st.subheader("Filters")

    col1, col2 = st.columns(2)

    with col1:

        app_options = ["All Apps"] + sorted(
            df["app_name"].dropna().unique().tolist()
        )

        selected_app = st.selectbox(
            "Delivery App",
            app_options
        )

    with col2:

        date_range = st.date_input(
            "Date Range",
            value=(
                df["date"].min().date(),
                df["date"].max().date()
            )
        )

    filtered_df = df.copy()

    if selected_app != "All Apps":

        filtered_df = filtered_df[
            filtered_df["app_name"] == selected_app
        ]

    if isinstance(date_range, (tuple, list)) and len(date_range) == 2:

        start_date = pd.Timestamp(date_range[0])
        end_date = pd.Timestamp(date_range[1])

        filtered_df = filtered_df[
            (filtered_df["date"] >= start_date)
            &
            (filtered_df["date"] <= end_date)
        ]

    if filtered_df.empty:

        st.warning(
            "No work sessions match the filters you selected."
        )
        return


    sessions_for_stats = filtered_df.to_dict("records")

    stats = calculate_period_stats(
        sessions_for_stats
    )

    st.divider()

    st.subheader("Performance Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Earnings",
            f"${stats['earnings']:.2f}"
        )

    with col2:
        st.metric(
            "Hours Worked",
            f"{stats['hours']:.2f}"
        )

    with col3:
        st.metric(
            "Trips",
            stats["trips"]
        )

    with col4:
        st.metric(
            "Miles",
            f"{stats['miles']:.1f}"
        )

    st.write("")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Average $ / Hour",
            f"${stats['hourly_rate']:.2f}"
        )

    with col2:
        st.metric(
            "Average $ / Trip",
            f"${stats['per_trip']:.2f}"
        )

    with col3:

        if stats["miles"] > 0:
            st.metric(
                "Average $ / Mile",
                f"${stats['per_mile']:.2f}"
            )
        else:
            st.metric(
                "Average $ / Mile",
                "N/A"
            )

    with col4:
        st.metric(
            "Trips / Hour",
            f"{stats['trips_per_hour']:.2f}"
        )

    st.divider()

    st.subheader("💵 Earnings by Day")

    daily_earnings = (
        filtered_df
        .groupby("date")["earnings"]
        .sum()
        .sort_index()
    )

    st.line_chart(
        daily_earnings
    )

    st.subheader("⏱️ Hours Worked by Day")

    daily_hours = (
        filtered_df
        .groupby("date")["hours"]
        .sum()
        .sort_index()
    )

    st.bar_chart(
        daily_hours
    )

    st.subheader("🚗 Trips by Day")

    daily_trips = (
        filtered_df
        .groupby("date")["trips"]
        .sum()
        .sort_index()
    )

    st.bar_chart(
        daily_trips
    )

    st.subheader("💰 Earnings per Hour by Day")

    daily_performance = (
        filtered_df
        .groupby("date")
        .agg({
            "earnings": "sum",
            "hours": "sum"
        })
    )

    daily_performance["earnings_per_hour"] = (
        daily_performance["earnings"]
        /
        daily_performance["hours"]
    )

    st.line_chart(
        daily_performance["earnings_per_hour"]
    )

    st.divider()

    st.subheader("📱 App Comparison")

    app_summary = (
        filtered_df
        .groupby("app_name")
        .agg({
            "earnings": "sum",
            "hours": "sum",
            "trips": "sum",
            "miles": "sum"
        })
        .reset_index()
    )

    app_summary["$/Hour"] = (
        app_summary["earnings"]
        /
        app_summary["hours"]
    ).round(2)

    app_summary["$/Trip"] = (
        app_summary["earnings"]
        /
        app_summary["trips"]
    ).round(2)

    app_summary["$/Mile"] = (
        app_summary["earnings"]
        /
        app_summary["miles"].replace(0, float("nan"))
    ).round(2)

    app_summary = app_summary.rename(
        columns={
            "app_name": "App",
            "earnings": "Earnings",
            "hours": "Hours",
            "trips": "Trips",
            "miles": "Miles"
        }
    )

    st.dataframe(
        app_summary,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Earnings by App")

    earnings_by_app = (
        filtered_df
        .groupby("app_name")["earnings"]
        .sum()
    )

    st.bar_chart(
        earnings_by_app
    )

    st.divider()

    st.subheader("🏆 Performance Highlights")

    daily_summary = (
        filtered_df
        .groupby("date")
        .agg({
            "earnings": "sum",
            "hours": "sum",
            "trips": "sum"
        })
    )

    daily_summary["hourly_rate"] = (
        daily_summary["earnings"]
        /
        daily_summary["hours"]
    )

    best_earning_day = daily_summary[
        "earnings"
    ].idxmax()

    best_earning_amount = daily_summary[
        "earnings"
    ].max()

    best_hourly_day = daily_summary[
        "hourly_rate"
    ].idxmax()

    best_hourly_rate = daily_summary[
        "hourly_rate"
    ].max()

    most_trips_day = daily_summary[
        "trips"
    ].idxmax()

    most_trips = daily_summary[
        "trips"
    ].max()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Highest Earning Day",
            f"${best_earning_amount:.2f}"
        )

        st.caption(
            best_earning_day.strftime(
                "%B %d, %Y"
            )
        )

    with col2:

        st.metric(
            "Best $ / Hour Day",
            f"${best_hourly_rate:.2f}"
        )

        st.caption(
            best_hourly_day.strftime(
                "%B %d, %Y"
            )
        )

    with col3:

        st.metric(
            "Most Trips in a Day",
            int(most_trips)
        )

        st.caption(
            most_trips_day.strftime(
                "%B %d, %Y"
            )
        )

    st.divider()

    st.subheader("📅 Day of Week Performance")

    filtered_df["day_of_week"] = (
        filtered_df["date"].dt.day_name()
    )

    day_summary = (
        filtered_df
        .groupby("day_of_week")
        .agg({
            "earnings": "sum",
            "hours": "sum",
            "trips": "sum"
        })
    )

    day_summary["$/Hour"] = (
        day_summary["earnings"]
        /
        day_summary["hours"]
    ).round(2)

    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    day_summary = day_summary.reindex(
        [
            day
            for day in day_order
            if day in day_summary.index
        ]
    )

    st.dataframe(
        day_summary,
        use_container_width=True
    )

    st.subheader("Average $ / Hour by Day of Week")

    st.bar_chart(
        day_summary["$/Hour"]
    )