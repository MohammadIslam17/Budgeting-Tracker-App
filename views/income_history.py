import streamlit as st
import pandas as pd

from datetime import date

from database import (
    get_all_work_sessions,
    update_work_session,
    delete_work_session,
    session_has_allocations
)

from calculations import calculate_shift_stats

def show_income_history_page():

    st.header("📋 Income History")

    st.write(
        "View, filter, edit, and manage your saved "
        "DoorDash and Uber Eats work sessions."
    )

    st.divider()

    sessions = get_all_work_sessions()

    if not sessions:

        st.info(
            "You haven't recorded any work sessions yet."
        )

        return

    df = pd.DataFrame(sessions)

    df["date"] = pd.to_datetime(
        df["date"]
    )

    st.subheader("Filters")

    col1, col2 = st.columns(2)

    with col1:

        app_options = ["All Apps"] + sorted(
            df["app_name"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_app = st.selectbox(
            "Delivery App",
            app_options,
            key="history_app_filter"
        )

    with col2:

        date_range = st.date_input(
            "Date Range",
            value=(
                df["date"].min().date(),
                df["date"].max().date()
            ),
            key="history_date_filter"
        )


    filtered_df = df.copy()

    if selected_app != "All Apps":

        filtered_df = filtered_df[
            filtered_df["app_name"]
            == selected_app
        ]

    if (
        isinstance(date_range, (tuple, list))
        and len(date_range) == 2
    ):

        start_date = pd.Timestamp(
            date_range[0]
        )

        end_date = pd.Timestamp(
            date_range[1]
        )

        filtered_df = filtered_df[
            (filtered_df["date"] >= start_date)
            &
            (filtered_df["date"] <= end_date)
        ]

    if filtered_df.empty:

        st.warning(
            "No work sessions match your selected filters."
        )

        return

    st.divider()

    st.subheader("History Summary")

    total_earnings = filtered_df[
        "earnings"
    ].sum()

    total_hours = filtered_df[
        "hours"
    ].sum()

    total_trips = filtered_df[
        "trips"
    ].sum()

    total_miles = filtered_df[
        "miles"
    ].sum()

    hourly_rate = 0
    per_trip = 0

    if total_hours > 0:

        hourly_rate = (
            total_earnings
            /
            total_hours
        )

    if total_trips > 0:

        per_trip = (
            total_earnings
            /
            total_trips
        )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Earnings",
            f"${total_earnings:.2f}"
        )

    with col2:

        st.metric(
            "Hours",
            f"{total_hours:.2f}"
        )

    with col3:

        st.metric(
            "Trips",
            int(total_trips)
        )

    with col4:

        st.metric(
            "$ / Hour",
            f"${hourly_rate:.2f}"
        )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "$ / Trip",
            f"${per_trip:.2f}"
        )

    with col2:

        st.metric(
            "Miles",
            f"{total_miles:.1f}"
        )

    st.divider()

    st.subheader("Work Sessions")

    display_df = filtered_df.copy()

    display_df["$/Hour"] = (
        display_df["earnings"]
        /
        display_df["hours"].replace(0, float("nan"))
    ).round(2)

    display_df["$/Trip"] = (
        display_df["earnings"]
        /
        display_df["trips"].replace(0, float("nan"))
    ).round(2)

    display_df["$/Mile"] = (
        display_df["earnings"]
        /
        display_df["miles"].replace(0, float("nan"))
    ).round(2)

    display_df["date"] = (
        display_df["date"]
        .dt.strftime("%Y-%m-%d")
    )

    display_df = display_df.rename(
        columns={
            "date": "Date",
            "app_name": "App",
            "earnings": "Earnings",
            "hours": "Hours",
            "trips": "Trips",
            "miles": "Miles",
            "notes": "Notes"
        }
    )

    columns_to_show = [
        "Date",
        "App",
        "Earnings",
        "Hours",
        "Trips",
        "Miles",
        "$/Hour",
        "$/Trip",
        "$/Mile",
        "Notes"
    ]

    st.dataframe(
        display_df[columns_to_show],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Earnings": st.column_config.NumberColumn(
                "Earnings",
                format="$%.2f"
            ),
            "$/Hour": st.column_config.NumberColumn(
                "$/Hour",
                format="$%.2f"
            ),
            "$/Trip": st.column_config.NumberColumn(
                "$/Trip",
                format="$%.2f"
            ),
            "$/Mile": st.column_config.NumberColumn(
                "$/Mile",
                format="$%.2f"
            )
        }
    )

    st.divider()

    st.subheader("Manage Work Sessions")

    st.write(
        "Select a work session below to view its "
        "details or make changes."
    )

    filtered_df = filtered_df.sort_values(
        by=["date", "id"],
        ascending=False
    )

    session_options = {}

    for _, row in filtered_df.iterrows():

        session_date = row["date"].strftime(
            "%B %d, %Y"
        )

        label = (
            f"{session_date} — "
            f"{row['app_name']} — "
            f"${row['earnings']:.2f}"
        )

        session_options[label] = int(
            row["id"]
        )

    selected_label = st.selectbox(
        "Select Work Session",
        list(session_options.keys())
    )

    selected_session_id = (
        session_options[selected_label]
    )

    selected_session = next(
        session
        for session in sessions
        if session["id"] == selected_session_id
    )

    stats = calculate_shift_stats(
        earnings=selected_session["earnings"],
        hours=selected_session["hours"],
        trips=selected_session["trips"],
        miles=selected_session["miles"]
    )

    st.write("")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Earnings",
            f"${stats['earnings']:.2f}"
        )

    with col2:

        st.metric(
            "$ / Hour",
            f"${stats['hourly_rate']:.2f}"
        )

    with col3:

        st.metric(
            "$ / Trip",
            f"${stats['per_trip']:.2f}"
        )

    with col4:

        if stats["miles"] > 0:

            st.metric(
                "$ / Mile",
                f"${stats['per_mile']:.2f}"
            )

        else:

            st.metric(
                "$ / Mile",
                "N/A"
            )

    with st.expander(
        "✏️ Edit Work Session"
    ):

        original_date = date.fromisoformat(
            selected_session["date"]
        )

        edit_date = st.date_input(
            "Date",
            value=original_date,
            key=f"edit_date_{selected_session_id}"
        )

        edit_app = st.selectbox(
            "Delivery App",
            [
                "DoorDash",
                "Uber Eats",
                "Both",
                "Other"
            ],
            index=(
                [
                    "DoorDash",
                    "Uber Eats",
                    "Both",
                    "Other"
                ].index(
                    selected_session["app_name"]
                )
                if selected_session["app_name"]
                in [
                    "DoorDash",
                    "Uber Eats",
                    "Both",
                    "Other"
                ]
                else 3
            ),
            key=f"edit_app_{selected_session_id}"
        )

        edit_earnings = st.number_input(
            "Earnings",
            min_value=0.01,
            value=float(
                selected_session["earnings"]
            ),
            step=1.00,
            key=f"edit_earnings_{selected_session_id}"
        )

        edit_hours = st.number_input(
            "Hours",
            min_value=0.01,
            value=float(
                selected_session["hours"]
            ),
            step=0.25,
            key=f"edit_hours_{selected_session_id}"
        )

        edit_trips = st.number_input(
            "Trips",
            min_value=1,
            value=int(
                selected_session["trips"]
            ),
            step=1,
            key=f"edit_trips_{selected_session_id}"
        )

        edit_miles = st.number_input(
            "Miles",
            min_value=0.0,
            value=float(
                selected_session["miles"]
            ),
            step=1.0,
            key=f"edit_miles_{selected_session_id}"
        )

        edit_notes = st.text_area(
            "Notes",
            value=(
                selected_session["notes"]
                or ""
            ),
            key=f"edit_notes_{selected_session_id}"
        )

        has_allocations = session_has_allocations(
            selected_session_id
        )

        if has_allocations:

            st.warning(
                "This work session has already contributed "
                "money toward one or more bills. Editing the "
                "earnings will not automatically recalculate "
                "those previous bill allocations yet."
            )

        if st.button(
            "Save Changes",
            key=f"save_session_{selected_session_id}",
            use_container_width=True
        ):

            update_work_session(
                session_id=selected_session_id,
                date=edit_date.isoformat(),
                app_name=edit_app,
                earnings=edit_earnings,
                hours=edit_hours,
                trips=edit_trips,
                miles=edit_miles,
                notes=edit_notes
            )

            st.success(
                "Work session updated successfully!"
            )

            st.rerun()

    with st.expander(
        "🗑️ Delete Work Session"
    ):

        if session_has_allocations(
            selected_session_id
        ):

            st.warning(
                "This session has money allocated toward "
                "bills, so it cannot safely be deleted yet."
            )

            st.caption(
                "We'll add allocation reversal so deleting "
                "a session also removes the money it "
                "contributed to your bills."
            )

        else:

            st.warning(
                "Deleting a work session is permanent."
            )

            confirm_delete = st.checkbox(
                "I understand that this session will be deleted.",
                key=f"confirm_delete_{selected_session_id}"
            )

            if st.button(
                "Delete Work Session",
                key=f"delete_session_{selected_session_id}",
                disabled=not confirm_delete,
                use_container_width=True
            ):

                delete_work_session(
                    selected_session_id
                )

                st.success(
                    "Work session deleted."
                )

                st.rerun()