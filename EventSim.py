import mysql.connector
import random
import os
from dotenv import load_dotenv

load_dotenv()
def create_connection():
    connection = mysql.connector.connect(
    host = os.getenv('DB_HOST'),
    user = os.getenv('DB_USER'),
    password = os.getenv('DB_PASSWORD'),
    database = os.getenv('DB_NAME')
    )
    return connection

conn = create_connection()
event_probabilities={
        'E1' :0.23,
        'E2':0.07,
        'E3':0.05,
        'E4':0.05,
        'E5':0.06,
        'E6':0.03,
        'E7':0.02,
        'E8':0.02,
        'E9':0.03,
        'E10':0.03,
        'E11':0.03,
        'E12':0.03,
        'E13':0.04,
        'E14':0.01,
        'E15':0.03,
        'E16':0.02,
        'E17':0.04,
        'E18':0.01,
        'E19':0.01,
        'E20':0.02,
        'E21':0.02,
        'E22':0.01,
        'E23':0.01,
        'E24':0.01,
        'E25':0.01,
        'E26':0.01,
        'E27':0.02,
        'E28':0.01,
        'E29':0.02,
        'SC1':0.001,
        'SC2':0.001,
        'SC3':0.0045,
        'SC4':0.005,
        'SC5':0.001,
        'SD1':0.0005,
        'SD2':0.005,
        'SD3':0.0025,
        'SD4':0.001,
        'SD5':0.0035,
        'T1':0.0005,
        'T2':0.005,
        'T3':0.002,
        'T4':0.005,
        'L1':0.0005,
        'L2':0.001,
        'L3':0.0005,
        'L4':0.0015,
        'L5':0.0015,
        'L6':0.0075
}
#make sure the sum of the probability it's 1
print(sum(event_probabilities.values()))