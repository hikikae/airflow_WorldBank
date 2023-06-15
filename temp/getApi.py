#consumir de la api de word bank

import requests
import json

def extract_api_data(indicator):
    try:
        url = f"http://api.worldbank.org/v2/country/all/indicator/{indicator}?format=json" 
        response = requests.get(url)
        n = response.json()[0]['pages']
        file_path = '/opt/airflow/temp/datosPaises.tsv'
        

        with open(file_path, 'w') as file: 
            for x in range(1, n+1):
                response = requests.get(f"{url}&page={x}")
                data = response.json()[1]

                for item in data:
                    id = getKeyFromItem(item, ["country", "id"])
                    country = getKeyFromItem(item, ["country", "value"])
                    iso3code = getKeyFromItem(item, ["countryiso3code"])
                    date = getKeyFromItem(item, ["date"])
                    population = getKeyFromItem(item, ["value"])
                    
                    line = f"{id}\t{country}\t{iso3code}\t{date}\t{population}\n"
                    file.write(line)
    
    except Exception as e:
        print(e)

def getKeyFromItem(item, keys):
    try:
        for key in keys:
            item = item[key]
        return item if item else "null"    
    except KeyError:
        return "null"

def main():
    indicator= 'SP.POP.TOTL'
    extract_api_data(indicator)

main()