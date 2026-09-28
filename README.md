# 🏃 Strava Fitness Analytics

An end-to-end fitness data analytics project that transforms Fitbit activity data into actionable insights using **Python, Pandas, SQLite, SQL, Plotly, and Streamlit**.

The project covers the complete analytics workflow:

**Raw Data → Data Cleaning → SQLite Database → SQL Analysis → Exploratory Data Analysis → Interactive Streamlit Dashboard**

---

## 📌 Project Overview

Strava Fitness Analytics analyzes fitness-tracking data to understand:

* Daily physical activity
* Steps and calories
* Activity intensity
* Sedentary behavior
* Sleep patterns
* Hourly activity
* Weight and BMI
* Differences in activity levels between users
* Relationships between sleep, steps, and calories

The final output is an interactive **Streamlit dashboard** that allows users to explore the analyzed fitness data through multiple analytical sections.

---

## 🎯 Business Problem

Fitness-tracking devices generate large amounts of data related to physical activity, sleep, calories, intensity, and weight.

The objective of this project is to transform this raw fitness data into meaningful analytical insights that can help identify:

* Activity patterns
* High and low activity periods
* Sedentary behavior
* Sleep patterns
* User activity levels
* Relationships between physical activity and calorie expenditure
* Weight and BMI patterns
* Potential areas for improving fitness engagement

---

## 📊 Dataset

The project uses the **Fitabase Fitbit Fitness Tracker dataset** containing anonymized fitness-tracking data.

The original dataset contains multiple daily, hourly, and minute-level files.

For this project, the following **8 core datasets** were selected:

| Dataset            | Records |
| ------------------ | ------: |
| Daily Activity     |     940 |
| Daily Calories     |     940 |
| Daily Intensities  |     940 |
| Daily Steps        |     940 |
| Sleep              |     410 |
| Weight             |      67 |
| Hourly Steps       |  22,099 |
| Hourly Intensities |  22,099 |

The daily activity datasets contain data from **33 users** across **31 dates**.

> Raw source files are intentionally not included in this GitHub repository to keep the repository lightweight and maintain a clean project structure.

---

# 🔄 Project Workflow

```text
Raw Fitbit Data
       ↓
Python + Pandas
       ↓
Data Cleaning
       ↓
Cleaned CSV Files
       ↓
SQLite Database
       ↓
SQL Analysis
       ↓
Python EDA
       ↓
Plotly Visualizations
       ↓
Streamlit Dashboard
```

---

# 🧹 1. Data Cleaning

Data cleaning was performed using **Python and Pandas** before loading the data into SQLite.

### Cleaning operations included

* Standardizing column names
* Removing duplicate records
* Removing leading/trailing whitespace
* Converting date/time columns
* Converting numerical columns to numeric data types
* Handling invalid numeric values
* Handling non-positive weight/BMI values
* Generating a data-quality summary
* Preserving the original raw dataset without modification

### Cleaning results

| Dataset            | Original Rows | Cleaned Rows |
| ------------------ | ------------: | -----------: |
| Daily Activity     |           940 |          940 |
| Daily Calories     |           940 |          940 |
| Daily Steps        |           940 |          940 |
| Daily Intensities  |           940 |          940 |
| Sleep              |           413 |          410 |
| Weight             |            67 |           67 |
| Hourly Steps       |        22,099 |       22,099 |
| Hourly Intensities |        22,099 |       22,099 |

Three duplicate records were removed from the sleep dataset.

---

# 🗄️ 2. SQLite Database

The cleaned datasets were loaded into a SQLite database:

```text
database/fitness.db
```

The database contains 8 analytical tables:

```text
daily_activity
daily_calories
daily_steps
daily_intensities
sleep
weight
hourly_steps
hourly_intensities
```

SQLite was selected to create a lightweight analytical database that can be queried directly from Python and Streamlit.

---

# 🔎 3. SQL Analysis

SQL was used to answer analytical questions and generate structured insights from the database.

The project includes **18 SQL analyses** covering:

* User and record counts
* Average steps
* Average calories
* Distance
* Activity levels
* Daily activity trends
* Active and inactive dates
* Activity intensity
* Sleep duration
* Sleep versus activity
* Hourly steps
* Hourly intensity
* Weight
* BMI
* Sedentary behavior
* Highly active users

The SQL queries are available in:

```text
sql/analysis.sql
```

---

# 📈 4. Exploratory Data Analysis

EDA was performed using **Python, Pandas, Matplotlib, and Seaborn**.

The analysis includes:

