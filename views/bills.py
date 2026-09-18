import streamlit as st
from datetime import date

from database import (
    add_bill,
    get_all_bills,
    get_bill,
    update_bill,
    delete_bill,
    deactivate_bill,
    get_allocations_for_bill
)

from calculations import (
    calculate_bill_progress,
    calculate_bill_remaining,
    calculate_days_until_due,
    calculate_daily_amount_needed
)

def show_bills_page():

    st.header("💳 Bills & Goals")

    st.write(
        "Create bills, assign a percentage of your delivery "
        "income to each one, and track your progress."
    )

    st.divider()

    st.subheader("➕ Add New Bill")

    with st.form("add_bill_form"):

        col1, col2 = st.columns(2)

        with col1:

            bill_name = st.text_input(
                "Bill Name",
                placeholder="Example: Rent"
            )

            bill_amount = st.number_input(
                "Bill Amount ($)",
                min_value=0.00,
                step=10.00,
                format="%.2f"
            )

        with col2:

            due_date = st.date_input(
                "Due Date",
                value=date.today()
            )

            allocation_percentage = st.number_input(
                "Income Allocation (%)",
                min_value=0.0,
                max_value=100.0,
                step=1.0,
                format="%.1f"
            )

        st.caption(
            "The allocation percentage determines how much "
            "of every new work session will be set aside "
            "toward this bill."
        )

        create_bill = st.form_submit_button(
            "Create Bill",
            use_container_width=True
        )

    if create_bill:

        if not bill_name.strip():

            st.error(
                "Please enter a bill name."
            )

        elif bill_amount <= 0:

            st.error(
                "Bill amount must be greater than $0."
            )

        elif allocation_percentage <= 0:

            st.error(
                "Allocation percentage must be greater than 0%."
            )

        else:
            existing_bills = get_all_bills()

            existing_percentage = sum(
                bill["allocation_percentage"]
                for bill in existing_bills
            )

            new_total_percentage = (
                existing_percentage
                + allocation_percentage
            )

            if new_total_percentage > 100:

                st.error(
                    f"Your total allocation would become "
                    f"{new_total_percentage:.1f}%. "
                    f"Allocations cannot exceed 100%."
                )

            else:

                add_bill(
                    name=bill_name.strip(),
                    amount=bill_amount,
                    due_date=due_date.isoformat(),
                    allocation_percentage=allocation_percentage
                )

                st.success(
                    f"{bill_name} was created successfully!"
                )

                st.rerun()

    bills = get_all_bills()

    st.divider()

    st.subheader("📊 Income Allocation")

    if bills:

        total_percentage = sum(
            bill["allocation_percentage"]
            for bill in bills
        )

        unallocated_percentage = max(
            100 - total_percentage,
            0
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Income Allocated",
                f"{total_percentage:.1f}%"
            )

        with col2:

            st.metric(
                "Unallocated Income",
                f"{unallocated_percentage:.1f}%"
            )

        st.progress(
            min(total_percentage / 100, 1.0)
        )

        st.caption(
            f"For every $100 you earn, "
            f"${total_percentage:.2f} is assigned to bills "
            f"and ${unallocated_percentage:.2f} remains."
        )

    else:

        st.info(
            "You haven't created any bills yet."
        )

        return

    st.divider()

    st.subheader("🎯 Bill Progress")

    for bill in bills:

        bill_id = bill["id"]
        name = bill["name"]
        amount = bill["amount"]
        saved_amount = bill["saved_amount"]
        percentage = bill["allocation_percentage"]

        try:

            bill_due_date = date.fromisoformat(
                bill["due_date"]
            )

        except (ValueError, TypeError):

            bill_due_date = date.today()

        progress = calculate_bill_progress(
            saved_amount,
            amount
        )

        remaining = calculate_bill_remaining(
            saved_amount,
            amount
        )

        days_remaining = calculate_days_until_due(
            bill_due_date
        )

        daily_needed = calculate_daily_amount_needed(
            remaining,
            days_remaining
        )

        with st.container(border=True):

            col1, col2 = st.columns(
                [3, 1]
            )

            with col1:

                st.subheader(name)

                st.caption(
                    f"{percentage:.1f}% of new income"
                )

            with col2:

                st.metric(
                    "Remaining",
                    f"${remaining:.2f}"
                )

            st.progress(
                min(progress / 100, 1.0)
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Saved",
                    f"${saved_amount:.2f}"
                )

            with col2:

                st.metric(
                    "Goal",
                    f"${amount:.2f}"
                )

            with col3:

                st.metric(
                    "Progress",
                    f"{progress:.1f}%"
                )

            st.write(
                f"**Due:** "
                f"{bill_due_date.strftime('%B %d, %Y')}"
            )

            if remaining <= 0:

                st.success(
                    "✅ This bill is fully funded!"
                )

            elif days_remaining > 0:

                st.info(
                    f"{days_remaining} days remaining. "
                    f"You need an average of "
                    f"${daily_needed:.2f} per day "
                    f"to fully fund this bill."
                )

            else:

                st.warning(
                    f"This bill is due today or past due. "
                    f"${remaining:.2f} still needs to be funded."
                )

            with st.expander(
                "View Allocation History"
            ):

                allocations = get_allocations_for_bill(
                    bill_id
                )

                if allocations:

                    for allocation in allocations:

                        st.write(
                            f"**{allocation['allocation_date']}** "
                            f"— ${allocation['amount']:.2f}"
                        )

                else:

                    st.write(
                        "No income has been allocated "
                        "to this bill yet."
                    )

            with st.expander(
                "Manage Bill"
            ):

                st.write(
                    "Edit, deactivate, or permanently "
                    "delete this bill."
                )

                edit_name = st.text_input(
                    "Bill Name",
                    value=name,
                    key=f"name_{bill_id}"
                )

                edit_amount = st.number_input(
                    "Bill Amount",
                    min_value=0.01,
                    value=float(amount),
                    step=10.00,
                    key=f"amount_{bill_id}"
                )

                edit_due_date = st.date_input(
                    "Due Date",
                    value=bill_due_date,
                    key=f"due_{bill_id}"
                )

                edit_percentage = st.number_input(
                    "Allocation %",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(percentage),
                    step=1.0,
                    key=f"percentage_{bill_id}"
                )

                col1, col2, col3 = st.columns(3)


                with col1:

                    if st.button(
                        "Save Changes",
                        key=f"save_{bill_id}",
                        use_container_width=True
                    ):

                        other_percentage = sum(
                            other_bill["allocation_percentage"]
                            for other_bill in bills
                            if other_bill["id"] != bill_id
                        )

                        new_total = (
                            other_percentage
                            + edit_percentage
                        )

                        if new_total > 100:

                            st.error(
                                f"Total allocation would become "
                                f"{new_total:.1f}%. "
                                f"It cannot exceed 100%."
                            )

                        else:

                            update_bill(
                                bill_id=bill_id,
                                name=edit_name.strip(),
                                amount=edit_amount,
                                due_date=edit_due_date.isoformat(),
                                allocation_percentage=edit_percentage
                            )

                            st.success(
                                "Bill updated."
                            )

                            st.rerun()


                with col2:

                    if st.button(
                        "Deactivate",
                        key=f"deactivate_{bill_id}",
                        use_container_width=True
                    ):

                        deactivate_bill(
                            bill_id
                        )

                        st.rerun()


                with col3:

                    if st.button(
                        "Delete",
                        key=f"delete_{bill_id}",
                        use_container_width=True
                    ):

                        delete_bill(
                            bill_id
                        )

                        st.rerun()