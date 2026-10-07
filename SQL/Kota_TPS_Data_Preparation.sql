USE kota_tps_analytics;
SELECT COUNT(*) AS total_rows
FROM station_daily;

SELECT *
FROM station_daily
LIMIT 10;

SELECT COUNT(*) AS total_unit_rows
FROM unit_daily;

SELECT *
FROM unit_daily
LIMIT 10;

ALTER TABLE station_daily
ADD COLUMN Date_New DATE;

DESCRIBE station_daily;

ALTER TABLE station_daily
DROP COLUMN Date_New;

SHOW COLUMNS FROM station_daily;

ALTER TABLE station_daily
CHANGE COLUMN `ï»¿Date` `Date_Text` TEXT;

ALTER TABLE station_daily
ADD COLUMN Date_SQL DATE;

UPDATE station_daily
SET Date_SQL = STR_TO_DATE(Date_Text, '%d-%b-%Y');

SET SQL_SAFE_UPDATES = 0;
UPDATE station_daily
SET Date_SQL = STR_TO_DATE(Date_Text, '%d-%b-%Y');

SELECT Date_Text, Date_SQL
FROM station_daily
LIMIT 10;

ALTER TABLE unit_daily
CHANGE COLUMN `ï»¿Date` `Date_Text` TEXT;

ALTER TABLE unit_daily
ADD COLUMN Date_SQL DATE;

UPDATE unit_daily
SET Date_SQL = STR_TO_DATE(Date_Text, '%d-%b-%Y');

SELECT Date_Text, Date_SQL, Unit
FROM unit_daily
LIMIT 10;