* Descriptive statistics
* Missing-value analysis
* Activity-level distribution
* Steps distribution
* Calories distribution
* Steps versus calories
* Daily activity trends
* Activity intensity
* Sleep distribution
* Sleep versus steps
* Hourly steps
* Hourly intensity
* Weight and BMI
* Sedentary behavior
* Top active users

EDA outputs are stored in:

```text
data/eda/
```

---

# 📊 Key Findings

## 🚶 Overall Activity

Across the daily activity dataset:

* **33 users** were analyzed.
* **940 daily activity records** were available.
* Average daily steps: **7,638**
* Average daily calories: **2,304**
* Average daily distance: **5.49**
* Average sedentary time: **991 minutes**
* Maximum recorded daily steps: **36,019**
* Maximum recorded daily calories: **4,900**

---

## 🏃 Activity Levels

Users were grouped based on average daily steps.

| Activity Level    | Users |
| ----------------- | ----: |
| Highly Active     |     7 |
| Active            |     9 |
| Moderately Active |     9 |
| Less Active       |     8 |

This shows a relatively distributed user base across the four activity categories.

---

## 🔥 Activity Intensity

Average daily activity minutes were:

| Intensity      | Average Minutes |
| -------------- | --------------: |
| Very Active    |           21.16 |
| Fairly Active  |           13.56 |
| Lightly Active |          192.81 |
| Sedentary      |          991.21 |

The data shows substantially more recorded time in light activity and sedentary categories than in higher-intensity activity.

---

## 👣 Steps and Calories

The Pearson correlation between daily steps and calories was approximately:

```text
0.592
```

This indicates a **moderate positive linear association** in this dataset: days with more recorded steps tended to also have higher recorded calorie expenditure.

Correlation should not be interpreted as proof of causation.

---

## 😴 Sleep

Sleep data was available for **24 users**.

Key results:

* Average sleep: **6.99 hours**
* Average time in bed: **7.64 hours**
* Highest average recorded sleep: **10.87 hours**

The date-aligned sleep/activity analysis was performed by matching users and dates between the sleep and daily activity datasets.

The correlation between sleep duration and daily steps was approximately:

```text
-0.066
```

This represents very little linear association within the available data.

---

## 🕐 Hourly Activity

Hourly analysis identified the most active period of the day.

The highest average hourly step activity occurred around:

```text
18:00
```

The highest hourly intensity was also observed around:

```text
18:00
```

Other relatively active periods included the afternoon and evening hours.

---

## ⚖️ Weight and BMI

Weight information was available for only **8 users**.

Key results:

* Average weight: **72.04 kg**
* Average BMI: **25.19**
* Weight records: **67**

Because weight data was available for only 8 of the 33 users, weight and BMI findings should be interpreted with caution and should not be generalized to the entire dataset.

---

## 🪑 Sedentary Behavior

The average recorded sedentary time was approximately:

```text
991 minutes per day
```

The highest recorded sedentary users included users with more than 1,250 recorded sedentary minutes.

Sedentary time represents tracker-recorded data and may not necessarily correspond exactly to actual waking inactivity.

---

# 👤 Top Activity Example

The SQL analysis identified users with the highest average daily step counts.

The highest recorded average was:

| User       | Avg. Steps |
| ---------- | ---------: |
| 8877689391 |     16,040 |
| 8053475328 |     14,763 |
| 1503960366 |     12,117 |
| 2022484408 |     11,371 |
| 7007744171 |     11,323 |

The user IDs are anonymized identifiers from the source dataset.

---

# 📱 Streamlit Dashboard

The final application is built entirely with **Streamlit**.

No Power BI or Tableau is required.

The dashboard contains the following sections:

### 🏠 Overview

Provides a high-level summary of:

* Users
* Activity records
* Average steps
* Average calories
* Activity distribution
* Key activity metrics

### 🚶 Activity

Explores:

* Daily steps
* Calories
* Activity levels
* Activity intensity
* Daily trends
* User-level activity

### 😴 Sleep

Explores:

* Average sleep
* Sleep duration
* Time in bed
* Sleep versus activity
* Sleep distribution

### 🕐 Hourly Analysis

Explores:

* Hourly steps
* Hourly intensity
* Peak activity hours

### ⚖️ Weight & BMI

Explores:

* Weight distribution
* BMI
* User-level weight metrics

### 💡 Insights

Summarizes the major findings generated from the SQL and EDA analysis.

---

# 🛠️ Technology Stack

