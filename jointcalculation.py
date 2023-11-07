import math
import random
from colorama import Fore

r1 = 5
r2 = 5
r3 = 5
x_dist = 6
y_dist = 4
step = 2 #359*step|| used to determine the number of points to check

def calculateab(locx, locy, o):
    b = math.acos((locx**2 + locy**2 - r1**2 - r2**2) / (2*r1*r2))#(r1**2+r2**2)
    bt = math.degrees(b)
    if bt >= -90 and bt <=90:
        a = math.atan(locx/locy)-math.atan((r2*math.sin(b))/(r1+(r2*math.cos(b))))
        at = math.degrees(a)
        if at >= -90 and at <=90:
            c_test = math.degrees(math.asin(locy/r3))
            ys = (((locy-r1*math.cos(a))/(locx-r1*math.sin(a)))*(x_dist-r1*math.sin(a))+r1*math.cos(a)) #equation of the line from r2
            ds = math.sqrt((x_dist-locx)**2 + (ys-locy)**2) #side 1
            ds3 = abs(ys-y_dist) #side 3
            c = math.degrees(math.acos((ds**2+r3**2-ds3**2)/(2*ds*r3))) #Cosine rule
            #if x_dist < locx:
             #   cp = 180-c
              #  print(o, "Uncertain", x_dist,locx)
               # print(at,bt,c, "or", cp)
            #if c >= -90 and c <=90:
            print(Fore.GREEN + "Point on circle (angle degrees):", o)
            print(Fore.RESET + "Degrees:",at,bt,c, "Radians:", a, b, c)

def choosepos():
    #angle = random.randrange(0,359,1)
    for i in range(359*step):
        x_p = r3*math.cos(math.radians(i/step))#r3*math.cos(math.radians(i))
        y_p = r3*math.sin(math.radians(i/step))#r3*math.sin(math.radians(i))
        joint3loc = [x_dist+x_p, y_dist+y_p]
        #print(joint3loc)
        try:
            calculateab(joint3loc[0], joint3loc[1],i/step)
        except Exception:
            continue
            #print("OUT OF RANGE")
choosepos()