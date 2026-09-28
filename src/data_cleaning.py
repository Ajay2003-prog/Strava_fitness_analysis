from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "Data Files" / "mturkfitbit_export_4.12.16-5.12.16" / "Fitabase Data 4.12.16-5.12.16"
CLEANED_DIR = BASE_DIR / "data" / "cleaned"
CLEANED_DIR.mkdir(parents=True, exist_ok=True)

FILES = [
    "dailyActivity_merged.csv",
    "dailyCalories_merged.csv",
    "dailyIntensities_merged.csv",
    "dailySteps_merged.csv",
    "sleepDay_merged.csv",
    "weightLogInfo_merged.csv",
    "hourlySteps_merged.csv",
    "hourlyIntensities_merged.csv"
]

def clean_names(df):
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )
    return df

def clean_text(df):
    for col in df.select_dtypes(include=["str"]).columns:
        df[col] = df[col].astype("string").str.strip()
    return df

def convert_numeric(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

def remove_negative(df, columns):
    for col in columns:
        if col in df.columns:
            df.loc[df[col] < 0, col] = pd.NA
    return df

def clean_file(filename, output, date_cols=None, numeric_cols=None, positive_cols=None):
    path = RAW_DIR / filename
    df = pd.read_csv(path)
    original_rows = len(df)

    df = clean_names(df)
    df = df.drop_duplicates()
    df = clean_text(df)

    for col in date_cols or []:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format="mixed", errors="coerce")

    df = convert_numeric(df, numeric_cols or [])
    df = remove_negative(df, numeric_cols or [])

    for col in positive_cols or []:
        if col in df.columns:
            df.loc[df[col] <= 0, col] = pd.NA

    df.to_csv(CLEANED_DIR / output, index=False)
    print(f"{output}: {original_rows:,} -> {len(df):,} rows")
    return df

def main():
    print("=" * 60)
    print("FITNESS ANALYTICS - DATA CLEANING")
    print("=" * 60)

    print(f"Raw data: {RAW_DIR}")
    print(f"Output:   {CLEANED_DIR}\n")

    missing = [f for f in FILES if not (RAW_DIR / f).exists()]

    if missing:
        print("ERROR: Missing files:")
        for f in missing:
            print(f"  - {f}")
        return

    clean_file(
        "dailyActivity_merged.csv",
        "daily_activity_clean.csv",
        ["activitydate"],
        [
            "totalsteps", "totaldistance", "trackerdistance",
            "loggedactivitiesdistance", "veryactivedistance",
            "moderatelyactivedistance", "lightactivedistance",
            "sedentaryactivedistance", "veryactiveminutes",
            "fairlyactiveminutes", "lightlyactiveminutes",
            "sedentaryminutes", "calories"
        ]
    )

    clean_file(
        "dailyCalories_merged.csv",
        "daily_calories_clean.csv",
        ["activityday"],
        ["calories"]
    )

    clean_file(
        "dailySteps_merged.csv",
        "daily_steps_clean.csv",
        ["activityday"],
        ["steptotal"]
    )

    clean_file(
        "dailyIntensities_merged.csv",
        "daily_intensities_clean.csv",
        ["activityday"],
        [
            "veryactiveminutes", "fairlyactiveminutes",
            "lightlyactiveminutes", "sedentaryminutes",
            "veryactivedistance", "moderatelyactivedistance",
            "lightactivedistance", "sedentaryactivedistance"
        ]
    )

    clean_file(
        "sleepDay_merged.csv",
        "sleep_clean.csv",
        ["sleepday"],
        ["totalsleeprecords", "totalminutesasleep", "totaltimeinbed"]
    )

    clean_file(
        "weightLogInfo_merged.csv",
        "weight_clean.csv",
        ["date"],
        ["weightkg", "weightpounds", "fat", "bmi"],
        ["weightkg", "weightpounds", "bmi"]
    )

    clean_file(
        "hourlySteps_merged.csv",
        "hourly_steps_clean.csv",
        ["activityhour"],
        ["steptotal"]
    )

    clean_file(
        "hourlyIntensities_merged.csv",
        "hourly_intensities_clean.csv",
        ["activityhour"],
        ["totalintensity", "averageintensity"]
    )

    summary = []

    for file in CLEANED_DIR.glob("*.csv"):
        if file.name == "data_quality_summary.csv":
            continue

        df = pd.read_csv(file)

        summary.append({
            "file": file.name,
            "rows": len(df),
            "columns": len(df.columns),
            "missing_values": int(df.isna().sum().sum()),
            "duplicates": int(df.duplicated().sum())
        })

    summary_df = pd.DataFrame(summary)
    summary_df.to_csv(
        CLEANED_DIR / "data_quality_summary.csv",
        index=False
    )

    print("\n" + "=" * 60)
    print("DATA CLEANING COMPLETED SUCCESSFULLY")
    print("=" * 60)
    print(f"Cleaned files saved to:\n{CLEANED_DIR}")

if __name__ == "__main__":
    main()