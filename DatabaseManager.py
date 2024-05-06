"""
A class to manage timeseries sensor data from the timescaleDB database. 
"""
from sqlalchemy import create_engine, Table, MetaData, URL
from sqlalchemy.exc import SQLAlchemyError


class DatabaseManager:
    def __init__(self, credentials:dict) -> None:  

        """
        Init with database credentials and create the database engine
        
        """
        self.credentials = credentials
        self.url_object = URL.create(
            "postgresql+psycopg2",
            username=self.credentials['db_user'],
            password=self.credentials['db_password'], 
            host=self.credentials['db_host'],
            port=self.credentials['db_port'],
            database=self.credentials['db_name']
            )
        
        self.engine = self.connect_to_database()
        

    def connect_to_database(self):
        """
        Create and return the SQLAlchemy database engine.
        """
        try:
            engine = create_engine(self.url_object)
            return engine
        except SQLAlchemyError as e:
            print(f"Error connecting to the database: {e}")
            return None

    def get_database_table(self, table:str):
        pass

    def get_sensor_timeseries(self, table:str, sensor:str):
        pass
