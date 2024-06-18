import os
import re
import argparse
from google.cloud import bigquery

def qualify_table_names(sql_content, project_id, dataset_id):
    # Qualify table names in CREATE TABLE statements
    create_table_pattern = re.compile(r'\bCREATE TABLE IF NOT EXISTS (\w+)\b', re.IGNORECASE)
    sql_content = create_table_pattern.sub(rf'CREATE TABLE IF NOT EXISTS `{project_id}.{dataset_id}.\1`', sql_content)

    # Qualify table names in INSERT INTO statements
    insert_into_pattern = re.compile(r'\bINSERT INTO (\w+)\b', re.IGNORECASE)
    sql_content = insert_into_pattern.sub(rf'INSERT INTO `{project_id}.{dataset_id}.\1`', sql_content)

    return sql_content

def execute_sql_file(client, sql_file_path, project_id, dataset_id):
    with open(sql_file_path, 'r') as file:
        sql_content = file.read()
    
    # Qualify table names with project and dataset
    sql_content = qualify_table_names(sql_content, project_id, dataset_id)

    query_job = client.query(sql_content)
    query_job.result()  # Wait for the job to complete
    print(f"Executed SQL file {sql_file_path}")

def execute_all_sql_files_in_folder(client, folder_path, project_id, dataset_id, mode):
    for sql_file in sorted(os.listdir(folder_path)):
        if sql_file.endswith('.sql'):
            sql_file_path = os.path.join(folder_path, sql_file)
            print(f"Executing {mode} file: {sql_file_path}")
            execute_sql_file(client, sql_file_path, project_id, dataset_id)

def main():
    parser = argparse.ArgumentParser(description="Execute schema or data SQL files in BigQuery.")
    parser.add_argument('--project_id', type=str, required=True, help="Google Cloud project ID")
    parser.add_argument('--dataset_id', type=str, required=True, help="BigQuery dataset ID")
    parser.add_argument('--mode', type=str, choices=['schema', 'data', 'all_schemas', 'all_data'], required=True, help="Mode of operation: 'schema' to execute a single schema file, 'data' to execute a single data file, 'all_schemas' to execute all schema files, 'all_data' to execute all data files")
    parser.add_argument('--sql_file', type=str, help="Path to the SQL file to be executed (required for 'schema' and 'data' modes)")
    parser.add_argument('--folder_path', type=str, help="Path to the folder containing SQL files (required for 'all_schemas' and 'all_data' modes)")

    args = parser.parse_args()

    project_id = args.project_id
    dataset_id = args.dataset_id
    mode = args.mode
    sql_file_path = args.sql_file
    folder_path = args.folder_path

    # Initialize BigQuery client with explicit project ID
    client = bigquery.Client(project=project_id)

    if mode in ['schema', 'data']:
        if not sql_file_path:
            parser.error("the following arguments are required: --sql_file")
        execute_sql_file(client, sql_file_path, project_id, dataset_id)
    elif mode == 'all_schemas':
        if not folder_path:
            parser.error("the following arguments are required: --folder_path")
        execute_all_sql_files_in_folder(client, folder_path, project_id, dataset_id, 'schema')
    elif mode == 'all_data':
        if not folder_path:
            parser.error("the following arguments are required: --folder_path")
        execute_all_sql_files_in_folder(client, folder_path, project_id, dataset_id, 'data')

if __name__ == '__main__':
    main()