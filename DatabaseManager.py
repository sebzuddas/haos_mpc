"""
A class to manage timeseries sensor data from the timescaleDB database. 
"""
from sqlalchemy import create_engine, Table, MetaData, URL
from sqlalchemy.sql import table, column, select
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd

class DatabaseManager:
    def __init__(self, credentials:dict) -> None:  

        """
        Init with database credentials and create the database engine
        """

        self.__credentials = credentials
        self.url_object = URL.create(
            "postgresql+psycopg2",
            username=self.__credentials['db_user'],
            password=self.__credentials['db_password'], 
            host=self.__credentials['db_host'],
            port=self.__credentials['db_port'],
            database=self.__credentials['db_name']
            )
        
        self.engine = self.connect_to_database()
        self.ltss_table = self.get_database_table('ltss')#default hypertable for homeassistant ltss addon
        

    def connect_to_database(self):
        """
        The function `connect_to_database` creates and returns a SQLAlchemy database engine, handling any
        connection errors.
        :return: The `connect_to_database` method is returning the SQLAlchemy database engine if the
        connection is successful. If there is an SQLAlchemyError during the connection attempt, it will
        print an error message and return `None`.
        """
        try:
            engine = create_engine(self.url_object)
            return engine
        except SQLAlchemyError as e:
            print(f"Error connecting to the database: {e}")
            return None

    def get_database_table(self, table: str):
        """
        The function `get_database_table` retrieves the SQLAlchemy Table object representing a specific
        table.
        
        :param table: The `table` parameter in the `get_database_table` method is a string that represents
        the name of the database table for which you want to retrieve the SQLAlchemy Table object
        :type table: str
        :return: the SQLAlchemy Table object representing a specific table. If an error occurs during the
        retrieval of the table, it will print an error message and return None.
        """

        metadata = MetaData(schema='public')#public is the default schema for ltss
        try:
            return Table(table, metadata, autoload_with=self.engine)
        except SQLAlchemyError as e:
            print(f"Error fetching table {table}: {e}")
            return None
            
    def get_sensor_timeseries(self, sensor: str, table: str='ltss') -> pd.DataFrame:
            """
            Retrieve time-series data for a specific sensor (entity) and return as a Pandas DataFrame.

            Args:
                table (str): The name of the table containing time-series data.
                sensor (str): The entity_id of the specific sensor to query.

            Returns:
                pd.DataFrame: A DataFrame containing the time-series data for the given sensor.
            """

            table_obj = self.ltss_table
            if table_obj is None:
                return pd.DataFrame()  # Return an empty DataFrame if the table doesn't exist

            # Create a query to filter by entity_id
            stmt = select(table_obj).where(table_obj.c.entity_id == sensor).order_by(table_obj.c.time)

            # Execute the query and convert to a Pandas DataFrame
            with self.engine.connect() as connection:
                result = connection.execute(stmt)
                data = result.fetchall()
                df = pd.DataFrame(data, columns=result.keys())

            return df
