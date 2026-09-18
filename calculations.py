from datetime import date

def calculate_hourly_rate(earnings, hours):
    """
    Calculate how much money was earned per hour.
    """
    if hours <= 0:
        return 0.0

    return round(earnings / hours, 2)


def calculate_per_trip(earnings, trips):
    """
    Calculate average earnings per delivery/trip.
    """
    if trips <= 0:
        return 0.0

    return round(earnings / trips, 2)


def calculate_per_mile(earnings, miles):
    """
    Calculate earnings per mile driven.
    """
    if miles <= 0:
        return 0.0

    return round(earnings / miles, 2)


def calculate_trips_per_hour(trips, hours):
    """
    Calculate average number of trips completed per hour.
    """
    if hours <= 0:
        return 0.0

    return round(trips / hours, 2)


def calculate_average_trip_time(hours, trips):
    """
    Calculate average minutes spent per trip.
    """
    if trips <= 0:
        return 0.0

    total_minutes = hours * 60

    return round(total_minutes / trips, 1)


def calculate_shift_stats(earnings, hours, trips, miles):
    return {
        "earnings": round(earnings, 2),
        "hours": round(hours, 2),
        "trips": trips,
        "miles": round(miles, 2),

        "hourly_rate": calculate_hourly_rate(
            earnings,
            hours
        ),

        "per_trip": calculate_per_trip(
            earnings,
            trips
        ),

        "per_mile": calculate_per_mile(
            earnings,
            miles
        ),

        "trips_per_hour": calculate_trips_per_hour(
            trips,
            hours
        ),

        "average_trip_time": calculate_average_trip_time(
            hours,
            trips
        )
    }


def calculate_bill_allocation(earnings, percentage):
    if earnings <= 0 or percentage <= 0:
        return 0.0

    allocation = earnings * (percentage / 100)

    return round(allocation, 2)


def calculate_all_allocations(earnings, bills):

    allocations = []

    for bill in bills:

        amount = calculate_bill_allocation(
            earnings,
            bill["percentage"]
        )

        allocations.append({
            "name": bill["name"],
            "percentage": bill["percentage"],
            "amount": amount
        })

    return allocations


def calculate_bill_progress(saved_amount, bill_amount):
    if bill_amount <= 0:
        return 0.0

    progress = (saved_amount / bill_amount) * 100

    return round(min(progress, 100), 1)


def calculate_bill_remaining(saved_amount, bill_amount):

    remaining = bill_amount - saved_amount

    return round(max(remaining, 0), 2)


def calculate_total_earnings(sessions):

    return round(
        sum(session["earnings"] for session in sessions),
        2
    )


def calculate_total_hours(sessions):

    return round(
        sum(session["hours"] for session in sessions),
        2
    )


def calculate_total_trips(sessions):

    return sum(
        session["trips"] for session in sessions
    )


def calculate_total_miles(sessions):

    return round(
        sum(session["miles"] for session in sessions),
        2
    )


def calculate_period_stats(sessions):

    if not sessions:
        return {
            "earnings": 0.0,
            "hours": 0.0,
            "trips": 0,
            "miles": 0.0,
            "hourly_rate": 0.0,
            "per_trip": 0.0,
            "per_mile": 0.0,
            "trips_per_hour": 0.0
        }

    earnings = calculate_total_earnings(sessions)
    hours = calculate_total_hours(sessions)
    trips = calculate_total_trips(sessions)
    miles = calculate_total_miles(sessions)

    return {
        "earnings": earnings,
        "hours": hours,
        "trips": trips,
        "miles": miles,

        "hourly_rate": calculate_hourly_rate(
            earnings,
            hours
        ),

        "per_trip": calculate_per_trip(
            earnings,
            trips
        ),

        "per_mile": calculate_per_mile(
            earnings,
            miles
        ),

        "trips_per_hour": calculate_trips_per_hour(
            trips,
            hours
        )
    }


def calculate_goal_progress(current_amount, goal_amount):

    if goal_amount <= 0:
        return 0.0

    progress = (current_amount / goal_amount) * 100

    return round(min(progress, 100), 1)


def calculate_amount_needed(current_amount, goal_amount):

    remaining = goal_amount - current_amount

    return round(max(remaining, 0), 2)


def calculate_hours_needed(amount_needed, average_hourly_rate):

    if average_hourly_rate <= 0:
        return 0.0

    return round(
        amount_needed / average_hourly_rate,
        2
    )


def calculate_trips_needed(amount_needed, average_per_trip):

    if average_per_trip <= 0:
        return 0

    trips = amount_needed / average_per_trip

    return int(-(-trips // 1))


def calculate_days_until_due(due_date):

    today = date.today()

    days = (due_date - today).days

    return max(days, 0)


def calculate_daily_amount_needed(
    amount_remaining,
    days_remaining
):

    if days_remaining <= 0:
        return round(amount_remaining, 2)

    return round(
        amount_remaining / days_remaining,
        2
    )