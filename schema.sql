CREATE TABLE IF NOT EXISTS metrics
(
  id INTEGER (8) PRIMARY KEY AUTOINCREMENT,
  insert_ts INTEGER (8),
  sensor_id TEXT (255),
  metric TEXT (MAX),
  ts REAL,
  ts_iso8601 TEXT (MAX),
  value REAL
);
