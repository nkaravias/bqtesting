CREATE TABLE IF NOT EXISTS appcodes (
  appcode STRING NOT NULL,
  custodian STRING,
  L3 STRING,
  L4 STRING,
  L5 STRING,
  PRIMARY KEY (appcode) NOT ENFORCED
);