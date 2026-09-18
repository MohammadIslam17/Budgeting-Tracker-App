import streamlit as st
from datetime import date

from database import add_work_session, get_all_bills, add_bill_allocation
from calculations import (
    calculate_shift_stats,
    calculate_bill_allocation
)


def show_add_income_page():

    st.header("💵 Add Work Session")

    st.write(
        "Enter the details from your DoorDash or Uber Eats "
        "work session."
    )

    st.divider()

    with st.form("add_income_form"):

        st.subheader("Session Information")

        col1, col2 = st.columns(2)

        with col1:
            session_date = st.date_input(
                "Date",
                value=date.today()
            )

        with col2:
            app_name = st.selectbox(
                "Delivery App",
                [
                    "DoorDash",
                    "Uber Eats",
                    "Both",
                    "Other"
                ]
            )

        st.subheader("Earnings")

        earnings = st.number_input(
            "Total Earnings ($)",
            min_value=0.00,
            step=1.00,
            format="%.2f"
        )

        st.subheader("Work Information")

        col1, col2, col3 = st.columns(3)

        with col1:
            hours = st.number_input(
                "Hours Worked",
                min_value=0.0,
                step=0.25,
                format="%.2f"
            )

        with col2:
            trips = st.number_input(
                "Trips Completed",
                min_value=0,
                step=1
            )

        with col3:
            miles = st.number_input(
                "Miles Driven",
                min_value=0.0,
                step=1.0,
                format="%.1f"
            )

        notes = st.text_area(
            "Notes (Optional)",
            placeholder=(
                "Example: Worked dinner rush, weather was bad, "
                "downtown was busy..."
            )
        )

        st.divider()

        submitted = st.form_submit_button(
            "💾 Save Work Session",
            use_container_width=True
        )


    if submitted:

        if earnings <= 0:

            st.error(
                "Please enter earnings greater than $0."
            )

            return

        if hours <= 0:

            st.error(
                "Please enter the number of hours worked."
            )

            return

        if trips <= 0:

            st.error(
                "Please enter at least one completed trip."
            )

            return

        stats = calculate_shift_stats(
            earnings=earnings,
            hours=hours,
            trips=trips,
            miles=miles
        )

        session_id = add_work_session(
            date=session_date.isoformat(),
            app_name=app_name,
            earnings=earnings,
            hours=hours,
            trips=trips,
            miles=miles,
            notes=notes
        )

        bills = get_all_bills()

        allocations = []

        for bill in bills:

            allocation_amount = calculate_bill_allocation(
                earnings,
                bill["allocation_percentage"]
            )

            if allocation_amount > 0:

                add_bill_allocation(
                    bill_id=bill["id"],
                    session_id=session_id,
                    amount=allocation_amount,
                    allocation_date=session_date.isoformat()
                )

                allocations.append({
                    "name": bill["name"],
                    "percentage": bill["allocation_percentage"],
                    "amount": allocation_amount
                })

        st.success(
            "Work session saved successfully!"
        )


        st.subheader("📊 Shift Summary")

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
            st.metric(
                "Trips / Hour",
                f"{stats['trips_per_hour']:.2f}"
            )

        st.write("")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Hours",
                f"{stats['hours']:.2f}"
            )

        with col2:
            st.metric(
                "Trips",
                stats["trips"]
            )

        with col3:
            st.metric(
                "Miles",
                f"{stats['miles']:.1f}"
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

        st.write("")

        st.info(
            f"Average trip time: "
            f"{stats['average_trip_time']:.1f} minutes"
        )

        if allocations:

            st.divider()

            st.subheader("💰 Today's Bill Allocations")

            st.write(
                "Based on the percentages you've assigned "
                "to your bills, here's how today's income "
                "was divided:"
            )

            total_allocated = 0

            for allocation in allocations:

                col1, col2, col3 = st.columns(
                    [2, 1, 1]
                )

                with col1:
                    st.write(
                        f"**{allocation['name']}**"
                    )

                with col2:
                    st.write(
                        f"{allocation['percentage']:.1f}%"
                    )

                with col3:
                    st.write(
                        f"${allocation['amount']:.2f}"
                    )

                total_allocated += allocation["amount"]

            st.divider()

            remaining_money = earnings - total_allocated

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Total Allocated",
                    f"${total_allocated:.2f}"
                )

            with col2:
                st.metric(
                    "Money Remaining",
                    f"${remaining_money:.2f}"
                )

        else:

            st.info(
                "No bills have been created yet, so today's "
                "income was saved without any bill allocations."
            )