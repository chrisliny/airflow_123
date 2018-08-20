from airflow import DAG
from airflow.hooks.S3_hook import S3Hook
from airflow.operators.sensors import S3KeySensor
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta

import os

cwd = os.getcwd()
local_file = os.path.join(cwd, "s3_sensor_test123.csv")

start_date = days_ago(2)
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
  dag_id='s3_sensor_123',
  schedule_interval='@once',
  default_args=default_args
)

def download(key, bucket_name, local_file):
  hook = S3Hook(aws_conn_id='aws_default')
  data = hook.read_key(key, bucket_name)
  with open(local_file, 'wb') as file:
      file.write(data) 

bucket_key = 'driver-data/s3_sensor.csv'
bucket_name = 'wdt-datalake'

t0 = S3KeySensor(
  task_id='s3_sensor',
  bucket_key=bucket_key,
  bucket_name=bucket_name,
  sla=timedelta(minutes=2),
  dag=dag
)

t1 = PythonOperator(
  task_id='download',
  python_callable = download,
  op_args=[bucket_key, bucket_name, local_file],
  dag=dag
)

t0 >> t1