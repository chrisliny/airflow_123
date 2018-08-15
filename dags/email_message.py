from airflow import DAG
from airflow.operators.email_operator import EmailOperator
from datetime import datetime, timedelta

from airflow.models import Variable

email_to = Variable.get("operation_email")

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
  'email_message', 
  schedule_interval='@once',
  default_args=default_args
)

EmailOperator(
  task_id='email_notification',
  to=email_to,
  subject='email message from airflow',
  html_content='Airflow can send emails',
  dag=dag
)