from google.cloud import bigquery

def get_next_project_code(client, project_id, dataset_id):
    query = f"""
    WITH existing_codes AS (
        SELECT project_code
        FROM `{project_id}.{dataset_id}.project_codes`
    ),
    all_possible_codes AS (
        SELECT LPAD(CAST(code AS STRING), 3, '0') AS project_code
        FROM UNNEST(GENERATE_ARRAY(1, 999)) AS code
    )
    SELECT MIN(project_code) AS next_project_code
    FROM all_possible_codes
    LEFT JOIN existing_codes
    USING (project_code)
    WHERE existing_codes.project_code IS NULL
    """
    
    query_job = client.query(query)
    results = query_job.result()
    
    for row in results:
        return row.next_project_code

def main():
    project_id = 'rbsee-sandbox-asdf001'
    dataset_id = 'testreg'

    client = bigquery.Client(project=project_id)
    next_project_code = get_next_project_code(client, project_id, dataset_id)
    
    if next_project_code:
        print(f"The next available project code is: {next_project_code}")
    else:
        print("No available project codes found.")

if __name__ == '__main__':
    main()
