import duckdb
import pandas as pd
from pathlib import Path

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
    SELECT sum(case when sample_size >= 30 then 1 else 0 end) as region_clt_valid
        , sum(case when sample_size < 30 then 1 else 0 end) as region_clt_invalid
    FROM (
        SELECT region_1 as region
            , count(*) as sample_size
        FROM wine_clean
        GROUP BY region_1
        ORDER BY count(*) DESC
    )
"""
).df()
print(results.to_string())
