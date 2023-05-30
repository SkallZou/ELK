import socket
import sys
import os
from datetime import datetime
import json
import glob

def UpdateEventID(filetoread, filetowrite="eventid.txt"):
    with open(filetoread, "r") as logfile, open(filetowrite, "w") as eventidfile:
        eventid = []
        data = json.load(logfile)
        for i in range(len(data['eventData'])):
            eventid.append(data['eventData'][i]['id'])
        idmax = max(eventid)
        print("......Highest ID: {0}".format(idmax))
        eventidfile.write(str(idmax))
        print("[+] Event ID file updated")
        return idmax

def main():
    HOST="0.0.0.0"
    PORT=1234
    BUFFER_SIZE = 4096
    count = 0
    now = datetime.now()
    currentdate = now.strftime("%d%m%y")
    idmax = 0

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))

    # Run for the first time the program, finding the highest id first
    # Count the number of log file
    for filename in os.listdir("./"):
        if os.path.isfile(filename) == True and filename.endswith(".log"):
            count = count + 1
    # Check if eventid.txt exist
    print("[+] Initialialization...")
    if os.path.isfile("./eventid.txt") == True and os.path.getsize("./eventid.txt") > 0:
        # File exist and is not empty => Read file that contains the id
        with open("eventid.txt", "r") as file:
            idmax = file.read().replace('\n','')
    else:
        print("[-] Warning: No event ID found")
        # Check if log file exist
        if len(glob.glob("log*.log")) > 0:
            recentfile = max(glob.glob("log*.log"), key=os.path.getctime)
            print("......Found most recent log file : {0}".format(recentfile))
            idmax =  UpdateEventID(recentfile)

        else:
            print("[!] Error: No log file found")
            quit()


    print("[+] Socket Bind Completed")
    while True:
        # Waiting for action
        request_client = ""
        receive_state = True
        server_socket.listen(3) # Can listen until 3 connections
        client_socket, client_addr = server_socket.accept()
        print("[+] Connected with {0}:{1}".format(str(client_addr[0]), str(client_addr[1]))) 
        client_socket.send(str.encode(str(idmax))) # Send the highest id to the client
        request_client = client_socket.recv(1).decode() # receive 1 or 2, 1 if some log will be pushed by the client, 2 means that there isn't any event to push

        if request_client == "1":
            logfilenumber = len(glob.glob("log*.log"))
            logfile = "log{0}.log".format(str(logfilenumber+1))
            print("[+] Writing new log file : {0}".format(logfile))
            with open(logfile, 'a') as file: # append because the buffer size is only 4096
                while receive_state == True:
                    bytes_read = client_socket.recv(BUFFER_SIZE).decode()
                    if not bytes_read:
                        receive_state = False
                        break
                    file.write(str(bytes_read))
                    
            # get the idmax of the new imported event and write it in the evendid text file
            idmax = UpdateEventID(logfile)
        elif request_client == "2":
            print("[-] No new event to write")
        
        else:
            print("[!] Error...")
       # client_socket.close()

if __name__ == '__main__':
    main()
