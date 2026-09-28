from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "fitness.db"
SQL_PATH = BASE_DIR / "sql" / "analysis.sql"

def main():
    print("=" * 60)
    print("FITNESS ANALYTICS - SQL ANALYSIS")
    print("=" * 60)

    conn = sqlite3.connect(DB_PATH)

    sql = SQL_PATH.read_text(encoding="utf-8")
    queries = [q.strip() for q in sql.split(";") if q.strip()]

    print(f"\nRunning {len(queries)} SQL analyses...\n")

    for i, query in enumerate(queries, 1):
        try:
            result = pd.read_sql_query(query, conn)

            print(f"Analysis {i}: {len(result):,} rows")
            print(result.head(5).to_string(index=False))
            print("-" * 60)

        except Exception as e:
            print(f"Analysis {i} ERROR: {e}")

    conn.close()

    print("\n" + "=" * 60)
    print("SQL ANALYSIS COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    main()

