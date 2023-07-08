import duckdb
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.stats import shapiro

root = Path(__file__).parent
wine_dirty = pd.read_csv(root / "data" / "wine_dirty.csv")
wine_clean = pd.read_csv(root / "data" / "wine_clean.csv")

conn = duckdb.connect()
conn.register("wine_dirty", wine_dirty)
conn.register("wine_clean", wine_clean)

# results = conn.execute(
#     """
#     SELECT title
#         , count(*) as count
#     FROM wine_dirty
#     GROUP BY title
#     HAVING count(*) > 2
# """
# ).df()
# print(results.to_string())

# results = conn.execute(
#     """
#     SELECT country
#         , median(points) as median_score
#         , count(*) as count
#     FROM wine_dirty
#     GROUP BY country
#     ORDER BY median(points) DESC
# """
# ).df()
# print(results.to_string())

results = conn.execute(
    """
    SELECT country
        , COUNT(DISTINCT variety) AS num_varieties
    FROM wine_dirty
    WHERE country IS NOT NULL
        AND variety IS NOT NULL
    GROUP BY country
    ORDER BY COUNT(DISTINCT variety) DESC
    LIMIT 10
"""
).df()
print(results.to_string())

# results = conn.execute(
#     """
#     SELECT country
#         , avg(points) as sample_mean
#         , avg(points) - 1.96 * stddev_pop(points) / sqrt(count(*)) as lower_95
#         , avg(points) + 1.96 * stddev_pop(points) / sqrt(count(*)) as upper_95
#         , count(*) as sample_size
#     FROM wine_clean
#     GROUP BY country
#     HAVING count(*) > 30
#     ORDER BY avg(points) - 1.96 * stddev_pop(points) / sqrt(count(*)) DESC
# """
# ).df()
# print(results.to_string())

results = conn.execute(
    """
    SELECT title
        , AVG(points) AS sample_mean
    FROM wine_clean
    WHERE title IS NOT NULL
    GROUP BY title
    ORDER BY AVG(points) DESC
    LIMIT 10
"""
).df()
print(results.to_string())

results = conn.execute(
    """
    SELECT SUM(CASE WHEN sample_size >= 30 THEN 1 ELSE 0 END) AS region_clt_valid
        , SUM(CASE WHEN sample_size < 30 THEN 1 ELSE 0 END) AS region_clt_invalid
    FROM (
        SELECT region_1 AS region
            , COUNT(*) AS sample_size
        FROM wine_clean
        GROUP BY region_1
        ORDER BY COUNT(*) DESC
    )
"""
).df()
print(results.to_string())

df = conn.execute(
    """
    SELECT points, region_1 as region
    FROM wine_clean
    WHERE region_1 in 
    (
        SELECT region_1
        FROM wine_clean
        GROUP BY region_1
        HAVING COUNT(*) >= 30
    )
    ORDER BY region_1
"""
).df()

df = (
    df.groupby("region")
    .apply(lambda x: pd.Series(shapiro(x["points"]), index=["stat", "p-value"]))
    .reset_index()
    .sort_values("p-value", ascending=False)
)
df["normal"] = df["p-value"] > 0.05
print(df.head(10).to_string())

true_count = df["normal"].sum()
false_count = len(df) - true_count
total_count = true_count + false_count
print(f"true: {true_count, round(true_count / total_count * 100, 2)}")
print(f"false: {false_count, round(false_count / total_count * 100, 2)}")
