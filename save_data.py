import mysql.connector
import sys
import boto3
import os

from env import ENDPOINT, PORT, USER, REGION, DBNAME, passwd

os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

def save_db(all_blocks, type):
  #gets the credentials from .aws/credentials
  session = boto3.Session(region_name = REGION)
  client = session.client('rds')

  # token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USER, Region=REGION)

  try:
      conn =  mysql.connector.connect(host=ENDPOINT, user=USER, passwd=passwd, port=PORT, database=DBNAME)
      cur = conn.cursor()
      
      if(type == "1"):
        myquery = "INSERT INTO result1 (Adres, Bouwjaar, Class, Compactheid, Datum_registratie, Energy, Koeling, Ventilatie, Verwarming, Vloeroppervlakte, Isolatie, Warm_water, Woningtype, Zonneboiler, Zonnepanelen, Bag_ID, Registratienummer) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (all_blocks['Adres'], all_blocks['Bouwjaar'], all_blocks['Class'], all_blocks['Compactheid'], all_blocks['Datum registratie'], all_blocks['Energy'], all_blocks['Koeling'], all_blocks['Ventilatie'], all_blocks['Verwarming'], all_blocks['Vloeroppervlakte'], str(all_blocks['Isolatie']), all_blocks["Warm water"], all_blocks["Woningtype"], all_blocks["Zonneboiler"], all_blocks["Zonnepanelen"], all_blocks["Bag_ID"], all_blocks["Registratienummer"])
      elif(type == "2"):
        myquery = "INSERT INTO result2 (Adres, Aparte_warmtapwatervoorziening, Bouwperiode, Dakisolatie, Datum_van_registratie, Gevelisolatie, Glas_slaapruimte, Glas_woonruimte, Ventilatie, Verwarming, Vloerisolatie, Woningtype, Woonoppervlakte, Zonne_energie, Tip, Energielabel, Bag_ID, Registratienummer) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (all_blocks['Adres'], all_blocks['Aparte warmtapwatervoorziening'], all_blocks['Bouwperiode'], all_blocks['Dakisolatie'], all_blocks['Datum van registratie'], all_blocks['Gevelisolatie'], all_blocks['Glas slaapruimte'], all_blocks['Glas woonruimte'], all_blocks['Ventilatie'], all_blocks['Verwarming'], all_blocks["Vloerisolatie"],  all_blocks["Woningtype"], all_blocks["Woonoppervlakte"], all_blocks["Zonne-energie"], str(all_blocks['Tip']), all_blocks["Energielabel"], all_blocks["Bag_ID"], all_blocks["Registratienummer"])  
      
      cur.execute(myquery, val)
      conn.commit()
      print("Successfully inserted the db!")
      success = True
  except Exception as e:
      print("Database connection failed due to {}".format(e))  
      success = False  
  return success
  