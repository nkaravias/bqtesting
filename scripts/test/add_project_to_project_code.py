import sys
from google.cloud import bigquery

def add_project(client, project_id, dataset_id, project_label, appcode, service_tier):
    sql = f"""
    DECLARE next_project_code STRING;
    DECLARE prefix STRING;
    DECLARE project_name STRING;

    BEGIN TRANSACTION;

    -- Determine the next available project code
    SET next_project_code = (
      WITH existing_codes AS (
        SELECT project_code
        FROM `{project_id}.{dataset_id}.project_codes`
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
    INSERT INTO `{project_id}.{dataset_id}.project_codes` (
      project_code,
      appcode,
      domain
    ) VALUES (
      next_project_code,  -- This should be the result from the previous step
      '{appcode}',
      'domain_value'
    );

    -- Check if a project with the same project_code and service_tier already exists
    IF (SELECT COUNT(*) FROM `{project_id}.{dataset_id}.projects` 
        WHERE project_code = next_project_code 
        AND service_tier = '{service_tier}') > 0 THEN
      RAISE USING MESSAGE = 'Project with the same project_code and service_tier already exists';
    END IF;

    -- Determine project_name based on the provided logic
    SET prefix = IF('{service_tier}' = 'nonp', 'n', 'p');
    SET project_name = CONCAT(prefix, LOWER('{appcode}'), '-', next_project_code, '-', '{project_label}');

    -- Insert the new project record
    INSERT INTO `{project_id}.{dataset_id}.projects` (
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
      'Description for ' || project_name,
      project_name || '_id',
      'lz_' || project_name,
      '{service_tier}',
      'sol_' || project_name
    );

    COMMIT TRANSACTION;

    SELECT next_project_code;
    """

    query_job = client.query(sql)
    results = query_job.result()  # Wait for the job to complete

    for row in results:
        print(f"Successfully added project with project code {row['next_project_code']}")

def main():
    if len(sys.argv) != 4:
        print("Usage: python add_project_to_project_code.py <project_label> <appcode> <service_tier>")
        return

    project_label, appcode, service_tier = sys.argv[1:]

    project_id = 'rbsee-sandbox-asdf001'
    dataset_id = 'testreg'

    client = bigquery.Client(project=project_id)
    add_project(client, project_id, dataset_id, project_label, appcode, service_tier)

if __name__ == '__main__':
    main()
