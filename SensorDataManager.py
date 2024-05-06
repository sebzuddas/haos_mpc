"""
A class to manage the interaction between the python applicaiton and HAOS
"""

import asyncio
import websockets
import json
import logging

class SensorDataManager:
    def __init__(self, auth_token: str, websocket_url: str) -> None:
        """
        Create an object to manage the authentication and the handling of data to and from HAOS.
        """
        self.auth_token: str = auth_token
        self.websocket_url: str = websocket_url
        self.message_id: int = 1# has to be more than zero. Has to increment. 
        self.subscribed_events: dict = {}# to retain ID's for subscribed events or triggers. 

    async def connect(self) -> None:
        """
        Method to connect to the HAOS instance via a Websocket
        """
        self.connection = await websockets.connect(self.websocket_url)
        try:
            await self.__authenticate()
        except Exception as e:
            print(f"Error during authentication: {e}")
            await self.connection.close()
            raise

    async def __authenticate(self) -> None:
        # Await the initial `auth_required` message from the server
        response = await self.connection.recv()
        auth_required = json.loads(response)
        if auth_required.get("type") != "auth_required":
            raise Exception("Unexpected response during authentication phase")

        # Send the authentication message with the access token
        auth_message = json.dumps({"type": "auth", "access_token": self.auth_token})
        await self.connection.send(auth_message)

        # Await the server's response to authentication
        response = await self.connection.recv()
        auth_response = json.loads(response)

        if auth_response.get("type") == "auth_ok":
            print("Authentication successful")
        elif auth_response.get("type") == "auth_invalid":
            raise Exception(f"Authentication failed: {auth_response.get('message')}")
        else:
            raise Exception("Unexpected response during authentication phase")

    async def fetch_sensor_state(self, sensor_id) -> dict:
        """
        Method to fetch specific sensor data and output the json as a dictionary
        """
        sensor_request = json.dumps(
            {"id": self.message_id, "type": "get_states"}
        )
        await self.connection.send(sensor_request)
        data = await self.connection.recv()
        self.message_id += 1
        data_dict = json.loads(data)
        
        try: 
            sensor_data = await self.__find_entity_by_id(data_dict, sensor_id)
            if sensor_id == None:
                raise NameError
        except NameError as n:
            print(f"Sensor ID could not be found:\n{n}")

        #clears the variable to save cache
        data.clear()
        data_dict.clear()
        return sensor_data

    async def __find_entity_by_id(self, data, entity_id):
        """
        Search for a specific entity in the given data by its entity_id.
        
        Args:
            data (dict): The complete JSON-like data structure.
            entity_id (str): The entity ID to look for (e.g., 'person.seb').

        Returns:
            dict: The matching entity dictionary or None if not found.
        """
            
        if data.get('type') == 'result' and data.get('success'):
            for entity in data.get('result', []):
                if entity.get('entity_id') == entity_id:
                    return entity

        return None  # Return None if the entity was not found

    async def fetch_all_states(self) -> dict:
        """
        Method to fetch all states present in HAOS at the time the request is sent.
        """
        states_request = json.dumps({
            "id": self.message_id, 
            "type": "get_states"
        })

        if not self.connection:
            logging.error("WebSocket connection is not established.")
            return {}

        try:
            # Log the outgoing request for debugging purposes
            logging.info(f"Sending request: {states_request}")
            await self.connection.send(states_request)

            # Receive and log the server response
            data = await self.connection.recv()
            logging.info(f"Raw response received: {data}")

            self.message_id += 1

            # Parse and return the JSON response
            return json.loads(data)

        except Exception as e:
            logging.error(f"Error during fetch_all_states: {e}")
            return {}

    async def subscribe(self, event:str, type:str) -> bool:
        """
        A method to subscribe to events or triggers. 
        Attributes:
        event - string - the event or trigger name. 
        type -  string - declares whether the event is a trigger or not
        """


        # states_request = json.dumps({
        #     'id': self.message_id,
        #     'type': 'get_states'
        # })
        # await self.connection.send(states_request)
        # data = await self.connection.recv()
        # self.message_id += 1
        # return json.loads(data)

        pass

    async def unsubscribe(self, event=None):
        success = False
        """
        A method to unsubscribe from a signular event or trigger. 
        The event parameter determines what to unsubscribe from.
        If the event is a single string then one single event is unsubscribed from. 
        If the event is a list then the list of events is unsubscribed from. 
        If the event is None then all are unsubscribed from (DEFAULT)
        """

        if event == str:
            self.__unsubscribe_single()
        
        elif event == list:
            self.__unsubscribe_list()
        
        elif event == None:
            self.__unsubscribe_all()

        else:
            raise ValueError('Please enter either a string, list or None')



        pass

    async def __unsubscribe_single(self, event_list:str):
        """
        A method to unsubscribe from a list of events
        """
        pass

    async def __unsubscribe_list(self, event_list:list):
        """
        A method to unsubscribe from a list of events
        """
        pass

    async def __unsubscribe_all(self):
        """
        A method to unsubscribe from all events or triggers. 
        """

        pass

    async def fire_event(self, event):
        """
        A method to fire events. 
        """
        pass

    async def call_service(self, service):
        """
        A method to call a service.
        """
        pass

    async def fetch_config(self):
        """
        A method to fetch the config of the HAOS instance.
        """
        pass

    async def fetch_all_services(self):
        """
        A method to fetch all services currently running within HAOS.
        """
        pass

    async def fetch_panels(self):
        """
        A method toget a dump of the current registered panels in HAOS.
        """

    async def ping_pong(self):
        """ 
        A method to check connection via a ping pong response to HAOS. 
        """

    async def __error_handling(self):
        """
        Method to handle errors
        """

        pass

    async def close(self):
        await self.connection.close()
