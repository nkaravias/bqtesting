-- insert_project_into_new_project_code.sql

-- Replace these placeholders with actual values before executing
DECLARE appcode STRING DEFAULT 'replace_with_appcode';
DECLARE project_name STRING DEFAULT 'replace_with_project_name';
DECLARE description STRING DEFAULT 'replace_with_description';
DECLARE project_id STRING DEFAULT 'replace_with_project_id';
DECLARE landing_zone_id STRING DEFAULT 'replace_with_landing_zone_id';
DECLARE service_tier STRING DEFAULT 'replace_with_service_tier';
DECLARE solution_id STRING DEFAULT 'replace_with_solution_id';

BEGIN TRANSACTION;

DECLARE next_project_code STRING;

-- Determine the next available project code
SET next_project_code = (
  WITH existing_codes AS (
    SELECT project_code
    FROM `rbsee-sandbox-asdf001.testreg.project_codes`
  ),
  all_possible_codes AS (
    SELECT LPAD(CAST(code AS STRING), 3, '0') AS project_code
    FROM UNNEST(GENERATE_ARRAY(1, 999)) AS code
  )
  SELECT MIN(project_code)
  FROM all_possible_codes
  LEFT JOIN existing_codes
  USING (project_code)
  WHERE existing_codes.project_code IS NULL
);

-- Insert the new project code into the project_codes table
INSERT INTO `rbsee-sandbox-asdf001.testreg.project_codes` (
  project_code,
  appcode,
  domain
) VALUES (
  next_project_code,  -- This should be the result from the previous step
  appcode,
  'domain_value'
);

-- Insert the new project record
INSERT INTO `rbsee-sandbox-asdf001.testreg.projects` (
  project_name,
  project_code,
  description,
  project_id,
  landing_zone_id,
  service_tier,
  solution_id
) VALUES (
  project_name,
  next_project_code,  -- Use the newly allocated project code
  description,
  project_id,
  landing_zone_id,
  service_tier,
  solution_id
);

COMMIT TRANSACTION;
