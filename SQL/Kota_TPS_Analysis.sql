USE kota_tps_analytics;

SELECT COUNT(*) AS station_rows
FROM station_daily;

SELECT COUNT(*) AS unit_rows
FROM unit_daily;

SELECT *
FROM station_daily
LIMIT 10;

SELECT *
FROM unit_daily
LIMIT 10;

-- Query 1: Overall Station Performance
SELECT
    COUNT(*) AS Total_Days,
    ROUND(SUM(Program_MU), 2) AS Total_Program_MU,
    ROUND(SUM(Actual_MU), 2) AS Total_Actual_MU,
    ROUND(SUM(Actual_MU) - SUM(Program_MU), 2) AS Generation_Variance_MU,
    ROUND((SUM(Actual_MU) / SUM(Program_MU)) * 100, 2)
        AS Program_Achievement_Percent,
    ROUND(AVG(Actual_MU), 2) AS Avg_Daily_Generation_MU
FROM station_daily;

-- Query 2: Highest Generation Day
SELECT
    Date_SQL,
    Program_MU,
    Actual_MU
FROM station_daily
ORDER BY Actual_MU DESC
LIMIT 1;

-- Query 3: Lowest Generation Day
SELECT
    Date_SQL,
    Program_MU,
    Actual_MU
FROM station_daily
ORDER BY Actual_MU ASC
LIMIT 1;

-- Query 4: Unit-wise Generation Performance
SELECT
    Unit,
    Unit_Label,
    Capacity_MW,
    ROUND(SUM(Program_MU), 2) AS Total_Program_MU,
    ROUND(SUM(Actual_MU), 2) AS Total_Actual_MU,
    ROUND(AVG(Actual_MU), 2) AS Avg_Daily_Generation_MU
FROM unit_daily
GROUP BY Unit, Unit_Label, Capacity_MW
ORDER BY Unit;

-- Query 5: Unit-wise Program Achievement
SELECT
    Unit,
    Unit_Label,
    Capacity_MW,
    ROUND(SUM(Program_MU), 2) AS Total_Program_MU,
    ROUND(SUM(Actual_MU), 2) AS Total_Actual_MU,
    ROUND(SUM(Actual_MU) - SUM(Program_MU), 2) AS Variance_MU,
    ROUND(
        (SUM(Actual_MU) / NULLIF(SUM(Program_MU), 0)) * 100,
        2
    ) AS Program_Achievement_Percent
FROM unit_daily
GROUP BY Unit, Unit_Label, Capacity_MW
ORDER BY Program_Achievement_Percent DESC;

-- Query 6: Station Outage Analysis
SELECT
    Date_SQL,
    Outage_MW,
    Actual_MU,
    Program_MU
FROM station_daily
WHERE Outage_MW > 0
ORDER BY Date_SQL;

-- Query 7: Maximum Outage Day
SELECT
    Date_SQL,
    Outage_MW,
    Program_MU,
    Actual_MU
FROM station_daily
ORDER BY Outage_MW DESC
LIMIT 1;

-- Query 8: Unit-wise Outage Analysis
SELECT
    Unit,
    Unit_Label,
    Capacity_MW,
    COUNT(*) AS Outage_Days,
    MAX(Outage_MW) AS Max_Outage_MW
FROM unit_daily
WHERE Outage_MW > 0
GROUP BY Unit, Unit_Label, Capacity_MW
ORDER BY Outage_Days DESC;

-- Query 9: Daily Generation Trend
SELECT
    Date_SQL,
    Program_MU,
    Actual_MU,
    ROUND(Actual_MU - Program_MU, 2) AS Variance_MU,
    ROUND(
        (Actual_MU / NULLIF(Program_MU, 0)) * 100,
        2
    ) AS Program_Achievement_Percent
FROM station_daily
ORDER BY Date_SQL;

-- Query 10: Days Above vs Below Program
SELECT
    SUM(CASE WHEN Actual_MU > Program_MU THEN 1 ELSE 0 END) AS Days_Above_Program,
    SUM(CASE WHEN Actual_MU < Program_MU THEN 1 ELSE 0 END) AS Days_Below_Program,
    SUM(CASE WHEN Actual_MU = Program_MU THEN 1 ELSE 0 END) AS Days_Equal_Program,
    COUNT(*) AS Total_Days
FROM station_daily;

-- Query 11: Outage vs Non-Outage Generation
SELECT
    CASE
        WHEN Outage_MW > 0 THEN 'Outage Day'
        ELSE 'No Outage Day'
    END AS Day_Type,

    COUNT(*) AS Number_of_Days,

    ROUND(AVG(Program_MU), 2) AS Avg_Program_MU,

    ROUND(AVG(Actual_MU), 2) AS Avg_Actual_MU,

    ROUND(AVG(Actual_MU - Program_MU), 2) AS Avg_Variance_MU
FROM station_daily
GROUP BY
    CASE
        WHEN Outage_MW > 0 THEN 'Outage Day'
        ELSE 'No Outage Day'
    END;
    
    -- Query 12: Coal Stock Analysis
SELECT 
    MIN(Coal_Stock_Days) AS Minimum_Coal_Stock_Days,
    MAX(Coal_Stock_Days) AS Maximum_Coal_Stock_Days,
    ROUND(AVG(Coal_Stock_Days), 2) AS Average_Coal_Stock_Days
FROM
    station_daily
WHERE
    Coal_Stock_Days IS NOT NULL;
    
    -- Query 13: Minimum Coal Stock Day
SELECT
    Date_SQL,
    Coal_Stock_Days,
    Program_MU,
    Actual_MU
FROM station_daily
WHERE Coal_Stock_Days = (
    SELECT MIN(Coal_Stock_Days)
    FROM station_daily
    WHERE Coal_Stock_Days IS NOT NULL
)
ORDER BY Date_SQL;

-- Query 14: Unit-wise PLF for 45-Day Period
SELECT
    Unit,
    Unit_Label,
    Capacity_MW,
    ROUND(SUM(Actual_MU), 2) AS Total_Actual_MU,
    ROUND(
        (SUM(Actual_MU) * 1000) /
        (Capacity_MW * COUNT(*) * 24) * 100,
        2
    ) AS PLF_Percent
FROM unit_daily
GROUP BY
    Unit,
    Unit_Label,
    Capacity_MW
ORDER BY Unit;

-- Query 15: Overall Station PLF for 45-Day Period
SELECT
    1240 AS Station_Capacity_MW,
    COUNT(*) AS Total_Days,
    ROUND(SUM(Actual_MU), 2) AS Total_Actual_MU,
    ROUND(
        (SUM(Actual_MU) * 1000) /
        (1240 * COUNT(*) * 24) * 100,
        2
    ) AS Station_PLF_Percent
FROM station_daily;





