# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
from gpiozero import MCP3008
import sys
import Adafruit_DHT

adc = MCP3008(channel=0)

# Custom MQTT message callback
def customCallback(client, userdata, message):
	print("Received a new message: ")
	print(message.payload)
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")
	
host = "a1073pumnlekl1-ats.iot.us-east-1.amazonaws.com"
rootCAPath = "rootca.pem"
certificatePath = "certificate.pem.crt"
privateKeyPath = "private.pem.key"

my_rpi = AWSIoTMQTTClient("PubSub-p1738032")
my_rpi.configureEndpoint(host, 8883)
my_rpi.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

my_rpi.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
my_rpi.configureDrainingFrequency(2)  # Draining: 2 Hz
my_rpi.configureConnectDisconnectTimeout(10)  # 10 sec
my_rpi.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
my_rpi.connect()
my_rpi.subscribe("sensors/light", 1, customCallback)
sleep(2)

pin = 4

# Publish to the same topic in a loop forever
loopCount = 0
while True:
      light = round(1024-(adc.value*1024))
      loopCount = loopCount+1
      message = {}
      message["deviceid"] = "raspberrypi-1738032-keithteo"
      import datetime as datetime
      now = datetime.datetime.now()
      message["datetimeid"] = now.isoformat()
      message["value"] = light
      humidity, temperature = Adafruit_DHT.read_retry(11, pin)
      message["temperature"] = temperature
      message["humidity"] = humidity
      import json
      my_rpi.publish("sensors/light", json.dumps(message), 1)
      sleep(5)
