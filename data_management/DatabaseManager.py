"""
The `DatabaseManager` class in Python initializes a database engine with given credentials,
retrieves database tables, and fetches time-series data for a specific sensor entity.
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
            
    def get_timeseries(self, sensor: str, table: str='ltss') -> pd.DataFrame:
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
                df = df.drop(["entity_id"], axis=1)# drop the entity id since we've asked for it in the method call
                df['time'] = pd.to_datetime(df['time'])# make time a datetime var
                df.set_index('time', inplace=True)#make time the index

                df = self._resample_timeseries(df)

            return df

    def get_list(self):
        #TODO: implement getting a list of all appropriate elements ie sensors/actuators
        pass

    def _resample_timeseries(self, df) -> pd.DataFrame:
        """
        This Python function resamples a time series DataFrame to a common time interval based on the most
        common time difference between samples.
        
        :param df: The `resample_timeseries` function takes a DataFrame `df` as input and resamples it based
        on the most common time interval found in the index of the DataFrame. The function calculates the
        most common time interval between samples, rounds it to the nearest second, and then uses this
        rounded interval to
        :return: The function `resample_timeseries` is returning a resampled DataFrame with forward-filled
        values based on the most common time interval found in the input DataFrame `df`.
        """
        
        time_diffs = df.index.to_series().diff() # get the difference between sample times
        rounded_interval = time_diffs.mode()[0]# find most common time interval
        common_interval_seconds = round(rounded_interval.total_seconds()) # find the most common and round
        rounded_sample_time = pd.Timedelta(seconds=common_interval_seconds) # make these a Timedelta object
        
        #TODO: handle this properly, why do some timeseries returning div zero errors? Is it because not enough data is there?
        try:
            df = df.resample(rounded_sample_time).ffill()   
            return df
        except ZeroDivisionError:
            return df



        