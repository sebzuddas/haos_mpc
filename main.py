import asyncio
import yaml
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# import data handlers
from data_management.SensorDataManager import SensorDataManager
from data_management.DatabaseManager import DatabaseManager
from peripherals.Sensor import Sensor
from peripherals.Actuator import Actuator

from dotenv import dotenv_values

from control.SystemIdentification import SystemIdentification
from control.SignalProcessing import SignalProcessing


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


async def make_column_numeric(dataframe:object, colname:str = 'state'):
    return pd.to_numeric(dataframe[colname])

async def main():

    config = dotenv_values(".env")
    auth = config.get("HASS_IO_AUTH_TOKEN")
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


    dbmanager = DatabaseManager(credentials=credentials_dict)# instantiate an object for the database
    # table = dbmanager.get_database_table('ltss')#this returns an sqlalchemy table object. 
    
    # print(f"Table Name: {table.name}")
    # for column in table.columns:
    #     print(f"Column: {column.name}, Type: {column.type}")

### Computers
    """
    computers_sensor = dbmanager.get_sensor_timeseries("sensor.smart_plug_computers_current_consumption")

    computers_sensor = computers_sensor[computers_sensor.state != 'unavailable']# drop unavailable

    computers_sensor["state"] = np.where(computers_sensor["state"] == "unavailable", 0, computers_sensor["state"])# change unavailable to zero
    
    computer_sensor_state = pd.to_numeric(computers_sensor["state"], errors='coerce')

    computer_sensor_state.plot()
    """

### Radiators
        

    sensor_name_list = [
        "sensor.smart_plug_radiator_current_consumption", 
        "sensor.esphome_web_38fb3c_bme280_temperature",
        "sensor.home_realfeel_temperature",
        ]

    actuator_name_list = ["switch.smart_plug_radiator"]

    radiator_consumption = Sensor(dbmanager=dbmanager, identifier="sensor.smart_plug_radiator_current_consumption")

    room_temperature = Sensor(dbmanager=dbmanager, identifier="sensor.esphome_web_38fb3c_bme280_temperature")

    outside_temperature = Sensor(dbmanager=dbmanager, identifier="sensor.home_realfeel_temperature")

    radiator_switch = Actuator(dbmanager=dbmanager, identifier="switch.smart_plug_radiator")

    room_temperature_timeseries = room_temperature.get_timeseries()
    room_temperature_x, room_temperature_y = room_temperature.get_timeseries(numpy=True)
    room_temperature_y_detrend = SignalProcessing.detrend(room_temperature_y)

    # plt.plot(room_temperature_x, room_temperature_y, color='firebrick', label='non detrend')
    # plt.plot(room_temperature_x, room_temperature_y_detrend, color='navy', label='detrend')
    # plt.legend()
    # plt.show()
    
    # SignalProcessing.fourier_transform(room_temperature_y, timestep=30, plot=True)
    filtered_data = SignalProcessing.butter_lowpass_filter(data=room_temperature_y, cutoff=0.0025, timestep=30, plot=True)
    # SignalProcessing.fourier_transform(filtered_data, timestep=30, plot=True)

    exit()

    #getting the real feel temperature and adding it to sysid
    real_feel_temp = dbmanager.get_sensor_timeseries("sensor.home_realfeel_temperature")
    real_feel_temp["state"] = pd.to_numeric(real_feel_temp["state"])
    
    #getting the switch data
    print(switch.to_string())
    
    print(real_feel_temp.to_string())
    exit()

    radiator_sensor["state"] = pd.to_numeric(radiator_sensor["state"])

    radiator_sensor["state"] = radiator_sensor["state"].rolling(window=5).mean()

    radiator_sensor[["state", "input"]].plot()# plot the sensors' state and input vars

    radiator_sensor = radiator_sensor.dropna(subset=['state'])
    # radiator_sensor = radiator_sensor[radiator_sensor["state"] != 0]# drops rows where state is zero. 

    radiator_input = radiator_sensor[["input"]]
    radiator_output = radiator_sensor[["state"]]
    
    test = SystemIdentification(radiator_input, radiator_output)
    test.fit_model_pysindy()



### show plot
    # plt.show()
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
