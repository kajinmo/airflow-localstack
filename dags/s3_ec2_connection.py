from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.amazon.aws.hooks.base_aws import AwsBaseHook

def test_s3_connection():
    hook = S3Hook(aws_conn_id='localstack_s3')
    s3_client = hook.get_conn()
    buckets = s3_client.list_buckets()
    print("Buckets:", buckets['Buckets'])
    s3_client.create_bucket(Bucket='test-airflow-bucket')

def test_ec2_connection():
    hook = AwsBaseHook(aws_conn_id='localstack_ec2', client_type='ec2')
    ec2_client = hook.get_conn()
    print(f"Tipo do cliente: {type(ec2_client)}")
    instances = ec2_client.describe_instances()
    print("Instâncias EC2:", instances)
    ec2_client.run_instances(
        ImageId='ami-df5de72bdb3b',
        InstanceType='t2.micro',
        MinCount=1,
        MaxCount=1
    )

with DAG(
    dag_id='s3_ec2_connections',
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:
    test_s3 = PythonOperator(
        task_id='test_s3',
        python_callable=test_s3_connection
    )
    test_ec2 = PythonOperator(
        task_id='test_ec2',
        python_callable=test_ec2_connection
    )

    test_s3 >> test_ec2
