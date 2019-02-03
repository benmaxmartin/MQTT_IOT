import paho.mqtt.publish as publish
import sys

print("Start chatting: \n")

while(True):
	payload = sys.argv[1]+input()
	publish.single(sys.argv[2], payload, hostname="iot.eclipse.org")