# Chat-project
Chat based on python , files transfer with releable UDP

# Main goal:
main goal of the projectIn this assignment we asked to build a communication app between
multiply clients and one server,
we tried our best to achieve our main goal: an application with basic
GUI which with it we could communicate each other with messages,
private messages file download and upload files.
While exploring this field and programming it we achieve a good
and deep understanding about all the communication world, how
binding between different clients and server work,
what is happening in the background of it etc.
We won’t lie, at first it was a little bit hard to understand how to
make all of this work as we want, but giving up was not an option,
so we sat and learned every part in this assignment not just for an A
in our final grade, we also improved our knowledge in this field.
In this assignment we implemented two main classes:
* Server
* Client including a GUI

# Explanation about the Server class:
This class is the main class in our project, everything which send
from any client is going through the server, and the server provide
any action we would like to do.
Our main host IP is 127.0.0.1 and the port we work on is 50,000 as
we asked for.
All the communication work via TCP connection, messages, private
messages, online members etc.
In aim to transfer files we created another socket which work via
UDP connection.

# File transfer explanation:
When we got a request from the client to download file from our file
list, the server started to split the file into 2048 bytes which
represent one packet, in aim to solve this problem we use timer, if
in the given time the client didn’t send me an “ack” the server will
send the packet over and over again, the client always check if the
specific packet is in it data structure, if it isn’t we append it to our
data structure and send ack to the server, the methos we use in is
“Stop and Wait”, for every packet we send we wait to ack response,
didn’t got it? Send again and again, in this way we ensure that all
the packet will arrive to the wanted destination.

![gokuuuu](https://user-images.githubusercontent.com/92504985/164762978-69be2571-bf56-470c-a7d3-daee59c88c9e.png) 

# The handle function
The main goal of this function is to handle with all the requests
which we get from the client class.
We are handling with commend such as:
* Send message
* Send private message
* Show online members
* Show files
* Download files
* Client disconnect

# Client functions and GUI:

* `Login` - To login the server with given nickname.
* `Show Online` - Show list of the connected online members in the chat.
* `Send` - Sending the message that the client wrote.
* `Send Private` - Sending private message to the given online member.
* `Download` - Downloading file from the server by name.
* `Show Files` - Shows the all the file that exists in the server.
* `Disconnect` - Disconnecting from the server.

# How to use :
* Clone this ripository

Windows:
* Double click on the `server.py`
* Double click on the `client.py` (You can do it multiple times)
* Start to chat.

Linux:
* Open terminal on the dictionary
* Use the command `python3 server.py` to start the server
* Use the command `python3 client.py` to open a gui and connect as a client (You can do it multiple times)
* Start to chat

# Gui :

![guiiii](https://user-images.githubusercontent.com/92504985/164764017-d70bda01-b9a3-451f-9795-e4585169fbb9.PNG)


