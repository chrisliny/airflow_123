from airflow import DAG
from airflow.operators.slack_operator import SlackAPIPostOperator
from datetime import datetime, timedelta

import os

token = os.environ['SLACK_API_TOKEN']

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
  'slack_message', 
  schedule_interval='@once',
  default_args=default_args
)

SlackAPIPostOperator(
  task_id='slack_notification',
  username='Airflow',
  token=token,
  channel='#general',
  text='From airflow: sending slack message',
  icon_url='http://airbnb.io/img/projects/airflow3.png',
  dag=dag
)