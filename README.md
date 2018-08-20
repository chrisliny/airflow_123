# Airflow 123

## Installation

---

__Install virtualenvwrapper__ : https://virtualenvwrapper.readthedocs.io/en/latest/install.html

```bash
mkproject -f -p `which python` airflow_123 
```

> For Macos, you may need to install the followings:

>> ```bash
>> brew update
>> brew install freetds
>> pip install cython
>> pip install git+https://github.com/pymssql/pymssql
>> ```

```
pip install apache-airflow[all]

pip install psycopg2-binary

```

## Configuration

---

```bash
export AIRFLOW_HOME=`pwd`

export OPERATION_EMAIL=operation@example.com

export SLACK_API_TOKEN=XXXXXXXXXXXXX

export AIRFLOW_CONN_AWS_DEFAULT='{"login": "access key", "password": "secret key", "region_name": "us-west-2"}'

```

To send email from airflow, you need to update the following smtp section of airflow.cfg

> [smtp]

> `` # `` If you want airflow to send emails on retries, failure, and you want to use

> `` # `` the airflow.utils.email.send_email_smtp function, you have to configure an

> `` # `` smtp server here

> smtp_host = localhost

> smtp_starttls = True

> smtp_ssl = False

> `` # `` Uncomment and set the user/pass settings if you want to use SMTP AUTH

> `` # `` smtp_user = airflow

> `` # `` smtp_password = airflow

> smtp_port = 25

> smtp_mail_from = airflow@example.com

## Initialization

---

```
airflow initdb
```

## Start Airflow Webserver and Scheduler

---

```bash
airflow webserver -p 8888 > logs/webserver.log &

airflow scheduler > logs/schedule.log &

```

## Test dags: email_message

---

```bash

airflow list_dags

airflow list_tasks email_message

airflow test email_message email_notification 2017-08-01
```

## Test dags: slack_message

---

```bash

airflow list_dags

airflow list_tasks slack_message

airflow test slack_message slack_notification 2017-08-01


```

## Test dags: s3_to_file

---

```bash

airflow list_dags

airflow list_tasks file_to_s3

airflow test file_to_s3 download 2017-08-01


```

## Test dags: file_to_s3

---

```bash

airflow list_dags

airflow list_tasks file_to_s3

airflow test file_to_s3 upload 2017-08-01


```

## Test dags: postgres_to_s3

---

```bash

airflow list_dags

airflow list_tasks postgres_to_s3

airflow test postgres_to_s3 process 2017-08-01


```

## Test dags: hdfs_to_hive

---

```bash

airflow list_dags

airflow list_tasks hdfs_to_hive

airflow backfill hdfs_to_hive -s 2017-08-01 -e 2017-08-02


```

## Test dags: hdfs_to_mysql

---

Using HiveToMySqlTransfer, you need to install the followings:

```bash

## fix struct error
pip install thrift==0.9.3

pip install thrift_sasl

```

HiveToMySqlTransfer is using hiveserver2. You need to have hiveserver2 running to test this dag:

```bash

airflow list_dags

airflow list_tasks hdfs_to_mysql

airflow backfill hdfs_to_mysql -s 2017-08-01 -e 2017-08-02


```