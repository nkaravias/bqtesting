-- insert_project_for_project_code.sql

-- Replace these placeholders with actual values before executing
DECLARE var_project_code STRING DEFAULT 'replace_with_project_code';
DECLARE var_project_name STRING DEFAULT 'replace_with_project_name';
DECLARE var_description STRING DEFAULT 'replace_with_description';
DECLARE var_project_id STRING DEFAULT 'replace_with_project_id';
DECLARE var_landing_zone_id STRING DEFAULT 'replace_with_landing_zone_id';
DECLARE var_service_tier STRING DEFAULT 'replace_with_service_tier';
DECLARE var_solution_id STRING DEFAULT 'replace_with_solution_id';

BEGIN TRANSACTION;

-- Check if a project with the same project_code and service_tier already exists
IF (SELECT COUNT(*) FROM `rbsee-sandbox-asdf001.testreg.projects` 
    WHERE project_code = var_project_code 
    AND service_tier = var_service_tier) > 0 THEN
  RAISE USING MESSAGE = 'Project with the same project_code and service_tier already exists';
END IF;

-- Insert the new project
INSERT INTO `rbsee-sandbox-asdf001.testreg.projects` (
  project_name,
  project_code,
  description,
  project_id,
  landing_zone_id,
  service_tier,
  solution_id
) VALUES (
  var_project_name,
  var_project_code,
  var_description,
  var_project_id,
  var_landing_zone_id,
  var_service_tier,
  var_solution_id
);

COMMIT TRANSACTION;
