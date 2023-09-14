import requests
import logging
import os
import pandas as pd


logging.basicConfig(filename='api_requests.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

api_url = "https://platform.tier-services.io/v2/vehicle?zoneId=BERLIN"  

api_token = "bpEUTJEBTf74oGRWxaIcW7aeZMzDDODe1yBoSxi2" 


headers = {
    "Authorization": f"Bearer {api_token}"
}

DATAPATH = os.path.join(os.getcwd(), 'Data', 'raw_data.csv')


def extract_df_from_data(data):
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

def collect_data():
    try:
        response = requests.get(api_url, headers=headers)

        logging.info(f"Request URL: {response.url}")
        logging.info(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            return data

        else:
            logging.error(f"Request failed with status code {response.status_code}: {response.text}")
            print(f"Request failed with status code {response.status_code}: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
        return None
    
def main():
    collected_data = collect_data()
    if collected_data is not None:
        df = extract_df_from_data(collected_data)
        df.to_csv(DATAPATH, mode='a', header=True, index=False)

        # Log the end of the data collection
        logging.info("Data collection completed.")    


if __name__ == '__main__':
    main()        