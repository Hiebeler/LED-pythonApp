import board
import neopixel
import socket
import multiprocessing
import random
import math
import datetime
import RPi.GPIO as GPIO
from time import sleep
print("Wait for 40 seconds")
#sleep(40)
print("ready")


HOST = '192.168.1.77'  # Standard loopback interface address (localhost)
PORT = 1234        # Port to listen on (non-privileged ports are > 1023)

ledAnzahl = 113

boolwecker = False

button_einschalten = True

pixels = neopixel.NeoPixel(board.D18,ledAnzahl,brightness = 1.0)

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def buttonClick(channel):
	global button_einschalten
	if button_einschalten:
		pixels.fill((100,255,0))
	else:
		pixels.fill(0)
	button_einschalten = not button_einschalten


GPIO.add_event_detect(17, GPIO.RISING, callback=buttonClick, bouncetime=300)

def dimmen(dim):
        dim = float(dim[10:14])
        pixels.brightness = dim


def color(colors):
        hex = int(colors[0:8],0)
        pixels.fill((hex))

def weckersetup():

        print("wecker")

        hour = int(wecktime[0:2])
        min = int(wecktime[3:5])
        day = int(wecktime[5:6])

        time = datetime.datetime.now()
        y = time.replace(hour = hour, minute = min, second =0, microsecond = 0)
        y = y.strftime("%H:%M")

        while True:
                if y <= datetime.datetime.now().strftime("%H:%M") and day == datetime.date.today().weekday():
                        wecker()
                        break

def wecker():
        print("wecker abgegangen")

        for _ in range(10):
                pixels.fill((255,0,0))
                sleep(1)
                pixels.fill(0)
                sleep(1)

        for _ in range(10):
                pixels.fill((255,0,0))
                sleep(0.2)
                pixels.fill(0)
                sleep(0.2)

        for _ in range(10):
                pixels.fill((0,255,0))
                sleep(0.2)
                pixels.fill(0)
                sleep(0.2)

        for _ in range(10):
                pixels.fill((0,0,255))
                sleep(0.2)
                pixels.fill(0)
                sleep(0.2)

        for _ in range(10):
                pixels.fill((255,255,255))
                sleep(0.1)
                pixels.fill(0)
                sleep(0.1)

        pixels.fill((100,255,0))




def fadeEasy():
        print("fadeEasy")
        while True:
                for y in range(3):
                        for x in range(256):
                                if y == 0:
                                        pixels.fill((x,0,0))
                                elif y == 1:
                                        pixels.fill((0,x,0))
                                else:
                                        pixels.fill((0,0,x))
                                sleep(0.01)
                        for x in range(255,-1,-1):
                                if y == 0:
                                        pixels.fill((x,0,0))
                                elif y == 1:
                                        pixels.fill((0,x,0))
                                else:
                                        pixels.fill((0,0,x))
                                sleep(0.01)


def fade():
        print("fade")
        while True:
                for y in range(3):
                        up = 0
                        down = 255
                        for _ in range(256):
                                if y == 0:
                                        pixels.fill((up,down,0))
                                elif y == 1:
                                        pixels.fill((down,0,up))
                                else:
                                        pixels.fill((0,up,down))
                                up += 1
                                down -= 1
                                sleep(0.1)


def fadesnake():
        print("regenbogenfade")
        pixels.auto_write = False
        schritt = math.floor(255/(ledAnzahl/3)*10)/10
        pixel = 0
        while True:
                up = 0
                down = 255
                for i in range(ledAnzahl):
                        if i < ledAnzahl/3:
                                if 1 == i:
                                        pixels[pixel] = ((255,5,1))
                                else:
                                        pixels[pixel] = ((down,up,0))
                                down -= schritt
                                up += schritt
                                pixel += 1
                                if pixel == ledAnzahl - 1:
                                        pixel = 0
                        elif i < ledAnzahl/1.5:
                                pixels[pixel] = ((0,up,down))
                                down += schritt
                                up -= schritt
                                pixel += 1
                                if pixel == ledAnzahl - 1:
                                        pixel = 0
                        else:
                                if ledAnzahl-1 == i:
                                        pixels[pixel] = ((253,0,2))
                                elif ledAnzahl-2 == i:
                                        pixels[pixel] = ((248,0,7))
                                else:
                                        pixels[pixel] = ((up,0,down))
                                down -= schritt
                                up += schritt
                                pixel += 1
                                if pixel == ledAnzahl-1:
                                        pixel = 0
                pixels.show()
                sleep(0.2)


