CREATE TABLE IF NOT EXISTS metrics
(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  insert_ts INTEGER NOT NULL,
  sensor_id TEXT NOT NULL,
  metric TEXT NOT NULL,
  ts REAL NOT NULL,
  ts_iso8601 TEXT NOT NULL,
  value REAL
);

CREATE INDEX IF NOT EXISTS metric_ts ON metrics (ts);
CREATE INDEX IF NOT EXISTS metric_name_ts ON metrics (metric, ts);

DROP INDEX IF EXISTS metric_name;
-- CREATE INDEX IF NOT EXISTS metric_name ON metrics (metric);
DROP INDEX IF EXISTS metric_value;
--CREATE INDEX IF NOT EXISTS metric_value ON metrics (value);
