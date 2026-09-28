from pathlib import Path
import matplotlib
matplotlib.use("Agg")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parent.parent
CLEANED_DIR = BASE_DIR / "data" / "cleaned"
EDA_DIR = BASE_DIR / "data" / "eda"
EDA_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid")


def load_data():
    files = {
        "activity": "daily_activity_clean.csv",
        "calories": "daily_calories_clean.csv",
        "steps": "daily_steps_clean.csv",
        "intensities": "daily_intensities_clean.csv",
        "sleep": "sleep_clean.csv",
        "weight": "weight_clean.csv",
        "hourly_steps": "hourly_steps_clean.csv",
        "hourly_intensities": "hourly_intensities_clean.csv"
    }

    data = {}

    for name, filename in files.items():
        path = CLEANED_DIR / filename

        if not path.exists():
            raise FileNotFoundError(
                f"Missing cleaned file: {path}"
            )

        data[name] = pd.read_csv(path)

    return data


def save_plot(filename):
    plt.tight_layout()
    plt.savefig(
        EDA_DIR / filename,
        dpi=150,
        bbox_inches="tight"
    )
    plt.close("all")


def main():
    print("=" * 60)
    print("FITNESS ANALYTICS - EXPLORATORY DATA ANALYSIS")
    print("=" * 60)

    data = load_data()

    activity = data["activity"]
    calories = data["calories"]
    steps = data["steps"]
    intensities = data["intensities"]
    sleep = data["sleep"]
    weight = data["weight"]
    hourly_steps = data["hourly_steps"]
    hourly_intensities = data["hourly_intensities"]

    # ========================================================
    # 1. DATASET OVERVIEW
    # ========================================================

    print("\n1. DATASET OVERVIEW")
    print("-" * 60)

    for name, df in data.items():
        print(
            f"{name:20} "
            f"{len(df):,} rows x {len(df.columns)} columns"
        )

    # ========================================================
    # 2. MISSING VALUES
    # ========================================================

    print("\n2. MISSING VALUES")
    print("-" * 60)

    missing_summary = []

    for name, df in data.items():
        missing_count = int(df.isna().sum().sum())

        missing_summary.append({
            "dataset": name,
            "missing_values": missing_count
        })

        print(f"{name:20} {missing_count:,}")

    pd.DataFrame(missing_summary).to_csv(
        EDA_DIR / "missing_values_summary.csv",
        index=False
    )

    # ========================================================
    # 3. DESCRIPTIVE STATISTICS
    # ========================================================

    print("\n3. DESCRIPTIVE STATISTICS")
    print("-" * 60)

    numeric_columns = [
        "totalsteps",
        "totaldistance",
        "calories",
        "veryactiveminutes",
        "fairlyactiveminutes",
        "lightlyactiveminutes",
        "sedentaryminutes"
    ]

    activity_stats = (
        activity[numeric_columns]
        .describe()
        .round(2)
    )

    print(activity_stats.to_string())

    activity_stats.to_csv(
        EDA_DIR / "activity_descriptive_statistics.csv"
    )

    # ========================================================
    # 4. ACTIVITY LEVEL DISTRIBUTION
    # ========================================================

    print("\n4. ACTIVITY LEVEL DISTRIBUTION")
    print("-" * 60)

    user_activity = (
        activity
        .groupby("id")
        .agg(
            avg_steps=("totalsteps", "mean"),
            avg_calories=("calories", "mean")
        )
        .reset_index()
    )

    def classify_activity(value):
        if value >= 10000:
            return "Highly Active"
        elif value >= 7500:
            return "Active"
        elif value >= 5000:
            return "Moderately Active"
        else:
            return "Less Active"

    user_activity["activity_level"] = (
        user_activity["avg_steps"]
        .apply(classify_activity)
    )

    activity_distribution = (
        user_activity["activity_level"]
        .value_counts()
        .rename_axis("activity_level")
        .reset_index(name="user_count")
    )

    print(
        activity_distribution.to_string(index=False)
    )

    activity_distribution.to_csv(
        EDA_DIR / "activity_level_distribution.csv",
        index=False
    )

    plt.figure(figsize=(9, 5))

    sns.barplot(
        data=activity_distribution,
        x="activity_level",
        y="user_count"
    )

    plt.title("User Activity Level Distribution")
    plt.xlabel("Activity Level")
    plt.ylabel("Number of Users")

    save_plot("activity_levels.png")

    # ========================================================
    # 5. DAILY STEPS DISTRIBUTION
    # ========================================================

    print("\n5. DAILY STEPS")
    print("-" * 60)

    print(
        f"Average steps: "
        f"{activity['totalsteps'].mean():,.0f}"
    )

    print(
        f"Minimum steps: "
        f"{activity['totalsteps'].min():,.0f}"
    )

    print(
        f"Maximum steps: "
        f"{activity['totalsteps'].max():,.0f}"
    )

    plt.figure(figsize=(9, 5))

    sns.histplot(
        activity["totalsteps"],
        bins=30,
        kde=True
    )

    plt.title("Distribution of Daily Steps")
    plt.xlabel("Daily Steps")
    plt.ylabel("Frequency")

    save_plot("daily_steps_distribution.png")

    # ========================================================
    # 6. CALORIES DISTRIBUTION
    # ========================================================

    print("\n6. CALORIES")
    print("-" * 60)

    print(
        f"Average calories: "
        f"{activity['calories'].mean():,.0f}"
    )

    print(
        f"Minimum calories: "
        f"{activity['calories'].min():,.0f}"
    )

    print(
        f"Maximum calories: "
        f"{activity['calories'].max():,.0f}"
    )

    plt.figure(figsize=(9, 5))

    sns.histplot(
        activity["calories"],
        bins=30,
        kde=True
    )

    plt.title("Distribution of Daily Calories")
    plt.xlabel("Calories")
    plt.ylabel("Frequency")

    save_plot("calories_distribution.png")

    # ========================================================
    # 7. STEPS VS CALORIES
    # ========================================================

    print("\n7. STEPS VS CALORIES")
    print("-" * 60)

    correlation = (
        activity[["totalsteps", "calories"]]
        .corr()
        .iloc[0, 1]
    )

    print(
        f"Steps vs Calories correlation: "
        f"{correlation:.3f}"
    )

    plt.figure(figsize=(9, 5))

    sns.scatterplot(
        data=activity,
        x="totalsteps",
        y="calories",
        alpha=0.6
    )

    sns.regplot(
        data=activity,
        x="totalsteps",
        y="calories",
        scatter=False
    )

    plt.title("Daily Steps vs Calories")
    plt.xlabel("Daily Steps")
    plt.ylabel("Calories")

    save_plot("steps_vs_calories.png")

    # ========================================================
    # 8. ACTIVITY INTENSITY
    # ========================================================

    print("\n8. ACTIVITY INTENSITY")
    print("-" * 60)

    intensity_summary = pd.DataFrame({
        "activity_type": [
            "Very Active",
            "Fairly Active",
            "Lightly Active",
            "Sedentary"
        ],
        "average_minutes": [
            activity["veryactiveminutes"].mean(),
            activity["fairlyactiveminutes"].mean(),
            activity["lightlyactiveminutes"].mean(),
            activity["sedentaryminutes"].mean()
        ]
    })

    intensity_summary["average_minutes"] = (
        intensity_summary["average_minutes"]
        .round(1)
    )

    print(
        intensity_summary.to_string(index=False)
    )

    intensity_summary.to_csv(
        EDA_DIR / "activity_intensity_summary.csv",
        index=False
    )

    plt.figure(figsize=(9, 5))

    sns.barplot(
        data=intensity_summary,
        x="activity_type",
        y="average_minutes"
    )

    plt.title("Average Daily Activity Intensity")
    plt.xlabel("Activity Type")
    plt.ylabel("Average Minutes")

    save_plot("activity_intensity.png")

    # ========================================================
    # 9. DAILY ACTIVITY TREND
    # ========================================================

    print("\n9. DAILY ACTIVITY TREND")
    print("-" * 60)

    activity["activitydate"] = pd.to_datetime(
        activity["activitydate"],
        errors="coerce"
    )

    daily_trend = (
        activity
        .groupby("activitydate")
        .agg(
            avg_steps=("totalsteps", "mean"),
            avg_calories=("calories", "mean")
        )
        .reset_index()
    )

    daily_trend.to_csv(
        EDA_DIR / "daily_activity_trend.csv",
        index=False
    )

    plt.figure(figsize=(11, 5))

    sns.lineplot(
        data=daily_trend,
        x="activitydate",
        y="avg_steps",
        marker="o"
    )

    plt.title("Average Daily Steps Trend")
    plt.xlabel("Date")
    plt.ylabel("Average Steps")
    plt.xticks(rotation=45)

    save_plot("daily_steps_trend.png")

    # ========================================================
    # 10. SLEEP ANALYSIS
    # ========================================================

    print("\n10. SLEEP ANALYSIS")
    print("-" * 60)

    sleep["sleep_hours"] = (
        sleep["totalminutesasleep"] / 60
    )

    sleep["bed_hours"] = (
        sleep["totaltimeinbed"] / 60
    )

    print(
        f"Average sleep: "
        f"{sleep['sleep_hours'].mean():.2f} hours"
    )

    print(
        f"Average time in bed: "
        f"{sleep['bed_hours'].mean():.2f} hours"
    )

    sleep_summary = (
        sleep
        .groupby("id")
        .agg(
            avg_sleep_hours=("sleep_hours", "mean"),
            avg_bed_hours=("bed_hours", "mean")
        )
        .reset_index()
    )

    sleep_summary.to_csv(
        EDA_DIR / "sleep_summary.csv",
        index=False
    )

    plt.figure(figsize=(9, 5))

    sns.histplot(
        sleep["sleep_hours"],
        bins=20,
        kde=True
    )

    plt.title("Distribution of Sleep Duration")
    plt.xlabel("Sleep Hours")
    plt.ylabel("Frequency")

    save_plot("sleep_distribution.png")

    # ========================================================
    # 11. SLEEP VS STEPS
    # ========================================================

    print("\n11. SLEEP VS STEPS")
    print("-" * 60)

    sleep["sleepday"] = pd.to_datetime(
        sleep["sleepday"],
        errors="coerce"
    ).dt.date

    activity["activitydate"] = pd.to_datetime(
        activity["activitydate"],
        errors="coerce"
    ).dt.date

    sleep_activity = pd.merge(
        sleep[
            ["id", "sleepday", "sleep_hours"]
        ],
        activity[
            ["id", "activitydate", "totalsteps"]
        ],
        left_on=["id", "sleepday"],
        right_on=["id", "activitydate"],
        how="inner"
    )

    sleep_activity_summary = (
        sleep_activity
        .groupby("id")
        .agg(
            avg_sleep_hours=("sleep_hours", "mean"),
            avg_steps=("totalsteps", "mean")
        )
        .reset_index()
    )

    sleep_activity_summary.to_csv(
        EDA_DIR / "sleep_vs_activity.csv",
        index=False
    )

    if len(sleep_activity_summary) > 1:
        sleep_correlation = (
            sleep_activity_summary[
                ["avg_sleep_hours", "avg_steps"]
            ]
            .corr()
            .iloc[0, 1]
        )

        print(
            f"Sleep vs Steps correlation: "
            f"{sleep_correlation:.3f}"
        )

    plt.figure(figsize=(9, 5))

    sns.scatterplot(
        data=sleep_activity_summary,
        x="avg_sleep_hours",
        y="avg_steps",
        alpha=0.7
    )

    plt.title("Average Sleep vs Average Steps")
    plt.xlabel("Average Sleep Hours")
    plt.ylabel("Average Steps")

    save_plot("sleep_vs_steps.png")

    # ========================================================
    # 12. HOURLY STEPS
    # ========================================================

    print("\n12. HOURLY STEPS")
    print("-" * 60)

    hourly_steps["activityhour"] = pd.to_datetime(
        hourly_steps["activityhour"],
        errors="coerce"
    )

    hourly_steps["hour"] = (
        hourly_steps["activityhour"]
        .dt.hour
    )

    hourly_summary = (
        hourly_steps
        .groupby("hour")
        .agg(
            avg_steps=("steptotal", "mean")
        )
        .reset_index()
    )

    peak_hour = hourly_summary.loc[
        hourly_summary["avg_steps"].idxmax()
    ]

    print(
        f"Peak activity hour: "
        f"{int(peak_hour['hour']):02d}:00"
    )

    hourly_summary.to_csv(
        EDA_DIR / "hourly_steps_summary.csv",
        index=False
    )

    plt.figure(figsize=(11, 5))

    sns.lineplot(
        data=hourly_summary,
        x="hour",
        y="avg_steps",
        marker="o"
    )

    plt.title("Average Steps by Hour")
    plt.xlabel("Hour of Day")
    plt.ylabel("Average Steps")

    save_plot("hourly_steps.png")

    # ========================================================
    # 13. HOURLY INTENSITY
    # ========================================================

    print("\n13. HOURLY INTENSITY")
    print("-" * 60)

    hourly_intensities["activityhour"] = pd.to_datetime(
        hourly_intensities["activityhour"],
        errors="coerce"
    )

    hourly_intensities["hour"] = (
        hourly_intensities["activityhour"]
        .dt.hour
    )

    intensity_hourly = (
        hourly_intensities
        .groupby("hour")
        .agg(
            avg_intensity=("totalintensity", "mean"),
            avg_average_intensity=("averageintensity", "mean")
        )
        .reset_index()
    )

    peak_intensity = intensity_hourly.loc[
        intensity_hourly["avg_intensity"].idxmax()
    ]

    print(
        f"Peak intensity hour: "
        f"{int(peak_intensity['hour']):02d}:00"
    )

    intensity_hourly.to_csv(
        EDA_DIR / "hourly_intensity_summary.csv",
        index=False
    )

    plt.figure(figsize=(11, 5))

    sns.lineplot(
        data=intensity_hourly,
        x="hour",
        y="avg_intensity",
        marker="o"
    )

    plt.title("Average Activity Intensity by Hour")
    plt.xlabel("Hour of Day")
    plt.ylabel("Average Intensity")

    save_plot("hourly_intensity.png")

    # ========================================================
    # 14. WEIGHT AND BMI
    # ========================================================

    print("\n14. WEIGHT AND BMI")
    print("-" * 60)

    print(
        f"Users with weight data: "
        f"{weight['id'].nunique()}"
    )

    print(
        f"Average weight: "
        f"{weight['weightkg'].mean():.2f} kg"
    )

    print(
        f"Average BMI: "
        f"{weight['bmi'].mean():.2f}"
    )

    weight_summary = (
        weight
        .groupby("id")
        .agg(
            avg_weight_kg=("weightkg", "mean"),
            avg_bmi=("bmi", "mean")
        )
        .reset_index()
    )

    weight_summary.to_csv(
        EDA_DIR / "weight_bmi_summary.csv",
        index=False
    )

    plt.figure(figsize=(9, 5))

    sns.histplot(
        weight["bmi"].dropna(),
        bins=15,
        kde=True
    )

    plt.title("BMI Distribution")
    plt.xlabel("BMI")
    plt.ylabel("Frequency")

    save_plot("bmi_distribution.png")

    # ========================================================
    # 15. SEDENTARY BEHAVIOR
    # ========================================================

    print("\n15. SEDENTARY BEHAVIOR")
    print("-" * 60)

    sedentary = (
        activity
        .groupby("id")
        .agg(
            avg_sedentary_minutes=("sedentaryminutes", "mean"),
            avg_steps=("totalsteps", "mean")
        )
        .reset_index()
        .sort_values(
            "avg_sedentary_minutes",
            ascending=False
        )
    )

    print(
        sedentary.head(10).to_string(index=False)
    )

    sedentary.to_csv(
        EDA_DIR / "sedentary_behavior.csv",
        index=False
    )

    # ========================================================
    # 16. TOP ACTIVE USERS
    # ========================================================

    print("\n16. TOP ACTIVE USERS")
    print("-" * 60)

    top_users = (
        user_activity
        .sort_values(
            "avg_steps",
            ascending=False
        )
        .head(10)
    )

    print(
        top_users.to_string(index=False)
    )

    top_users.to_csv(
        EDA_DIR / "top_active_users.csv",
        index=False
    )

    plt.figure(figsize=(10, 5))

    sns.barplot(
        data=top_users,
        x="avg_steps",
        y="id"
    )

    plt.title("Top 10 Users by Average Daily Steps")
    plt.xlabel("Average Steps")
    plt.ylabel("User ID")

    save_plot("top_active_users.png")

    # ========================================================
    # 17. EDA SUMMARY
    # ========================================================

    print("\n17. EDA SUMMARY")
    print("-" * 60)

    summary = pd.DataFrame({
        "metric": [
            "Total Users",
            "Total Activity Records",
            "Average Daily Steps",
            "Average Daily Calories",
            "Average Daily Distance",
            "Average Sleep Hours",
            "Users With Sleep Data",
            "Users With Weight Data",
            "Average Weight Kg",
            "Average BMI",
            "Average Sedentary Minutes"
        ],
        "value": [
            activity["id"].nunique(),
            len(activity),
            round(activity["totalsteps"].mean(), 0),
            round(activity["calories"].mean(), 0),
            round(activity["totaldistance"].mean(), 2),
            round(sleep["sleep_hours"].mean(), 2),
            sleep["id"].nunique(),
            weight["id"].nunique(),
            round(weight["weightkg"].mean(), 2),
            round(weight["bmi"].mean(), 2),
            round(activity["sedentaryminutes"].mean(), 1)
        ]
    })

    print(
        summary.to_string(index=False)
    )

    summary.to_csv(
        EDA_DIR / "eda_summary.csv",
        index=False
    )

    # ========================================================
    # COMPLETED
    # ========================================================

    print("\n" + "=" * 60)
    print("EDA COMPLETED SUCCESSFULLY")
    print("=" * 60)
    print(f"EDA results saved to:")
    print(EDA_DIR)


if __name__ == "__main__":
    main()