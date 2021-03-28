from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

try:
    import thread
except ImportError:
    import _thread as thread

gNano = None
gServer = None

# import json
# import os
# import sys

PORT = 8500
gClients = []


class WebRelayServer(WebSocket):

    def handleMessage(self):

        global gNano

        message = self.data

        if "UP_START" == message:

            gNano.velocitySet(100)

        elif "DOWN_START" == message:

            gNano.velocitySet(-100)

        else:

            gNano.messageSend(message)


    def handleConnected(self):

        self.messageWrite(self.address[0] + ' connected')

        # if disconnection hasn't been recognized or hasn't happened yet, then we need to check client exists and remove
        ipAddress = self.address[0]

        for client in gClients:

            if client.address[0] == ipAddress:
                print('Client already exists - removing old entry')
                gClients.remove(client)

        gClients.append(self)

        # self.sendMessage("Hello client")

        self.clientsPrint()

        # for client in gClients:
        #
        #     client.sendMessage("A new client has joined")


    def handleClose(self):

        print(self.address, 'closed')

        gClients.remove(self)

        # Looks dodgy
        # self.clientsPrint()

    def clientsPrint(self):

        self.messageWrite(str(len(gClients)) + ' clients')

    def messageWrite(self, pMessage):

        print("Web Relay: " + pMessage)

    # self.messageWrite('Sending Data')
    # self.sendMessage('Client list')


gServer = SimpleWebSocketServer('', PORT, WebRelayServer)


def init(pNano):

    global gNano

    gNano = pNano


def run(*args):

    global gServer

    print("Starting socket server")

    gServer.serveforever()


def start():

    thread.start_new_thread(run, ())


def allClientsSendMessage(pMessage):

    for client in gClients:

        client.sendMessage(pMessage)