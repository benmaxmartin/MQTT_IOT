import paho.mqtt.subscribe as subscribe
import re
import sys

def on_message_print(client, userdata, message):
	#print("%s %s" % (message.topic, message.payload))
	reg1 = re.compile("(^{})(.*)".format(sys.argv[1]))
	reg2 = re.compile("(^{})(.*)".format(sys.argv[3]))
	tmp1 = reg1.search(message.payload.decode("utf-8"))
	tmp2 = reg2.search(message.payload.decode("utf-8"))
	if tmp1 is not None:
		print("you: "+tmp1.group(2))
	elif tmp2 is not None:
		print("{}: {}".format(tmp2.group(1),tmp2.group(2)))

print("Chat Console :\n")	
while(True):
	subscribe.callback(on_message_print, sys.argv[2], hostname="iot.eclipse.org")