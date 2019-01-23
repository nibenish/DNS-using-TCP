Nicholas Benish
4739200 benis012@umn.edu

My project runs on Python3, the server must be started before the client, with
the command:
> python3 DNSServer.py
and the client started with the command:
> python3 DNSClient.py

The server will look at DNS_mapping.txt for previous mappings and save its new
mappings to the same file. This file can be changed by altering the "cacheFile"
variable in DNSServer.py (line 55). The server will first scan through the lines
of the cacheFile and search for the client's input (e.g. "facebook.com", 
"www.google.com", "umn.edu"). If the input is found it will pass the entire
from the cacheFile on to dnsSelection, to pick one of the possibly many IP
addresses from that line. It then does some formatting before sending the
encoded response back to the client.

If the hostname queried by the client is not found in the cacheFile, the function
"gethostbyname" is called on the client's input. This response is cached into the
cacheFile, and then formatted into the style "Root DNS:<hostname>:<IP_ADDRESS>"
before sent to the client in its encoded form. If the gethostbyname function
does not return an IP address, the server will not write anything to the cacheFile,
and will indicate failure to the client by writing an encoded "Hostname not found"
message to the client socket.

Finally, the connection socket to the client is closed, and the server thread,
having completed its execution, is killed.
