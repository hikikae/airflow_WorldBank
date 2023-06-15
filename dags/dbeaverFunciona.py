from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from operators.PostgresFileOperator import PostgresFileOperator
from datetime import datetime

def insert_data_from_file():
    # Leer el archivo y realizar las inserciones en la base de datos
    with open('/opt/airflow/dags/filese.tsv','r') as file:
        for line in file:
            # Parsear los datos de cada línea del archivo y realizar la inserción
            data = line.strip().split('\t')  # Separador de tabulación ('\t')
            id = data[0]
            country = data[1]
            
            # Ejecutar la inserción en la base de datos
            # Puedes utilizar una conexión a la base de datos y ejecutar una sentencia SQL o utilizar algún ORM
            # Aquí, por simplicidad, se utiliza la misma sintaxis SQL que en el ejemplo anterior
            sql = f"INSERT INTO datos (id, country) VALUES ('{id}', '{country}')"
            # Ejecutar la sentencia SQL utilizando el operador PostgresOperator
            PostgresOperator(
                task_id="insert_data",
                postgres_conn_id="postgres_localhost",
                sql=sql
            ).execute(context={})
            

with DAG(
    dag_id='vamosSigue',
    start_date=datetime(2023, 6, 12)
) as dag:
    task_1 = PostgresOperator(
        task_id='creacion_tabla',
        postgres_conn_id="postgres_localhost",
        sql="""
            CREATE TABLE IF NOT EXISTS datos (
                id VARCHAR NOT NULL,
                country VARCHAR NOT NULL
            )
        """
    )

    task_2 = PythonOperator(
        task_id="insert_data_from_file",
        python_callable=insert_data_from_file
    )


    task_3=PostgresFileOperator(
        task_id="llenar_tabla_from_file",
        operation="write",
        config={"table_name":"datos"}
    )
    task_1 >> task_3
