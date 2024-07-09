from django.core.management.base import BaseCommand
from app.models import SymbolData  # Adjust this import according to your actual app structure
import requests
from datetime import datetime
from django.db import connection
import json
from kiteconnect import KiteConnect
import time
import pyotp, random
from requests import Session
from kiteconnect import KiteTicker
from kiteconnect import KiteConnect
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By



# Define the path to the configuration file
config_file_path = 'data.json'

# Read the JSON file
with open(config_file_path, 'r') as config_file:
    config = json.load(config_file)


class Command(BaseCommand):
    help = 'Fetch symbol data from API and save/update to SymbolData model'

    def reset_sequence(self, table_name):
        with connection.cursor() as cursor:
            if connection.vendor == 'sqlite':
                cursor.execute(f"UPDATE sqlite_sequence SET seq = 0 WHERE sqlite_sequence.name = '{table_name}'")
            elif connection.vendor == 'postgresql':
                sequence_name = f"{table_name}_id_seq"
                cursor.execute(f"ALTER SEQUENCE {sequence_name} RESTART WITH 1")
            elif connection.vendor == 'mysql':
                cursor.execute(f"ALTER TABLE {table_name} AUTO_INCREMENT = 1")
            else:
                raise NotImplementedError(f"Reset sequence not implemented for database backend {connection.vendor}")

    def handle(self, *args, **kwargs):
        # url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
        SymbolData.objects.all().delete()
        self.reset_sequence('app_symboldata')
        # SymbolData.objects.all().delete()
        try:
            
            self.data = self.read_json('data.json')
            kite = KiteConnect(api_key=self.data["api_key"])
            try:
                kite_data = kite.generate_session(self.data["request_token"], api_secret=self.data["api_secret"])
            except:
                request_token = self.get_request_token(kite)
                kite_data = kite.generate_session(request_token, api_secret=self.data["api_secret"])

            kite.set_access_token(kite_data["access_token"])

            data = kite.instruments()
            # Prepare SymbolData instances for bulk operations
            symbol_data_instances = []
            for item in data:
               
                # Assuming expiry is available in the item data
                expiry_date_str = item.get("expiry", "")
                
                # Parse the expiry_date string to a date object
                expiry_date = datetime.strptime(str(expiry_date_str), '%Y-%m-%d').date() if expiry_date_str else None
                
                # Create or update SymbolData instance
                symbol_data_instances.append(
                    SymbolData(
                        instrument_token=item["instrument_token"],
                        tradingsymbol=item["tradingsymbol"],
                        name=item["name"],
                        expiry=expiry_date,
                        exchange=item["exchange"],
                        segment=item["segment"],
                        instrument_type=item["instrument_type"]

                    )
                )
            
            # Bulk create or update SymbolData instances
            SymbolData.objects.bulk_create(symbol_data_instances, ignore_conflicts=True)
            
            self.stdout.write(self.style.SUCCESS('Successfully fetched and saved symbol data.'))
        
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Error fetching data from API: {str(e)}"))

    def get_otp(self):
        return pyotp.TOTP("6YNNSWI4EEGO24UZT5O4K54APWRU4G2L").now()

    def random_sleep(self):
        time.sleep(random.randint(5,7))

    def write_json(self, data: dict, file_name: str=''):
        with open(file_name, 'w') as file :
            json.dump(data, file, indent=4)

    def read_json(self, file_name:str=''):
        f = open(file_name)
        return json.load(f)



    def get_request_token(self, kite):
        driver = uc.Chrome()
        driver.get(kite.login_url())
        self.random_sleep()
        driver.find_element(By.ID,'userid').send_keys('PCW343')
        self.random_sleep()
        driver.find_element(By.ID, 'password').send_keys('Bhavin@123')
        self.random_sleep()
        driver.find_element(By.XPATH, '//*[@type="submit"]').click()
        self.random_sleep()
        driver.find_element(By.ID,'userid').send_keys(self.get_otp())
        self.random_sleep()
        request_token = driver.current_url.split('request_token=')[-1]
        self.data["request_token"] = request_token
        self.write_json(self.data, 'data.json')
        return request_token
