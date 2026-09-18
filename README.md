# 💰 Delivery Finance

Delivery Finance is a local financial management and analytics application built with Python and Streamlit for gig delivery drivers.

The application is designed to help DoorDash and Uber Eats drivers track their earnings, analyze driving performance, manage bills, and automatically allocate portions of their income toward financial obligations and goals.

Rather than only tracking how much money was earned, Delivery Finance combines **income tracking, performance analytics, and budgeting** into one dashboard.

---

## 🚀 Features

### 💵 Work Session Tracking

Record individual delivery sessions including:

- Delivery platform
- Date
- Total earnings
- Hours worked
- Trips completed
- Miles driven
- Session notes

The application automatically calculates:

- Earnings per hour
- Earnings per trip
- Earnings per mile
- Trips per hour
- Average trip time

---

### 🏠 Financial Dashboard

The dashboard provides a quick overview of your delivery activity and financial progress.

It includes:

- Today's earnings
- Today's hours worked
- Today's trips
- Average earnings per hour
- Weekly earnings
- Weekly hours
- Weekly trips
- Weekly earnings chart
- Bill funding progress
- Upcoming bill information
- Income allocation overview
- Recent work sessions

---

### 💳 Bills & Goals

Create financial obligations or savings goals and automatically allocate delivery income toward them.

Each bill can include:

- Bill name
- Target amount
- Due date
- Income allocation percentage
- Amount currently funded

For example:

```text
Delivery Income: $200

Rent Allocation:       40% → $80
Car Insurance:         10% → $20
Savings:               10% → $20

Total Allocated:       $120
Remaining Income:       $80
```

The application also provides:

- Bill progress bars
- Remaining amount
- Funding percentage
- Days until the due date
- Required daily funding amount
- Allocation history
- Bill editing
- Bill deactivation
- Bill deletion

The system prevents active allocation percentages from exceeding 100%.

---

### 📊 Delivery Analytics

Analyze historical delivery performance using saved work sessions.

Analytics include:

- Total earnings
- Total hours worked
- Total trips
- Total miles
- Average earnings per hour
- Average earnings per trip
- Average earnings per mile
- Trips per hour
- Daily earnings trends
- Daily hours
- Daily trip volume
- Earnings-per-hour trends
- Delivery platform comparisons
- Highest earning day
- Highest hourly-rate day
- Most trips completed in a day
- Day-of-week performance

Analytics can also be filtered by delivery platform and date range.

---

### 📋 Income History

View and manage previously recorded delivery sessions.

Features include:

- Complete work-session history
- Date filtering
- Platform filtering
- Historical performance calculations
- Individual session details
- Session editing
- Safe deletion checks

---

### ⚙️ Settings

Configure personal tracking targets and application preferences.

Current settings include:

- Default delivery platform
- Mileage tracking preference
- Weekly income goal
- Monthly income goal
- Target hourly earnings
- Local database information

Settings are stored in the application's SQLite database and persist between sessions.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | User interface and local web application |
| SQLite | Local persistent database |
| Pandas | Data processing and analytics |

---

## 🗄️ Database

Delivery Finance uses SQLite for local data storage.

The database stores:

- Work sessions
- Bills
- Bill allocations
- Application settings

The database is automatically initialized when the application starts.

No external database server is required.

---

## 📁 Project Structure

```text
Budgeting Tracker App/
│
├── app.py
├── calculations.py
├── database.py
├── requirements.txt
│
└── views/
    ├── dashboard.py
    ├── add_income.py
    ├── income_history.py
    ├── bills.py
    ├── analytics.py
    └── settings.py
```

### File Responsibilities

**`app.py`**

Main Streamlit application and navigation system.

**`calculations.py`**

Contains financial and delivery-performance calculations.

**`database.py`**

Handles SQLite database creation, queries, inserts, updates, and persistent storage.

**`views/dashboard.py`**

Displays current income, weekly performance, bill progress, and recent activity.

**`views/add_income.py`**

Handles new delivery work-session entry and automatic bill allocations.

**`views/income_history.py`**

Displays and manages historical delivery sessions.

**`views/bills.py`**

Handles bills, financial goals, allocation percentages, and funding progress.

**`views/analytics.py`**

Provides historical delivery-performance analytics and charts.

**`views/settings.py`**

Manages application preferences and income targets.

---

## 💻 Running the Project Locally

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
```

Then enter the project directory:

```bash
cd YOUR_REPOSITORY_FOLDER
```

---

### 2. Create a virtual environment

Windows:

```bash
py -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

On Windows, you can also use:

```bash
py -m pip install -r requirements.txt
```

---

### 4. Run the application

Windows:

```bash
py -m streamlit run app.py
```

macOS/Linux:

```bash
python3 -m streamlit run app.py
```

Streamlit will provide a local address, typically:

```text
http://localhost:8501
```

Open that address in your browser to use the application.

---

## 🔒 Privacy

Delivery Finance is currently designed as a **local-first application**.

Financial and delivery information is stored locally using SQLite. The current version does not require:

- User accounts
- Cloud storage
- External financial APIs
- Banking credentials
- DoorDash credentials
- Uber Eats credentials

---

## 🧠 How It Works

```text
                    User
                      │
                      ▼
              Add Work Session
                      │
              ┌───────┴───────┐
              ▼               ▼
       calculations.py    database.py
                              │
                              ▼
                           SQLite
                              │
             ┌────────────────┼────────────────┐
             ▼                ▼                ▼
         Dashboard        Analytics       Bills & Goals
             │
             ▼
       Income History
```

When a delivery session is recorded, the application:

1. Stores the work session in SQLite.
2. Calculates delivery-performance statistics.
3. Finds active bills and financial goals.
4. Calculates each bill's income allocation.
5. Records those allocations.
6. Updates bill funding progress.
7. Makes the new information available to the dashboard and analytics system.

---

## 📈 Example

Suppose a driver records the following session:

```text
Platform:       DoorDash
Earnings:       $150
Hours:          5
Trips:          20
Miles:          75
```

Delivery Finance calculates:

```text
Earnings / Hour:    $30.00
Earnings / Trip:     $7.50
Earnings / Mile:     $2.00
Trips / Hour:         4.00
Avg. Trip Time:      15 min
```

If the driver has configured:

```text
Rent:             40%
Car Insurance:    10%
```

the same $150 session generates:

```text
Rent:             $60
Car Insurance:    $15
Unallocated:      $75
```

These allocations are then reflected in the driver's bill progress.

---

## 🗺️ Roadmap

Planned improvements include:

- Automatic allocation recalculation when work sessions are edited
- Safe allocation reversal when work sessions are deleted
- Automatic handling of fully funded bills
- Weekly and monthly goal tracking
- Recurring monthly bills
- Expense tracking
- Gas expense tracking
- Vehicle maintenance tracking
- Net profit calculations
- CSV/Excel exports
- Database backup and restore
- Improved dashboard visualizations
- Additional financial analytics

---

## ⚠️ Current Development Status

Delivery Finance is currently under active development.

The core application architecture and major pages have been implemented, but additional testing and improvements are still in progress. It should not currently be considered a replacement for professional accounting, tax, or financial software.

---

## 🎯 Project Goal

The goal of Delivery Finance is to create a financial tool specifically designed around the way gig delivery workers earn money.

Instead of treating income, driving performance, and budgeting as separate problems, the application connects them so drivers can better understand:

- How much they are earning
- How efficiently they are earning it
- Where their income is being allocated
- How close they are to covering upcoming obligations
- How their delivery performance changes over time

---

## 📄 License

This project is currently intended for educational and personal use.
