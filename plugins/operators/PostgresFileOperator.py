from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.providers.postgres.hooks.postgres import PostgresHook

class PostgresFileOperator(BaseOperator):

    @apply_defaults
    def __init__(self,
                operation,
                config={},
                *args,
                **kwargs):
        
        super(PostgresFileOperator,self).__init__(*args,**kwargs)
        self.operation=operation
        self.config=config
        self.postgres_hook= PostgresHook(postgres_conn_id='postgres_localhost')

    def execute(self,context):
        if self.operation=="write":
            self.writeInTable()
        elif self.operation=="read":
            pass
    
    def writeInTable(self):
        self.postgres_hook.bulk_load(self.config.get('table_name'), '/opt/airflow/temp/datosPaises.tsv')
