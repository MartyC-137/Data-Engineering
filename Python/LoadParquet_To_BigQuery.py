from google.cloud import bigquery
# Construct a BigQuery client object.
client = bigquery.Client()
# TODO(developer): Set table_id to the ID of the table to create.
table_id = "your-project.your-dataset.your-table"
job_config = bigquery.LoadJobConfig(source_format=bigquery.SourceFormat.PARQUET,)
uri = "gs://your-cloud-storage-uri"
load_job = client.load_table_from_uri(
    uri, table_id, job_config=job_config
)  # Make an API request.
load_job.result()  # Waits for the job to complete.
destination_table = client.get_table(table_id)
print("Loaded {} rows.".format(destination_table.num_rows))