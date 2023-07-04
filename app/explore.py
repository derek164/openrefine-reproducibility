import duckdb
import pandas as pd
from pathlib import Path

file = Path(__file__).parent / "data" / "wine-raw.csv"

conn = duckdb.connect()
wine_df = pd.read_csv(file)
conn.register("wine", wine_df)

results = conn.execute(
    """
    SELECT title, count(*) as count
    FROM wine
    GROUP BY title
    HAVING count(*) > 2
"""
).df()

print(results.to_string())
