# Spring 2018 CSci4211: Introduction to Computer Networks
# This program serves as the server of DNS query.
# Written in Python v3.

import sys, threading, os, random
from socket import *

def main():
	host = "localhost" # Hostname. It can be changed to anything you desire.
	serverPort = 5001 # Port number.

	serverPort = 5001

	#create a socket object, SOCK_STREAM for TCP
	serverSocket = socket(AF_INET,SOCK_STREAM)

	#bind socket to the current address on port 5001
	serverSocket.bind(('',serverPort))

	#Listen on the given socket maximum number of connections queued is 20
	serverSocket.listen(20)

	monitor = threading.Thread(target=monitorQuit, args=[])
	monitor.start()

	print("Server is listening...")

	while 1:
		#blocked until a remote machine connects to the local port 5001
		connectionSock, addr = serverSocket.accept()
		print(addr)
		server = threading.Thread(target=dnsQuery, args=[connectionSock, addr[0]])
		server.start()

# my shit, copied from slide
#	print 'The server is ready to receive'

#	while True:

#		connectionSocket, addr = serverSocket.accept()

#		sentence = connectionSocket.recv(1024).decode()

#		capitalizedSentence = sentence.upper()

#		connectionSocket.send(capitalizedSentence.encode())

#		connectionSocket.close()
# end my shit

def dnsQuery(connectionSock, srcAddress):

	dnsAnswers = ""
	found = False
	cacheFile = "DNS_mapping.txt"
	sentence = connectionSock.recv(1024).decode()
	#check the DNS_mapping.txt to see if the host name exists
	#set local file cache to predetermined file.
	try:
		dataFile = open(cacheFile, "r")
        #create file if it doesn't exist
	except IOError:
		dataFile = open(cacheFile, "w")
        #if it does exist, read the file line by line to look for a
        #match with the query sent from the client
	for line in dataFile:
    #If match, use the entry in cache.
		if sentence in line:
        #However, we may get multiple IP addresses in cache, so call dnsSelection to select one.
			found = True
			print("found in dataFile")
			dnsAnswers = dnsSelection(line)

	dataFile.close()

	if (not found):
		#If no lines match, query the local machine DNS lookup to get the IP resolution
		try:
			dnsAnswers = gethostbyname(sentence)
			print("found by DNS lookup")
			#write the response in DNS_mapping.txt
			dataFile = open(cacheFile, "a")
			dataFile.write(sentence + ":" + dnsAnswers)
			dataFile.write('\n')
			dataFile.close()
		except IOError:
			print("Invalid URL")



	if (dnsAnswers == ""):
		connectionSock.send("hostname not found\n".encode())
	else:
		#print response to the terminal
		print(dnsAnswers)
		#send the response back to the client
		if (found):
			dnsAnswers = "Local DNS:" + sentence + ":" + dnsAnswers
		else:
			dnsAnswers = "Root DNS:" + sentence + ":" + dnsAnswers + '\n'

		connectionSock.send(dnsAnswers.encode())
	#Close the server socket.
	connectionSock.close()


def dnsSelection(ipList):
	#checking the number of IP addresses in the cache
	entries = ipList.split(':')
	#if there is only one IP address, return the IP address
	if (len(entries) <= 2) :
		return entries[1]
	#if there are multiple IP addresses, select one and return.
	else :
		return entries[random.randint(1,len(entries)-1)]
	##bonus project: return the IP address according to the Ping value for better performance (lower latency)

def monitorQuit():
	while 1:
		sentence = input()
		if sentence == "exit":
			os.kill(os.getpid(),9)

main()