def colorsnake():
        print("regenbogen")
        pixels.auto_write = False
        schritt = math.floor(255/(ledAnzahl/3)*10)/10
        up = 0
        down = 255
        for i in range(ledAnzahl):
                        if i < ledAnzahl/3:
                                pixels[i] = ((down,up,0))
                                down -= schritt
                                up += schritt
                        elif i < ledAnzahl/1.5:
                                pixels[i] = ((0,up,down))
                                down += schritt
                                up -= schritt
                        else:
                                pixels[i] = ((up,0,down))
                                down -= schritt
                                up += schritt
        pixels.show()

def sparkle():
        print("sparkle")
        while True:

                r = int(coloranimation[0:2],16)//3
                g = int(coloranimation[2:4],16)//3
                b = int(coloranimation[4:6],16)//3


                speedDelay = random.uniform(0.1,1)
                pixels.fill((r,g,b))

                intsparkle = random.randint(1,(ledAnzahl-1))
                pixels[intsparkle] = (((r*3), (g*3), (b*3)))
                sleep(0.02)
                pixels[intsparkle] = ((r,g,b))
                sleep(speedDelay)


def runningLights():
        print("runningLights")
        pixels.fill(0)
        while True:
                hex = int(coloranimation,0)
                for i in range(ledAnzahl):
                        pixels[i] = ((hex))
                        sleep(0.01)

                for i in range(ledAnzahl-1,-1, -1):
                        pixels[i] = (0)
                        sleep(0.01)



def snow():
        print("snow")
        pixels.auto_write = False
        a = 0
        while True:

                pixels.fill = 0
                pixels.show()
                for i in range(ledAnzahl):
                        if a == 0:
                                pixels[i] = 0
                        elif a == 1:
                                pixels[i] = ((0,1,0))
                        elif a == 2:
                                pixels[i] = ((20,30,0))
                        elif a == 3:
                                pixels[i] = ((80,20,0))
                        elif a == 4:
                                pixels[i] = ((255,0,0))
                        elif a == 5:
                                pixels[i] = ((70,0,30))
                        elif a == 6:
                                pixels[i] = ((20,0,30))
                        else:
                                pixels[i] = ((0,0,1))
                                a = -1
                        a += 1

                sleep(0.01)
                pixels.show()

def randomcolors():
        print("random")
        pixels.auto_write = False
        for i in range(ledAnzahl):
                pixels[i] = (random.randint(0, 255), random.randint(0, 255), 0)
        pixels.show()


def test():
        while True:
                a = 112
                for i in range(ledAnzahl):
                        pixels.fill(0)
                        pixels[i] = ((255,0,0))
                        pixels[a] = ((255,0,0))
                        a -= 1
                        sleep(0.01)


