import os, time
from asterisk.ami import (
    AMIClient, 
    SimpleAction, 
    EventListener
    )


# OPERATOR EXTENSIONS (read from a file to a list - array)

try:
    operators_file = open("operators.txt", mode="r")
    operators_data = operators_file.read()
    operators_data_list = operators_data.split("\n")
    print(operators_data_list)
    operators_file.close()
except FileNotFoundError:
    print("File operators.txt does not exist")


# CLIENT NUMBERS (read from a file to a list - array)

try:
    clients_file = open("list.txt", mode="r")
    clients_data = clients_file.read()
    clients_data_list = clients_data.split("\n")
    print(clients_data_list)
    clients_file.close()
except FileNotFoundError:
    print("File list.txt does not exist")


# CALL FUNCTIONS

# Call operator

def callOperator(pjsipuser):
	print(f'Calling {pjsipuser}')
	action = SimpleAction(
		'Originate',
		Channel=pjsipuser,
		Exten='7005',
		Priority=1,
		Context='local',
		)
	client.send_action(action)

# Call client

def callClient(pjsipuser):
	print(f'Calling {pjsipuser}')
	action = SimpleAction(
		'Originate',
		Channel=pjsipuser,
		Exten='7006',
		Priority=1,
		Context='local',
		)
	client.send_action(action)

# Channel merging

def do_bridge(pjsipuser1,pjsipuser2):
	print(f'Channel merging {pjsipuser1} and {pjsipuser2}')
	action = SimpleAction(
		'Bridge',
		Channel1=pjsipuser1,
		Channel2=pjsipuser2,
	)
	client.send_action(action)

# Login to AMI interface of Asterisk server

client = AMIClient(address='192.168.1.200',port=5038)
client.login(username='USERNAME',secret='********')


# LIST OF OPERATORS AND CLIENTS

Operators = operators_data_list
ListOfClients = clients_data_list
N = len (Operators)
n = len (ListOfClients)
ti = 0.5
ti2= 5

def printListOfClients():
    for i in range(1,n+1):
        print(i,")",ListOfClients[i-1])

def ListOfOperators():
    os.system('cls')
    print(f'{N} operator available, select operator:"')
    for i in range(1,N+1):
        print(i,")",Operators[i-1])
    T = int(input("Operator: \n"))
    return T



# MANUAL CALL SELECT

def CallBySelection():
    a = 0
    while a != 4:
        os.system('cls')
        T = ListOfOperators()
        if T <= N:   
            print (f'Operator: {Operators[T-1]}, will call:"')
            printListOfClients()
            C = int(input("Client: "))
            if C <= n:
                os.system('cls')
                print(f'Operator {Operators[T-1]} connects: {ListOfClients[C-1]}')
                x = f'pjsip/{Operators[T-1]}'
                callOperator(x)
                time.sleep(ti)
                y = f'pjsip/{ListOfClients[C-1]}'
                callClient(y)    
                time.sleep(ti)
                do_bridge(x,y)
                time.sleep(ti2)
            else:
                print ("Client", C, "does not exist or is incorrectly entered")
                time.sleep(ti)
                break
        else:
            print ("Operator", T, "does not exist or is incorrectly entered")
            time.sleep(ti)
            break



# AUTOMATIC CALLING

def AutomaticCalls ():
    a =0
    T = ListOfOperators()
    if T <= N:
        x = f'pjsip/{Operators[T-1]}'
        while a <= n:
            os.system('cls')
            y = f'pjsip/{ListOfClients[a]}'
            print (f'Connecting {x} with client {y}')
            time.sleep(ti)
            callOperator(x)
            time.sleep(ti)
            callClient(y)    
            time.sleep(ti)
            do_bridge(x,y)
            input('PAUSE')
            a += 1
            if a >= n:
                print("You have done all calls in queue")
                break
    else:
        print ("Operator", T, "does not exist or is incorrectly entered")


# MENU

os.system('cls')
print("Menu")
print("1) Automatic calls")
print("2) Call by selection")
k = int (input())
if k == 1:
    AutomaticCalls()
elif k == 2:
    CallBySelection()
else:
    print("Option not available")


# TEST CALLING     

# x = f'pjsip/{Operators[0]}'
# callOperator(x)
# time.sleep(0.1)
# y = f'pjsip/{ListOfClients[1]}'
# callClient(y)    
# time.sleep(0.1)
# do_bridge(x,y)
# input('Press Enter to continue in Terminal')