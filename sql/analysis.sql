-- ============================================================
-- FITNESS ANALYTICS - SQL ANALYSIS
-- ============================================================


-- ============================================================
-- 1. OVERALL DATASET SUMMARY
-- ============================================================

SELECT
    COUNT(DISTINCT Id) AS total_users,
    COUNT(*) AS total_records,
    ROUND(AVG(TotalSteps), 0) AS avg_daily_steps,
    ROUND(AVG(Calories), 0) AS avg_daily_calories,
    ROUND(AVG(TotalDistance), 2) AS avg_daily_distance
FROM daily_activity;


-- ============================================================
-- 2. DAILY ACTIVITY STATISTICS
-- ============================================================

SELECT
    ROUND(AVG(TotalSteps), 0) AS avg_steps,
    MIN(TotalSteps) AS min_steps,
    MAX(TotalSteps) AS max_steps,
    ROUND(AVG(Calories), 0) AS avg_calories,
    MIN(Calories) AS min_calories,
    MAX(Calories) AS max_calories,
    ROUND(AVG(SedentaryMinutes), 0) AS avg_sedentary_minutes
FROM daily_activity;


-- ============================================================
-- 3. ACTIVITY LEVEL BY USER
-- ============================================================

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
ORDER BY avg_steps DESC;


-- ============================================================
-- 4. ACTIVITY LEVEL DISTRIBUTION
-- ============================================================

SELECT
    activity_level,
    COUNT(*) AS user_count
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
ORDER BY user_count DESC;


-- ============================================================
-- 5. DAILY STEPS TREND
-- ============================================================

SELECT
    ActivityDate,
    ROUND(AVG(TotalSteps), 0) AS avg_steps,
    ROUND(AVG(Calories), 0) AS avg_calories
FROM daily_activity
GROUP BY ActivityDate
ORDER BY ActivityDate;


-- ============================================================
-- 6. HIGHEST ACTIVITY DAYS
-- ============================================================

SELECT
    ActivityDate,
    ROUND(AVG(TotalSteps), 0) AS avg_steps,
    ROUND(AVG(Calories), 0) AS avg_calories
FROM daily_activity
GROUP BY ActivityDate
ORDER BY avg_steps DESC
LIMIT 10;


-- ============================================================
-- 7. LOWEST ACTIVITY DAYS
-- ============================================================

SELECT
    ActivityDate,
    ROUND(AVG(TotalSteps), 0) AS avg_steps,
    ROUND(AVG(Calories), 0) AS avg_calories
FROM daily_activity
GROUP BY ActivityDate
ORDER BY avg_steps ASC
LIMIT 10;


-- ============================================================
-- 8. ACTIVITY INTENSITY
-- ============================================================

SELECT
    ROUND(AVG(VeryActiveMinutes), 1) AS very_active_minutes,
    ROUND(AVG(FairlyActiveMinutes), 1) AS fairly_active_minutes,
    ROUND(AVG(LightlyActiveMinutes), 1) AS lightly_active_minutes,
    ROUND(AVG(SedentaryMinutes), 1) AS sedentary_minutes
FROM daily_activity;


-- ============================================================
-- 9. SLEEP ANALYSIS
-- ============================================================

SELECT
    COUNT(DISTINCT Id) AS users_with_sleep_data,
    ROUND(AVG(TotalMinutesAsleep) / 60.0, 2) AS avg_sleep_hours,
    ROUND(AVG(TotalTimeInBed) / 60.0, 2) AS avg_time_in_bed_hours
FROM sleep;


-- ============================================================
-- 10. SLEEP BY USER
-- ============================================================

SELECT
    Id,
    ROUND(AVG(TotalMinutesAsleep) / 60.0, 2) AS avg_sleep_hours,
    ROUND(AVG(TotalTimeInBed) / 60.0, 2) AS avg_time_in_bed_hours,
    ROUND(
        AVG(TotalTimeInBed - TotalMinutesAsleep),
        0
    ) AS avg_awake_in_bed_minutes
FROM sleep
GROUP BY Id
ORDER BY avg_sleep_hours DESC;


-- ============================================================
-- 11. SLEEP AND ACTIVITY RELATIONSHIP
-- CORRECTED: MATCH USER + DATE
-- ============================================================

SELECT
    s.Id,
    ROUND(
        AVG(s.TotalMinutesAsleep) / 60.0,
        2
    ) AS avg_sleep_hours,
    ROUND(
        AVG(a.TotalSteps),
        0
    ) AS avg_steps,
    ROUND(
        AVG(a.Calories),
        0
    ) AS avg_calories
FROM sleep s
JOIN daily_activity a
    ON s.Id = a.Id
    AND DATE(s.SleepDay) = DATE(a.ActivityDate)
GROUP BY s.Id
ORDER BY avg_sleep_hours DESC;


-- ============================================================
-- 12. HOURLY STEPS
-- ============================================================

SELECT
    strftime('%H', ActivityHour) AS hour,
    ROUND(AVG(StepTotal), 0) AS avg_steps
FROM hourly_steps
GROUP BY hour
ORDER BY hour;


-- ============================================================
-- 13. MOST ACTIVE HOURS
-- ============================================================

SELECT
    strftime('%H', ActivityHour) AS hour,
    ROUND(AVG(StepTotal), 0) AS avg_steps
FROM hourly_steps
GROUP BY hour
ORDER BY avg_steps DESC
LIMIT 10;


-- ============================================================
-- 14. HOURLY INTENSITY
-- ============================================================

SELECT
    strftime('%H', ActivityHour) AS hour,
    ROUND(AVG(TotalIntensity), 2) AS avg_intensity,
    ROUND(AVG(AverageIntensity), 2) AS avg_average_intensity
FROM hourly_intensities
GROUP BY hour
ORDER BY hour;


-- ============================================================
-- 15. WEIGHT AND BMI
-- ============================================================

SELECT
    COUNT(DISTINCT Id) AS users_with_weight_data,
    ROUND(AVG(WeightKg), 2) AS avg_weight_kg,
    ROUND(AVG(BMI), 2) AS avg_bmi
FROM weight;


-- ============================================================
-- 16. WEIGHT BY USER
-- ============================================================

SELECT
    Id,
    ROUND(AVG(WeightKg), 2) AS avg_weight_kg,
    ROUND(AVG(BMI), 2) AS avg_bmi
FROM weight
GROUP BY Id
ORDER BY avg_weight_kg DESC;


-- ============================================================
-- 17. SEDENTARY BEHAVIOR BY USER
-- ============================================================

SELECT
    Id,
    ROUND(AVG(SedentaryMinutes), 0) AS avg_sedentary_minutes,
    ROUND(AVG(TotalSteps), 0) AS avg_steps
FROM daily_activity
GROUP BY Id
ORDER BY avg_sedentary_minutes DESC;


-- ============================================================
-- 18. VERY ACTIVE USERS
-- ============================================================

SELECT
    Id,
    ROUND(AVG(VeryActiveMinutes), 1) AS avg_very_active_minutes,
    ROUND(AVG(TotalSteps), 0) AS avg_steps
FROM daily_activity
GROUP BY Id
ORDER BY avg_very_active_minutes DESC
LIMIT 10;