import requests
import logging
import os
import pandas as pd
import configparser


logging.basicConfig(filename=os.path.join(os.getcwd(),'logs','api_requests.log'), level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class APIRequest:
    def __init__(self, API):
        config = configparser.ConfigParser()
        config_path = os.path.join(os.getcwd(), 'src', 'API', 'config.ini')
        config.read(config_path)
        self.url = config[API]['url']
        self.api_token = config[API]['api_token']       

    def _collect_data_(self):
        headers = {
            'Authorization': f'Bearer {self.api_token}'
        }
        try:
            response = requests.get(self.url, headers=headers)
            logging.info(f'Request URL: {self.url}')
            logging.info(f'Status Code: {response.status_code}')
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                logging.error(f'Request failed with status code {response.status_code}: {response.text}')
                return None    
        except requests.exceptions.RequestException as e:
            logging.error(f'An error ocurred: {e}')
            print(f'An error ocurred: {e}')
            return None
        
    def _extract_df_from_data_(self, data):
        scooter_data = []
        for scooter_info in data['data']:
            attributes = scooter_info['attributes']
            scooter_data.append({
                'state': attributes['state'],
                'lastLocationUpdate': attributes['lastLocationUpdate'],
                'batteryLevel': attributes['batteryLevel'],
                'currentRangeMeters': attributes['currentRangeMeters'],
                'lat': attributes['lat'],
                'lng': attributes['lng'],
                'maxSpeed': attributes['maxSpeed'],
                'isRentable': attributes['isRentable'],
                'vehicleType': attributes['vehicleType'],
            })    
        df = pd.DataFrame(scooter_data)
        df['time'] = pd.Timestamp("now")
        return df    

    def get(self):
        data = self._collect_data_()
        if data is not None:
            df = self._extract_df_from_data_(data)
            return df

if __name__ == '__main__':
    api = APIRequest('TIER')
    df = api.get()


