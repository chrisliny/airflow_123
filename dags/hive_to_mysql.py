from airflow import DAG
from airflow.operators.hive_to_mysql import HiveToMySqlTransfer
from airflow.operators.mysql_operator import MySqlOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta

default_args = {
  'owner': 'airflow',
  'start_date': days_ago(2),
  'email_on_failure': False,
  'email_on_retry': False,
  'retries': 1,
  'retry_delay': timedelta(minutes=1)
}

dag = DAG(
  dag_id='hive_to_mysql',
  schedule_interval='@once',
  default_args=default_args
)

t1 = MySqlOperator(
  task_id='drop_table',
  sql='drop table if exists temp_drivers',
  dag=dag
)
t2 = HiveToMySqlTransfer(
  task_id='hive_to_mysql',
  mysql_table='temp_drivers',
  mysql_preoperator='create table temp_drivers(col_value varchar(256))',
  sql='select * from temp_drivers',
  dag=dag
)

t1 >> t2