def blitzen():
        print("blitzen")
        while True:
                if coloranimation == True:
                        pixels.fill(0)
                        for _ in range(20):
                                pixels[random.randint(1, ledAnzahl)-1] = ((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                else:
                        r = int(coloranimation[0:2],16)
                        g = int(coloranimation[2:4],16)
                        b = int(coloranimation[4:6],16)

                        pixels.fill(0)
                        for _ in range(20):
                                pixels[random.randint(1, ledAnzahl)-1] = ((r, g, b))



def differentcolors():
        print("different Colors")
        print(coloranimation)

        start = 2
        end = 10

        colorlist = []

        for i in range(int(len(coloranimation)/10)):
                colorlist.append(int(coloranimation[start:end],0))
                start += 10
                end += 10


        pixels.auto_write = False
        a = 0
        for i in range(ledAnzahl):
                pixels[i] = colorlist[a]
                if len(colorlist)-1 == a:
                        a = 0
                else:
                        a += 1
        pixels.show()



#Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

def socket():
        global coloranimation
        global wecktime
        message = ""
        boolanimation = [False,False,False, False, False, False, False, False, False, False]
        panimation = [multiprocessing.Process(target=colorsnake), multiprocessing.Process(target=fade), multiprocessing.Process(target=fadeEasy), multiprocessing.Process(target=sparkle), multiprocessing.Process(target=runningLights), multiprocessing.Process(target=snow), multiprocessing.Process(target=randomcolors), multiprocessing.Process(target=blitzen), multiprocessing.Process(target=fadesnake),multiprocessing.Process(target=differentcolors) ]
        functions = [colorsnake, fade, fadeEasy, sparkle, runningLights, snow, randomcolors, blitzen, fadesnake, differentcolors]
        boolwecker = False

        lastsnake = ""
        while True:
                conn, addr = s.accept()

                while True:
                        message  = conn.recv(1024)
                        data  = conn.recv(1024)
                        message = message.decode("utf-8")
                        if not message:
                                break


                        if message[0:2] == "10":

                                for i in range(len(panimation)):
                                        if boolanimation[i] == True:
                                                panimation[i].terminate()
                                                panimation[i] = multiprocessing.Process(target=functions[i])
                                                boolanimation[i] = False

                                if boolanimation[2] == False:
                                        panimation[2].start()

                                boolanimation[2] = True


                        elif message[0:2] == "11":
                                for i in range(len(panimation)):
                                        if boolanimation[i] == True:
                                                panimation[i].terminate()
                                                panimation[i] = multiprocessing.Process(target=functions[i])
                                                boolanimation[i] = False

                                if boolanimation[1] == False:
                                        panimation[1].start()

                                boolanimation[1] = True


                        elif message[0:2] == "12":
                                for i in range(len(panimation)):
                                        if boolanimation[i] == True:
                                                panimation[i].terminate()
                                                panimation[i] = multiprocessing.Process(target=functions[i])
                                                boolanimation[i] = False


                                coloranimation = message[4:10]

                                if boolanimation[0] == False:
                                        panimation[0].start()

                                boolanimation[0] = True



                        elif message[0:2] == "13":
                                for i in range(len(panimation)):
                                        if boolanimation[i] == True:
                                                panimation[i].terminate()
                                                panimation[i] = multiprocessing.Process(target=functions[i])
                                                boolanimation[i] = False


                                coloranimation = message[4:10]

                                if boolanimation[3] == False:
                                        panimation[3].start()

                                boolanimation[3] = True


                        elif message[0:2] == "14":
                                for i in range(len(panimation)):
                                        if boolanimation[i] == True:
                                                panimation[i].terminate()
                                                panimation[i] = multiprocessing.Process(target=functions[i])
                                                boolanimation[i] = False


                                coloranimation = message[2:10]

                                if boolanimation[4] == False:
                                        panimation[4].start()

                                boolanimation[4] = True


                        elif message[0:2] == "15":
                                for i in range(len(panimation)):
                                        if boolanimation[i] == True:
                                                panimation[i].terminate()
                                                panimation[i] = multiprocessing.Process(target=functions[i])
                                                boolanimation[i] = False

                                if boolanimation[5] == False:
                                        panimation[5].start()

                                boolanimation[5] = True


                        elif message[0:2] == "16":
                                for i in range(len(panimation)):
                                        if boolanimation[i] == True:
                                                panimation[i].terminate()
                                                panimation[i] = multiprocessing.Process(target=functions[i])
                                                boolanimation[i] = False

                                if boolanimation[6] == False:
                                        panimation[6].start()

                                boolanimation[6] = True

                        elif message[0:2] == "17":
                                for i in range(len(panimation)):
                                        if boolanimation[i] == True:
                                                panimation[i].terminate()
                                                panimation[i] = multiprocessing.Process(target=functions[i])
                                                boolanimation[i] = False

                                print(message)

                                if message[2:3] == "9":
                                        coloranimation = True
                                else:
                                        coloranimation = message[4:10]

                                if boolanimation[7] == False:
                                        panimation[7].start()

                                boolanimation[7] = True


                        elif message[0:2] == "18":
                                for i in range(len(panimation)):
                                        if boolanimation[i] == True:
                                                panimation[i].terminate()
                                                panimation[i] = multiprocessing.Process(target=functions[i])
                                                boolanimation[i] = False

                                coloranimation = message[4:10]

                                if boolanimation[8] == False:
                                        panimation[8].start()

                                boolanimation[8] = True

                        elif message[0:2] == "19":

                                for i in range(len(panimation)):
                                        if boolanimation[i] == True:
                                                panimation[i].terminate()
                                                panimation[i] = multiprocessing.Process(target=functions[i])
                                                boolanimation[i] = False

                                coloranimation = message[2:]
                                coloranimation = coloranimation[:-10]

                                if boolanimation[9] == False:
                                        panimation[9].start()

                                boolanimation[9] = True


                        if message[11:12] == ".":
                                dimmen(message)


                        if message[0:2] == "00":

                                for i in range(len(panimation)):
                                        if boolanimation[i] == True:
                                                panimation[i].terminate()
                                                panimation[i] = multiprocessing.Process(target=functions[i])
                                                boolanimation[i] = False


                                color(message[2:])

                        if message[0:1] == "2":
                                print(message)
                                wecktime = message[1:7]
                                weckerpro = multiprocessing.Process(target=weckersetup)
                                weckerpro.start()
                                boolwecker = True


	
p1 = multiprocessing.Process(target=socket)
p1.start()
