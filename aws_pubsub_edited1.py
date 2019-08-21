# Import SDK packages
import MFRC522
import sys
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
from gpiozero import MCP3008

adc = MCP3008(channel=0)
uid = None
mfrc522 = MFRC522.MFRC522()
# Custom MQTT message callback
def customCallback(client, userdata, message):
	print("Received a new message: ")
	print(message.payload)
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")
	
host = "a2g0cpxek9vcfn-ats.iot.us-east-1.amazonaws.com"
rootCAPath = "rootca.pem"
certificatePath = "certificate.pem.crt"
privateKeyPath = "private.pem.key"

my_rpi = AWSIoTMQTTClient("PubSub-p1851830")
my_rpi.configureEndpoint(host, 8883)
my_rpi.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

my_rpi.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
my_rpi.configureDrainingFrequency(2)  # Draining: 2 Hz
my_rpi.configureConnectDisconnectTimeout(10)  # 10 sec
my_rpi.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
# my_rpi.connect()
# my_rpi.subscribe("clinic/sensors/value", 1, customCallback)
# sleep(2)

# Publish to the same topic in a loop forever
loopCount = 0
while True:
	(status,TagType) = mfrc522.MFRC522_Request(mfrc522.PICC_REQIDL)

	if status == mfrc522.MI_OK:
		(status,uid) = mfrc522.MFRC522_Anticoll()
		loopCount = loopCount+1
    	message = {}
    	message["deviceid"] = "deviceid_edwinlow"
    	import datetime as datetime
     	now = datetime.datetime.now()
     	message["datetimeid"] = now.isoformat()      
     	message["value"] = str(uid)
     	import json
		my_rpi.publish("clinic/sensors/value",json.dumps(message), 1)
		print(message)
		sleep(5)
