from airflow import DAG
from airflow.operators.mysql_to_hive import MySqlToHiveTransfer
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta

default_args = {
  'ower': 'airflow',
  'start_date': days_ago(5),
  'email_on_failure': False,
  'email_on_retry': False,
  'depends_on_past': False,
  'retries': 1,
  'retry_delay': timedelta(minutes=1)
}

dag = DAG(
  dag_id='mysql_to_hive',
  template_searchpath='templates/mysql_to_hive',
  schedule_interval='@daily',
  default_args=default_args
)

MySqlToHiveTransfer(
  task_id='mysql_to_hive',
  sql='mysql_to_hive_sql.sql',
  delimiter=',',
  hive_table='mysql_to_hive_table.sql',
  create=True,
  recreate=True,
  dag=dag
)