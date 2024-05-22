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


    # radiator_switch = Actuator(dbmanager=dbmanager, identifier="switch.smart_plug_radiator")

    room_temperature = Sensor(dbmanager=dbmanager, identifier="sensor.esphome_web_38fb3c_bme280_temperature")
    room_temperature_x, room_temperature_y = room_temperature.get_timeseries(numpy=True)
    room_temperature_y_detrend = SignalProcessing.detrend(room_temperature_y)
    room_temperature_timestep = room_temperature.get_timestep()
    SignalProcessing.psd(room_temperature_y, room_temperature_timestep, plot=True)




    # SignalProcessing.fourier_transform(room_temperature_y, timestep=30, plot=True)
    filtered_indoor_temp = SignalProcessing.butter_lowpass_filter(data=room_temperature_y, cutoff=0.0075, timestep=30)
    # SignalProcessing.fourier_transform(filtered_indoor_temp, timestep=30, plot=True)
    SignalProcessing.psd(filtered_indoor_temp, room_temperature_timestep, plot=True)
    # print(SignalProcessing.signaltonoise(room_temperature_y), SignalProcessing.signaltonoise(room_temperature_y, detrend=True), SignalProcessing.signaltonoise(filtered_data))

    outside_temperature = Sensor(dbmanager=dbmanager, identifier="sensor.home_realfeel_temperature")
    outside_temp_timestep = outside_temperature.get_timestep()
    outside_temp_timeseries_x, outside_temp_timeseries_y = outside_temperature.get_timeseries(numpy=True)
    # SignalProcessing.fourier_transform(outside_temp_timeseries_y, outside_temp_timestep, plot=True)
    # SignalProcessing.butter_lowpass_filter(data=outside_temp_timeseries_y, cutoff=0.0002, timestep=outside_temp_timestep, plot=True)

    #TODO: radiator consumption data can't be filtered as above if you use the whole dataset since there are a lot of on/offs and it creates a lot of problems with overshooting.
    #TODO: solution could be to collect the 'on' states together then distribute them once the data is filtered. This may cause issues with the timestep. 
    radiator_consumption = Sensor(dbmanager=dbmanager, identifier="sensor.smart_plug_radiator_current_consumption")
    radiator_consumption_timestep = radiator_consumption.get_timestep()
    radiator_consumption_timeseries_x, radiator_consumption_timeseries_y = radiator_consumption.get_timeseries(numpy=True)
    SignalProcessing.fourier_transform(radiator_consumption_timeseries_y, timestep=radiator_consumption_timestep, plot=True)
    SignalProcessing.butter_lowpass_filter(data=radiator_consumption_timeseries_y, cutoff=0.02, timestep=radiator_consumption_timestep, plot=True)


    #TODO: make timeseries from sensors and actuators align
    #TODO: cutoff time to consider only when the heater is on and when it's turned off?
    #TODO: Investigate cleaning data for system identification. 
    #TODO: Investigate multi-rate system identificaiton


    exit()

    
    test = SystemIdentification(radiator_input, radiator_output)
    test.fit_model_pysindy()



### show plot
    # plt.show()
    exit()

    timeseries_schema = config.get("TIMESERIES_SCHEMA")
    timeserties_table = config.get("TIMESERIES_TABLE")



### websocket code. 
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
