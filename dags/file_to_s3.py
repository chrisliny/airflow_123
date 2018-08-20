from airflow import DAG
from airflow.hooks.S3_hook import S3Hook
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago

from airflow.operators.python_operator import PythonOperator

import os

cwd = os.getcwd()
local_file = os.path.join(cwd, "logs", "test.csv")

start_date = datetime.now() - timedelta(days=1)

default_args = {
  'owner': 'airflow',
  'depends_on_past': False,
  'start_date': start_date,
  'email_on_failure': False,
  'email_on_retry': False,
  'retries': 1,
  'retry_delay': timedelta(minutes=1),
}

dag = DAG(
  'file_to_s3', 
  schedule_interval='@once',
  default_args=default_args
)

def upload(key, bucket_name, local_file):
  hook = S3Hook(aws_conn_id='aws_default')
  hook.load_file(local_file, key, bucket_name=bucket_name , replace=True)

PythonOperator(
  task_id='upload',
  python_callable = upload,
  op_args=['driver-data/timesheet-test.csv', 'wdt-datalake', local_file],
  dag=dag
)
