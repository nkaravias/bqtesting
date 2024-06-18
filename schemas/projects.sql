CREATE TABLE IF NOT EXISTS projects (
  project_name STRING NOT NULL,
  project_code STRING,
  description STRING,
  project_id STRING,
  landing_zone_id STRING,
  service_tier STRING,
  solution_id STRING,
  PRIMARY KEY (project_name) NOT ENFORCED
);