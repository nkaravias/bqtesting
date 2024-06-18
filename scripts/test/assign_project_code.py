import sys
from google.cloud import bigquery

def execute_sql_from_file(client, sql_file_path, params):
    with open(sql_file_path, 'r') as file:
        sql_content = file.read()

    for key, value in params.items():
        sql_content = sql_content.replace(f'replace_with_{key}', value)

    query_job = client.query(sql_content)
    query_job.result()  # Wait for the job to complete
    print(f"Executed SQL file {sql_file_path}")

def main():
    if len(sys.argv) != 7:
        print("Usage: python assign_project_code.py <appcode> <project_name> <description> <project_id> <landing_zone_id> <service_tier> <solution_id>")
        return

    appcode, project_name, description, project_id, landing_zone_id, service_tier, solution_id = sys.argv[1:]

    params = {
        'appcode': appcode,
        'project_name': project_name,
        'description': description,
        'project_id': project_id,
        'landing_zone_id': landing_zone_id,
        'service_tier': service_tier,
        'solution_id': solution_id
    }

    client = bigquery.Client(project='rbsee-sandbox-asdf001')
    execute_sql_from_file(client, 'insert_project_into_new_project_code.sql', params)

if __name__ == '__main__':
    main()
