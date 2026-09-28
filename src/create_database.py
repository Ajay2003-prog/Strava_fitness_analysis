from pathlib import Path
import pandas as pd
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
CLEANED_DIR = BASE_DIR / "data" / "cleaned"
DATABASE_DIR = BASE_DIR / "database"
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATABASE_DIR / "fitness.db"

TABLES = {
    "daily_activity": "daily_activity_clean.csv",
    "daily_calories": "daily_calories_clean.csv",
    "daily_steps": "daily_steps_clean.csv",
    "daily_intensities": "daily_intensities_clean.csv",
    "sleep": "sleep_clean.csv",
    "weight": "weight_clean.csv",
    "hourly_steps": "hourly_steps_clean.csv",
    "hourly_intensities": "hourly_intensities_clean.csv"
}

def create_database():
    print("=" * 60)
    print("FITNESS ANALYTICS - SQLITE DATABASE")
    print("=" * 60)
    print(f"Database: {DB_PATH}\n")

    missing = [
        file for file in TABLES.values()
        if not (CLEANED_DIR / file).exists()
    ]

    if missing:
        print("ERROR: Missing cleaned files:")
        for file in missing:
            print(f"  - {file}")
        return

    if DB_PATH.exists():
        DB_PATH.unlink()
        print("Existing database replaced.\n")

    connection = sqlite3.connect(DB_PATH)

    try:
        for table_name, file_name in TABLES.items():
            file_path = CLEANED_DIR / file_name
            df = pd.read_csv(file_path)

            df.to_sql(
                table_name,
                connection,
                if_exists="replace",
                index=False
            )

            print(
                f"{table_name}: "
                f"{len(df):,} rows, "
                f"{len(df.columns)} columns"
            )

        connection.commit()

        print("\n" + "=" * 60)
        print("DATABASE CREATED SUCCESSFULLY")
        print("=" * 60)
        print(f"Location: {DB_PATH}")

    finally:
        connection.close()

if __name__ == "__main__":
    create_database()