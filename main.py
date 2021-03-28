# import servocontrol
import time
import nano
import socketServer
# import motherboard_serial


def init():

    nano.init()

    socketServer.init(nano)

    socketServer.start()

    while 1:

        line = nano.nextMessageGet()

        if line:

            socketServer.allClientsSendMessage(line)

        # time.sleep(10)
        # print('Hello?')


while True:

    try:

        init()

    except:

        print("* Fail - Restarting *")
