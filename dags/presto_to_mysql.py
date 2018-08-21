from airflow import DAG
from airflow.operators.presto_to_mysql import PrestoToMySqlTransfer
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
  dag_id='presto_to_mysql',
  schedule_interval='@daily',
  default_args=default_args
)

PrestoToMySqlTransfer(
  task_id='presto_to_mysql',
  sql='select * from hive.default.drivers',
  mysql_table='drivers',
  mysql_preoperator='create table if not exists drivers(driverid bigint, name varchar(128), ssn varchar(10), location varchar(256), certified varchar(1), wageplan varchar(8))',
  dag=dag

)