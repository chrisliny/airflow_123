# Airflow 123

## Installation

---

```bash
mkproject -f -p `which python` airflow_123 

export AIRFLOW_HOME=`pwd`

pip install apache-airflow[postgres,s3,slack]

```

## Configuration

---

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

## Deploy dags: email_message

---

```bash
airflow variables -s operation_email alert@example.com

airflow list_dags

airflow list_tasks email_message

airflow test email_message email_notification 2017-08-01
```

## Deploy dags: slack_message

---

```bash
export SLACK_API_TOKEN="XXXXXXXXXXXXX"

airflow list_dags

airflow list_tasks slack_message

airflow test slack_message slack_notification 2017-08-01


```

