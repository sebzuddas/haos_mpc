import asyncio
import yaml
import pandas as pd


from SensorDataManager import SensorDataManager
from DatabaseManager import DatabaseManager
from dotenv import dotenv_values


async def init_subscriptions(datamanager:object, subscriptions_file:str):
    """
    Reads the subscriptions file and initialises subscriptions via the datamanager object.
    """

    with open (subscriptions_file, 'r') as file:
        subscriptions = yaml.safe_load(file)
    
    for sensor_id in subscriptions.get("sensors", []):
        await datamanager.subscribe_entity(sensor_id)
    pass


async def get_database_data():
    pass


async def main():

    config = dotenv_values(".env")
    __auth = config.get("HASS_IO___auth_TOKEN")
    url = config.get("HASS_IO_HOSTNAME")
    yaml_file = config.get("YAML_NAME")

    db_name = config.get("DATABASE_NAME")
    db_host = config.get("DATABASE_HOST")
    db_port = config.get("DATABASE_PORT")
    db_user = config.get("DATABASE_USER")
    db_password = config.get("DATABASE_PASSWORD")

    credentials_dict = {
        'db_name':db_name,
        'db_host':db_host,
        'db_port':db_port,
        'db_user':db_user,
        'db_password':db_password
    }

    databasemanager = DatabaseManager(credentials=credentials_dict)# instantiate an object for the database
    table = databasemanager.get_database_table('ltss')#this returns an sqlalchemy table object. 
    
    sensor = databasemanager.get_sensor_timeseries("sensor.smart_plug_radiator_current_consumption")
    
    print(f"Table Name: {table.name}")
    for column in table.columns:
        print(f"Column: {column.name}, Type: {column.type}")

    print(sensor)





    exit()

    timeseries_schema = config.get("TIMESERIES_SCHEMA")
    timeserties_table = config.get("TIMESERIES_TABLE")



    datamanager = SensorDataManager(auth_token=__auth, websocket_url=url)
    await datamanager.connect()

    # await init_subscriptions(datamanager, yaml_file)
    sensor_data = await datamanager.fetch_sensor_state("person.seb")
    print(sensor_data)

    # states_data = await datamanager.fetch_all_states()
    # print(states_data)
    await datamanager.close()


if __name__ == "__main__":
    asyncio.run(main())
    exit()
