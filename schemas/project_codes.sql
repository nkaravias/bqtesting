CREATE TABLE IF NOT EXISTS project_codes (
  project_code STRING NOT NULL,
  appcode STRING,
  domain STRING,
  PRIMARY KEY (project_code) NOT ENFORCED
);