| Technology | Purpose                          |
| ---------- | -------------------------------- |
| Python     | Data processing and analysis     |
| Pandas     | Data cleaning and transformation |
| NumPy      | Numerical operations             |
| SQLite     | Analytical database              |
| SQL        | Data analysis                    |
| Matplotlib | EDA visualization                |
| Seaborn    | Statistical visualization        |
| Plotly     | Interactive dashboard charts     |
| Streamlit  | Interactive web application      |
| Git        | Version control                  |
| GitHub     | Project repository               |

---

# 📁 Project Structure

```text
Strava_fitness_analysis/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── cleaned/
│   │   ├── daily_activity_clean.csv
│   │   ├── daily_calories_clean.csv
│   │   ├── daily_intensities_clean.csv
│   │   ├── daily_steps_clean.csv
│   │   ├── hourly_intensities_clean.csv
│   │   ├── hourly_steps_clean.csv
│   │   ├── sleep_clean.csv
│   │   ├── weight_clean.csv
│   │   └── data_quality_summary.csv
│   │
│   └── eda/
│       ├── charts
│       ├── summary CSV files
│       └── EDA outputs
│
├── database/
│   └── fitness.db
│
├── sql/
│   └── analysis.sql
│
└── src/
    ├── data_cleaning.py
    ├── create_database.py
    ├── test_database.py
    ├── run_sql_analysis.py
    └── eda_analysis.py
```

---

# ▶️ How to Run Locally

## 1. Clone the repository

```bash
git clone https://github.com/Ajay2003-prog/Strava_fitness_analysis.git
cd Strava_fitness_analysis
```

## 2. Create a virtual environment

```bash
python -m venv venv
```

## 3. Activate the environment

### Windows

```powershell
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

## 5. Run the Streamlit application

```bash
streamlit run app.py
```

The application will open in your browser.

---

# 🔄 Rebuilding the Data Pipeline

The repository contains the scripts used to reproduce the analytical workflow.

### Clean the raw data

```bash
python src/data_cleaning.py
```

### Create the SQLite database

```bash
python src/create_database.py
```

### Validate the database

```bash
python src/test_database.py
```

### Run SQL analysis

```bash
python src/run_sql_analysis.py
```

### Run Python EDA

```bash
python src/eda_analysis.py
```

### Launch the dashboard

```bash
streamlit run app.py
```

> The original raw Fitbit dataset is intentionally excluded from the repository. If reproducing the pipeline from scratch, place the source data in the expected local `Data Files/` directory before running the cleaning script.

---

# ⚠️ Limitations

Several limitations should be considered when interpreting the results.

### Limited user coverage

The dataset contains 33 users, while weight data is available for only 8 users and sleep data for 24 users.

### Limited observation period

The daily activity data covers a relatively short period, so the results may not represent long-term behavior.

### Missing or zero activity

Some records contain zero steps or calories. These may represent days with limited tracker activity or incomplete recording rather than actual zero physical activity.

### Weight data limitations

BMI and weight analysis is based on a small subset of users and should not be generalized to the entire dataset.

### Correlation versus causation

Relationships such as steps versus calories and sleep versus steps represent statistical associations and do not establish causal relationships.

### Tracker-recorded sedentary time

Sedentary minutes are based on device-recorded activity and may not perfectly represent actual waking sedentary behavior.

---

# 🚀 Future Improvements

Potential future enhancements include:

* Add additional Fitbit datasets such as minute-level activity and heart rate
* Add interactive date filters
* Add user-level filtering
* Add downloadable analytical reports
* Add more advanced statistical analysis
* Add predictive modeling
* Add user segmentation
* Add recommendation features
* Deploy the Streamlit application online
* Add automated data-refresh workflows

---

# 📌 Portfolio Highlights

This project demonstrates practical experience with:

* End-to-end data analytics
* Data cleaning
* Exploratory data analysis
* SQL querying
* SQLite database design
* Data validation
* Statistical analysis
* Interactive visualization
* Dashboard development
* Python-based analytics workflows
* Git and GitHub project management

---

## 👨‍💻 Author

**Chinnam Ajay Sai Phaneendra Reddy**

Data Analyst | Business Analytics

GitHub:
https://github.com/Ajay2003-prog

LinkedIn:
https://linkedin.com/in/asp-reddy-245asp

---

## ⭐ Project Summary

**Strava Fitness Analytics** demonstrates an end-to-end analytics workflow using real-world fitness-tracking data.

The project combines:

```text
Python
+
Pandas
+
SQLite
+
SQL
+
EDA
+
Plotly
+
Streamlit
```

to transform raw fitness data into an interactive analytical dashboard and a structured set of data-driven insights.
