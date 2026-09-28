from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "fitness.db"

TABLES = [
    "daily_activity",
    "daily_calories",
    "daily_steps",
    "daily_intensities",
    "sleep",
    "weight",
    "hourly_steps",
    "hourly_intensities"
]

def main():
    print("=" * 60)
    print("FITNESS ANALYTICS - DATABASE VALIDATION")
    print("=" * 60)

    if not DB_PATH.exists():
        print(f"ERROR: Database not found:\n{DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        print("\nChecking tables...\n")

        for table in TABLES:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"[OK] {table}: {count:,} rows")

        cursor.execute("""
            SELECT
                COUNT(DISTINCT Id),
                ROUND(AVG(TotalSteps), 0),
                ROUND(AVG(Calories), 0)
            FROM daily_activity
        """)

        users, avg_steps, avg_calories = cursor.fetchone()

        print("\nChecking sample query...\n")
        print(f"Total users:      {users:,}")
        print(f"Average steps:    {avg_steps:,.0f}")
        print(f"Average calories: {avg_calories:,.0f}")

        print("\nChecking activity levels...\n")

        cursor.execute("""
            SELECT activity_level, COUNT(*) AS user_count
            FROM (
                SELECT
                    Id,
                    CASE
                        WHEN AVG(TotalSteps) >= 10000 THEN 'Highly Active'
                        WHEN AVG(TotalSteps) >= 7500 THEN 'Active'
                        WHEN AVG(TotalSteps) >= 5000 THEN 'Moderately Active'
                        ELSE 'Less Active'
                    END AS activity_level
                FROM daily_activity
                GROUP BY Id
            )
            GROUP BY activity_level
            ORDER BY user_count DESC
        """)

        results = cursor.fetchall()

        for level, count in results:
            print(f"{level}: {count}")

        print("\nChecking user-level activity...\n")

        cursor.execute("""
            SELECT
                Id,
                ROUND(AVG(TotalSteps), 0) AS avg_steps,
                ROUND(AVG(Calories), 0) AS avg_calories,
                CASE
                    WHEN AVG(TotalSteps) >= 10000 THEN 'Highly Active'
                    WHEN AVG(TotalSteps) >= 7500 THEN 'Active'
                    WHEN AVG(TotalSteps) >= 5000 THEN 'Moderately Active'
                    ELSE 'Less Active'
                END AS activity_level
            FROM daily_activity
            GROUP BY Id
            ORDER BY avg_steps DESC
            LIMIT 10
        """)

        print("Top 10 users by average steps:\n")

        for row in cursor.fetchall():
            user_id, steps, calories, level = row
            print(
                f"ID: {user_id} | "
                f"Steps: {steps:,.0f} | "
                f"Calories: {calories:,.0f} | "
                f"{level}"
            )

        print("\n" + "=" * 60)
        print("DATABASE VALIDATION COMPLETED SUCCESSFULLY")
        print("=" * 60)

    except sqlite3.Error as e:
        print(f"\nSQL ERROR: {e}")

    finally:
        conn.close()

if __name__ == "__main__":
    main()