from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from operators.PostgresFileOperator import PostgresFileOperator
from datetime import datetime

         

with DAG(
    dag_id='pipelineWorldBank',
    start_date=datetime(2023, 6, 12)
) as dag:
    task_1 = PostgresOperator(
        task_id='creacion_tabla',
        postgres_conn_id="postgres_localhost",
        sql="""
            CREATE TABLE IF NOT EXISTS datos (
                id VARCHAR,
                country VARCHAR, 
                iso3code VARCHAR,
                date VARCHAR,
                population VARCHAR
            )
        """
    )

    task_2 = BashOperator(
        task_id="insert_data_from_api",
        bash_command="python /opt/airflow/temp/getApi.py"
    )


    task_3=PostgresFileOperator(
        task_id="llenar_tabla_from_file",
        operation="write",
        config={"table_name":"datos"}
    )

    task_1 >> task_2 >> task_3
