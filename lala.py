import os
from google.cloud import bigquery

# Hardcoded project ID and dataset ID
project_id = 'rbsee-sandbox-asdf001'
dataset_id = 'testreg'

# Initialize BigQuery client with explicit project ID
client = bigquery.Client(project=project_id)

def load_csv_to_bigquery(project_id, dataset_id, table_id, file_path):
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
    )

    with open(file_path, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_ref, job_config=job_config)

    job.result()  # Wait for the job to complete.
    print(f"Loaded {job.output_rows} rows into {table_ref} from {file_path}.")

def main():
    data_folder = 'data'

    # Load all CSV files in the data folder
    for data_file in sorted(os.listdir(data_folder)):
        if data_file.endswith('.csv'):
            table_id = data_file.split('.')[0]  # Assumes table name is the same as the CSV file name without the extension
            file_path = os.path.join(data_folder, data_file)
            load_csv_to_bigquery(project_id, dataset_id, table_id, file_path)

if __name__ == '__main__':
    main()
