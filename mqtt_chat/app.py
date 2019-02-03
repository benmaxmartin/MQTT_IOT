from getpass import getpass
import requests
import os
from multiprocessing import Process

def fun(*argv):
	os.system("start /wait cmd /c python {}".format(" ".join(argv)))
	
def user_validate(**kwargs):
    payload = kwargs
    res = requests.get('http://127.0.0.1:5000/api/v1.0/UserValidation',params = payload).json()
    if res['status'] == 200 :
        return 0
    elif res['status'] == 203:
        return 1
    else :
        return 2

def user_register(**kwargs):
    payload = kwargs
    res = requests.get('http://127.0.0.1:5000/api/v1.0/UserValidation',params = payload).json()
    if res['status'] == 200 or res['status'] == 203:
        return 1
    else:
        res = requests.get('http://127.0.0.1:5000/api/v1.0/UserRegistration',params = payload).json()
        if res['status'] == 200 :
            return 0
        else :
            return 2

def chat():
	print("Welcome to MQTT chat application\n")

	u = ''
	while(True):
		choice = input("Are you a registered user ?(Y/N): ")
		if choice.lower() == 'y':
			u = input("Username: ")
			p = getpass("Password: ")
			if user_validate(username=u,password=p) == 2 :
				c = ''
				while c == '' :
					c = input("you are not a registered user , Please provide your contact: ")
				if user_register(username=u,password=p,contact=c) == 0:
					print("you are now a registered user !!")
					break
				else:
					print("We couldn't register you , please re-enter your details")
					continue
			elif user_validate(username=u,password=p) == 1 :
				print("wrong password !!")
				continue
			else:
				break
		elif choice.lower() == "n":
			u = input("Username: ")
			p = getpass("Password: ")
			c = input("Contact: ")
			if user_register(username=u,password=p) == 1 :        
				print("User already registered")
				continue
			else:
				if user_register(username=u,password=p,contact=c) == 0:
					print("you are now a registered user !!")
					break
				else:
					print("We couldn't register you , please re-enter your details")
					continue
		else:
			continue
				
	print("List of current subscribers")

	res = requests.get('http://127.0.0.1:5000/api/v1.0/AllUsers').json()            

	for i,d in enumerate(res) :
		print("{}. {}".format(i+1,d))

	choice = 0
	friend_name = ''
		
	while(True):
		choice = input("Please enter whome you want to chat: ")
		friend_name = res[int(choice)-1]
		if friend_name == u :
			print("You are not planning to chat with yourself , are you !!")
		else :
			break


	x = requests.get('http://127.0.0.1:5000/api/v1.0/UserSignature',params = {'username':u}).json()['signature']
	y = requests.get('http://127.0.0.1:5000/api/v1.0/UserSignature',params = {'username':friend_name}).json()['signature']      

	topic = (lambda xs,ys : hex(int(x, 16) ^ int(y, 16)))(x,y)
	return (topic , u , friend_name)
	
	
if __name__ == "__main__":
	op = chat()
	print(op)
	p1 = Process(target = fun,args=('subscriber.py',op[1],op[0],op[2]))
	p2 = Process(target = fun,args=('publisher.py',op[1],op[0]))
	p1.start()
	p2.start()
	p1.join()
	p2.join()

