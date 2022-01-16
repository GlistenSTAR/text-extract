import mysql.connector
import sys
import boto3
import os

ENDPOINT="textract.czhhj2yyt7he.us-east-2.rds.amazonaws.com"
PORT="3306"
USER="admin"
REGION="us-east-2a"
DBNAME="textract"
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'
passwd = "kCjpSdt5f7s7FQ7CD4kf"

def save_db(all_blocks):
  #gets the credentials from .aws/credentials
  session = boto3.Session(region_name = REGION)
  client = session.client('rds')

  # token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USER, Region=REGION)

  try:
      conn =  mysql.connector.connect(host=ENDPOINT, user=USER, passwd=passwd, port=PORT, database=DBNAME)
      cur = conn.cursor()
      myquery = "INSERT INTO Result (Adres, Bouwjaar, Class, Compactheid, Datum_registratie, Energy, Koeling, Ventilatie, Verwarming, Vloeroppervlakte, Isolatie, Warm_water, Woningtype, Zonneboiler, Zonnepanelen) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
      val = (all_blocks['Adres'], all_blocks['Bouwjaar'], all_blocks['Class'], all_blocks['Compactheid'], all_blocks['Datum registratie'], all_blocks['Energy'], all_blocks['Koeling'], all_blocks['Ventilatie'], all_blocks['Verwarming'], all_blocks['Vloeroppervlakte'], str(all_blocks['Isolatie']), all_blocks["Warm water"], all_blocks["Woningtype"], all_blocks["Zonneboiler"], all_blocks["Zonnepanelen"])
      cur.execute(myquery, val)
      conn.commit()
      print("Successfully inserted the db!")
      success = True
  except Exception as e:
      print("Database connection failed due to {}".format(e))  
      success = False  
  return success
  