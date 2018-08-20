from airflow import DAG
from airflow.operators.hive_operator import HiveOperator
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta

default_args = {
  'owner': 'airflow',
  'depends_on_past': False,
  'start_date': days_ago(2),
  'email_on_failure': False,
  'email_on_retry': False,
  'retries': 1,
  'retry_delay': timedelta(minutes=1),
}

dag = DAG(
  dag_id='hdfs_to_hive',
  schedule_interval='@once',
  default_args=default_args
)

t0 = BashOperator(
  task_id='copy_file_to_hdfs',
  bash_command='hdfs dfs -copyFromLocal /tmp/drivers.csv /tmp',
  dag=dag
)

t1 = HiveOperator(
  task_id='drop_table',
  hql='DROP TABLE IF EXISTS temp_drivers',
  mapred_job_name='airflow_hivecli',
  dag=dag
)

t2 = HiveOperator(
  task_id='create_table',
  hql='CREATE TABLE temp_drivers(col_value STRING);',
  dag=dag
)

t3 = HiveOperator(
  task_id='load_data',
  hql='LOAD DATA INPATH "/tmp/drivers.csv" OVERWRITE INTO TABLE temp_drivers',
  dag=dag
)

t0 >> t1 >> t2 >> t3