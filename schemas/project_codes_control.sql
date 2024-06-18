CREATE TABLE IF NOT EXISTS project_code_control (
  appcode STRING NOT NULL,
  next_available_code INT64 NOT NULL,
  PRIMARY KEY (appcode) NOT ENFORCED
);