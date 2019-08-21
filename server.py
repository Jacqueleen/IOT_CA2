from flask import Flask, render_template, jsonify,request

app = Flask(__name__)
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
from gpiozero import LED
led = LED(18)

def ledOn():
    GPIO.setup(18, GPIO.OUT)
    GPIO.output(18,True)
    return "Clinic light is ON."

def ledOff():
    GPIO.setup(18, GPIO.OUT)
    GPIO.output(18,False)
    return "Clinic light is OFF."

@app.route("/writeLED/<status>")
def writePIN(status):

   if status == 'On':
     response = ledOn()
   else:
     response = ledOff()

   return response

import dynamodb
import jsonconverter as jsonc

@app.route("/api/getdata",methods=['POST','GET'])
def apidata_getdata():
    if request.method == 'POST' or request.method == 'GET':
        try:
            data = {'chart_data': jsonc.data_to_json(dynamodb.get_data_from_dynamodb()), 
             'title': "IOT Data"}
            return jsonify(data)

        except:
            import sys
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])

@app.route("/")
def home():
    return render_template("index.html")


app.run(debug=True,host="0.0.0.0")