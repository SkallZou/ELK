def getEvent(self):
                BUFFER_SIZE = 4096
                print("Get Events")
                srvAddr = # [ELK_SERVER_IP]
                port = # [ELK_SERVER_PORT]
                client_socket = socket.socket()
                print(f"[+] Connecting to {srvAddr}:{port}")
                client_socket.connect((srvAddr, port))
                print("Requesting highest ID")
                idmax = client_socket.recv(1024).decode() # Receiving highest ID from the server
                print(f"IDMAX: {idmax}")
                query = "id:>{0}".format(idmax)
                now = datetime.now()
                current_time = now.strftime("%d%m%y")
                data = {"module":"Endpoint_Active","offset":0,"limit":100,"timeOrder":"ASC","advFilter":query,"hotData":True,"countOnly":False,"aggregateOnGroups":False}
                headers = {"accept": "application/json","Content-Type": "application/json", "Authorization": "Bearer " + self.xdrTokens[self.XDR]}
                response = self.xdrSession.post(f'[IPAddress_to_pull the event]', headers=headers, json=data)
                if response.status_code == 200:
                        output_json = json.dumps(response.json())

                        if len(response.json()['eventData']) > 0:
                                print("Sending log to server")
                                client_socket.send(str.encode("1")) # Log to be sent to server
                                filename = "log_{0}.log".format(current_time)
                                with open(filename, 'w', encoding='utf-8') as file:
                                        file.write(output_json)
                                        file.write("\n")

                                print(f"Sending the file {filename}")
                                with open(filename, "rb") as file:
                                        while True:
                                                # read the bytes from the file
                                                bytes_read = file.read(BUFFER_SIZE)
                                                if not bytes_read:
                                                        break
                                                client_socket.sendall(bytes_read)
                        else:
                                print("No event to send to the server")
                                client_socket.send(str.encode("2"))
                                print("No new event to push")
                else:
                        print(response.status_code)
                        print("error")
