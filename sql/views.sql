CREATE SCHEMA IF NOT EXISTS mart;

-- Latest snapshot per city
CREATE OR REPLACE VIEW mart.latest_city_weather AS
WITH latest_day AS (
  SELECT MAX(date) AS max_date FROM staging.daily_weather
)
SELECT w.*
FROM staging.daily_weather w
JOIN latest_day l ON w.date = l.max_date
ORDER BY w.city;

-- 7-day rolling averages per city
CREATE OR REPLACE VIEW mart.city_7d_rolling AS
SELECT
  city,
  date,
  temp_max,
  temp_min,
  precip_sum,
  AVG(temp_max) OVER (PARTITION BY city ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS temp_max_avg_7d,
  AVG(precip_sum) OVER (PARTITION BY city ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS precip_avg_7d
FROM staging.daily_weather;

-- Rainy days count per city (all time)
CREATE OR REPLACE VIEW mart.rainy_days_by_city AS
SELECT
  city,
  COUNT(*) FILTER (WHERE precip_sum IS NOT NULL AND precip_sum > 0) AS rainy_days,
  COUNT(*) AS total_days
FROM staging.daily_weather
GROUP BY city
ORDER BY rainy_days DESC, city;