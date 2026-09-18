import streamlit as st
import pandas as pd

from datetime import date, timedelta

from database import (
    get_all_work_sessions,
    get_all_bills
)

from calculations import (
    calculate_period_stats,
    calculate_bill_progress,
    calculate_bill_remaining,
    calculate_days_until_due
)


def show_dashboard_page():

    st.header("🏠 Financial Dashboard")

    st.write(
        "Your delivery income, performance, and bill progress "
        "all in one place."
    )

    st.divider()


    sessions = get_all_work_sessions()
    bills = get_all_bills()

    today = date.today()

    # Monday of current week
    start_of_week = today - timedelta(
        days=today.weekday()
    )


    end_of_week = start_of_week + timedelta(
        days=6
    )

    if sessions:

        df = pd.DataFrame(sessions)

        df["date"] = pd.to_datetime(
            df["date"]
        ).dt.date

        today_df = df[
            df["date"] == today
        ]

        week_df = df[
            (df["date"] >= start_of_week)
            &
            (df["date"] <= end_of_week)
        ]

        today_sessions = today_df.to_dict(
            "records"
        )

        week_sessions = week_df.to_dict(
            "records"
        )

    else:

        df = pd.DataFrame()

        today_sessions = []
        week_sessions = []

    today_stats = calculate_period_stats(
        today_sessions
    )

    week_stats = calculate_period_stats(
        week_sessions
    )

    st.subheader("☀️ Today")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Earnings",
            f"${today_stats['earnings']:.2f}"
        )

    with col2:

        st.metric(
            "Hours",
            f"{today_stats['hours']:.2f}"
        )

    with col3:

        st.metric(
            "Trips",
            today_stats["trips"]
        )

    with col4:

        st.metric(
            "$ / Hour",
            f"${today_stats['hourly_rate']:.2f}"
        )

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "$ / Trip",
            f"${today_stats['per_trip']:.2f}"
        )

    with col2:

        if today_stats["miles"] > 0:

            st.metric(
                "$ / Mile",
                f"${today_stats['per_mile']:.2f}"
            )

        else:

            st.metric(
                "$ / Mile",
                "N/A"
            )

    with col3:

        st.metric(
            "Miles",
            f"{today_stats['miles']:.1f}"
        )

    st.divider()

    st.subheader("📅 This Week")

    st.caption(
        f"{start_of_week.strftime('%B %d')} - "
        f"{end_of_week.strftime('%B %d, %Y')}"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Weekly Earnings",
            f"${week_stats['earnings']:.2f}"
        )

    with col2:

        st.metric(
            "Weekly Hours",
            f"{week_stats['hours']:.2f}"
        )

    with col3:

        st.metric(
            "Weekly Trips",
            week_stats["trips"]
        )

    with col4:

        st.metric(
            "Weekly $ / Hour",
            f"${week_stats['hourly_rate']:.2f}"
        )

    if week_sessions:

        st.write("")

        st.subheader("Weekly Earnings")

        chart_df = week_df.copy()

        daily_earnings = (
            chart_df
            .groupby("date")["earnings"]
            .sum()
        )

        week_dates = [
            start_of_week + timedelta(days=i)
            for i in range(7)
        ]

        daily_earnings = daily_earnings.reindex(
            week_dates,
            fill_value=0
        )

        daily_earnings.index = [
            day.strftime("%a")
            for day in daily_earnings.index
        ]

        st.bar_chart(
            daily_earnings
        )

    else:

        st.info(
            "No work sessions have been recorded "
            "for this week yet."
        )

    st.divider()

    st.subheader("💳 Bills & Financial Goals")

    if not bills:

        st.info(
            "You haven't created any bills yet. "
            "Go to Bills & Goals to create your first one."
        )

    else:

        total_bill_amount = sum(
            bill["amount"]
            for bill in bills
        )

        total_saved = sum(
            bill["saved_amount"]
            for bill in bills
        )

        total_remaining = max(
            total_bill_amount - total_saved,
            0
        )

        total_progress = 0

        if total_bill_amount > 0:

            total_progress = (
                total_saved
                /
                total_bill_amount
            ) * 100

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total Bills",
                f"${total_bill_amount:.2f}"
            )

        with col2:

            st.metric(
                "Saved Toward Bills",
                f"${total_saved:.2f}"
            )

        with col3:

            st.metric(
                "Still Needed",
                f"${total_remaining:.2f}"
            )

        st.write("")

        st.write(
            f"**Overall Funding Progress: "
            f"{total_progress:.1f}%**"
        )

        st.progress(
            min(total_progress / 100, 1.0)
        )

        st.write("")

        st.subheader("Bill Progress")

        # Sort bills by due date
        sorted_bills = sorted(
            bills,
            key=lambda bill: (
                bill["due_date"]
                if bill["due_date"]
                else "9999-12-31"
            )
        )

        for bill in sorted_bills:

            name = bill["name"]
            amount = bill["amount"]
            saved = bill["saved_amount"]

            progress = calculate_bill_progress(
                saved,
                amount
            )

            remaining = calculate_bill_remaining(
                saved,
                amount
            )

            try:

                due_date = date.fromisoformat(
                    bill["due_date"]
                )

                days_left = calculate_days_until_due(
                    due_date
                )

            except (ValueError, TypeError):

                due_date = None
                days_left = None

            with st.container(border=True):

                col1, col2 = st.columns(
                    [3, 1]
                )

                with col1:

                    st.write(
                        f"### {name}"
                    )

                    st.write(
                        f"${saved:.2f} of "
                        f"${amount:.2f}"
                    )

                with col2:

                    st.metric(
                        "Remaining",
                        f"${remaining:.2f}"
                    )

                st.progress(
                    min(progress / 100, 1.0)
                )

                st.caption(
                    f"{progress:.1f}% funded"
                )

                if remaining <= 0:

                    st.success(
                        "Fully funded!"
                    )

                elif due_date:

                    if due_date < today:

                        st.error(
                            f"Past due — "
                            f"${remaining:.2f} still needed."
                        )

                    elif due_date == today:

                        st.warning(
                            f"Due today — "
                            f"${remaining:.2f} still needed."
                        )

                    else:

                        st.write(
                            f"Due "
                            f"{due_date.strftime('%B %d, %Y')} "
                            f"— {days_left} days remaining"
                        )

    if bills:

        st.divider()

        st.subheader("💰 Income Allocation Plan")

        total_allocation_percentage = sum(
            bill["allocation_percentage"]
            for bill in bills
        )

        remaining_percentage = max(
            100 - total_allocation_percentage,
            0
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Allocated to Bills",
                f"{total_allocation_percentage:.1f}%"
            )

        with col2:

            st.metric(
                "Unallocated",
                f"{remaining_percentage:.1f}%"
            )

        st.write(
            "For every **$100** you earn:"
        )

        for bill in bills:

            amount_per_100 = (
                bill["allocation_percentage"]
            )

            st.write(
                f"**{bill['name']}:** "
                f"${amount_per_100:.2f}"
            )

        if remaining_percentage > 0:

            st.write(
                f"**Remaining:** "
                f"${remaining_percentage:.2f}"
            )

    st.divider()

    st.subheader("🕒 Recent Work Sessions")

    if sessions:

        recent_sessions = sessions[:5]

        for session in recent_sessions:

            earnings = session["earnings"]
            hours = session["hours"]
            trips = session["trips"]

            hourly_rate = 0

            if hours > 0:

                hourly_rate = (
                    earnings / hours
                )

            with st.container(border=True):

                col1, col2, col3, col4 = (
                    st.columns(4)
                )

                with col1:

                    st.write(
                        f"**{session['app_name']}**"
                    )

                    st.caption(
                        session["date"]
                    )

                with col2:

                    st.metric(
                        "Earnings",
                        f"${earnings:.2f}"
                    )

                with col3:

                    st.metric(
                        "Trips",
                        trips
                    )

                with col4:

                    st.metric(
                        "$ / Hour",
                        f"${hourly_rate:.2f}"
                    )

    else:

        st.info(
            "No work sessions have been recorded yet."
        )