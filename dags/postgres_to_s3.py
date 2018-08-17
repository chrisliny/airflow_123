from airflow import DAG
from airflow.hooks.postgres_hook import PostgresHook
from airflow.hooks.S3_hook import S3Hook
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta, date
from decimal import Decimal

import json

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
  'postgres_to_s3', 
  schedule_interval='@once',
  default_args=default_args  
)

def _query_postgres(sql):
  hook = PostgresHook(schema='weather')
  conn = hook.get_conn()
  cursor = conn.cursor()
  cursor.execute(sql)
  return cursor 

def _cursor_to_json(cursor):
  data = []
  schema = list(map(lambda schema_tuple: schema_tuple[0], cursor.description))

  for row in cursor:
    row = map(_convert_types, row)
    row_dict = dict(zip(schema, row))
    data.append(row_dict)

  return json.dumps(data)

def _convert_types(value):
    """
    Decimals are converted to floats. 
    """
    if isinstance(value, Decimal):
        return float(value)
    else:
        return value

def _upload_to_s3(key, bucket_name, str_data):
  hook = S3Hook(aws_conn_id='aws_default')  
  hook.load_string(str_data, key, bucket_name=bucket_name, encoding='utf-8', replace=True)


def get_data_from_postgres(sql, key, bucket_name, *args, **kwargs):
  cursor = _query_postgres(sql)
  str_data = _cursor_to_json(cursor)
  _upload_to_s3(key, bucket_name, str_data)

PythonOperator(
  task_id="process",
  python_callable=get_data_from_postgres,
  op_args=['select * from drivers;', 'driver-data/driver_from_postgres.json', 'wdt-datalake'],
  provide_context=True,
  dag=dag
)