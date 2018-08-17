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
  's3_download', 
  schedule_interval='@once',
  default_args=default_args
)

def download(key, bucket_name, local_file):

  hook = S3Hook(aws_conn_id='aws_default')

  data = hook.read_key(key, bucket_name)

  with open(local_file, 'wb') as file:
      file.write(data) 

  
  # s3.load_string(str_data, key, bucket_name=bucket_name, encoding='utf-8', replace=True)
  # s3.load_file(filename, key, bucket_name=bucket_name , replace=True)

PythonOperator(
  task_id='download',
  python_callable = download,
  op_args=['driver-data/timesheet.csv', 'wdt-datalake', local_file],
  dag=dag
)
