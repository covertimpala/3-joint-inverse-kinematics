import math
try:
    from colorama import Fore
    nocolor = 0
except Exception:
    nocolor = 1

r1 = 15 #Length of segment 1 of the arm (between joints a and b (1 and 2))
r2 = 7.9 #Length of segment 2 of the arm (between joints b and c (2 and 3))
r3 = 14.5 #Length of segment 3 of the arm (between joints c (3) and end effector)
#x_dist = 18
#y_dist = 20
step = 2 #359*step|| used to determine the number of points to check
bypass = 4 #switch to  a value >= 4 to bypass filter
_range = [-90, 90] #angle ranges (anything outside the range is filtered out (as long as bypass = 1))
#Degorrad = "deg" # choose between "deg" or "rad" (degrees or radians for output)

def loc_of_J3():
    #J3_y = r1*math.cos(an_a)+r2*math.cos(an_b)
    #J3_x = r1*math.sin(an_a)+r2*math.sin(an_b)
    #ef_y = J3_x+r3*math.cos(an_c)
    #ef_x = J3_y+r3*math.sin(an_c)
    #lcx = -r3*math.sin(an_c)
    #lcy = r3*math.cos(an_c)
    print(r3*math.cos(an_c)/r3, r3*math.sin(an_c)/r3)
    x_x = math.acos(-math.sin(an_c))
    x_y = math.asin(math.cos(an_c))
    print(x_x, ":", r1*math.cos(x_x), x_y)
    if x_x == x_y:
        return(x_x)
    else:
        return("no solution")


def calculateab(locx, locy, o, r1, r2, r3, _range, bypass, x_dist, y_dist):
    b = math.pi - math.acos((-locx**2 - locy**2 + r1**2 + r2**2) / (2*r1*r2))#(r1**2+r2**2)            (2*r1*r2)
    #print("b:", b)
    bt = math.degrees(b)
    if bt >= _range[0]*bypass and bt <=_range[1]*bypass:
        a = math.atan(locx/locy)-math.atan((r2*math.sin(b))/(r1+(r2*math.cos(b))))
        #print("a:", a)
        at = math.degrees(a)
        if at >= _range[0]*bypass and at <=_range[1]*bypass:
            ys = (((locy-r1*math.cos(a))/(locx-r1*math.sin(a)))*(x_dist-r1*math.sin(a))+r1*math.cos(a)) #equation of the line from r2
            ds = math.sqrt((x_dist-locx)**2 + (ys-locy)**2) #side 1
            ds3 = abs(ys-y_dist) #side 3
            c = math.degrees(math.acos((ds**2+r3**2-ds3**2)/(2*ds*r3))) #Cosine rule
            if x_dist < locx:
                cp = c-180
                if cp >= _range[0]*bypass and cp <= _range[1]*bypass:
                    if nocolor == 0:
                        print(Fore.RED + "Additional", o) #Uncertain has been updated to "Additional"
                        print(Fore.RESET + "",at,bt,c, "or", cp)
                    else:
                        print("Additional", o)
                        print(at,bt,cp)
            elif c >= _range[0] and c <=_range[1]:
                if nocolor == 0:
                    print(Fore.GREEN + "Point on circle (angle degrees):", o, "location:", locx, locy)
                    print(Fore.RESET + "Degrees:",at,bt,c)
                else:
                    print("Point on circle (angle degrees):", o, "location:", locx, locy)
                    print("Degrees:",at,bt,c)
    else:
        print(Fore.RED + "angle out of range" + Fore.RESET)
        #print()

def choosepos(segment1, segment2, segment3, x_dist, y_dist, step, _range, bypass):
    #angle = random.randrange(0,359,1)
    #for i in range(359*step):
    x_p = x_dist+offstx#x_p = r3*math.cos(math.radians(i/step))
    y_p = y_dist+offsty#y_p = r3*math.sin(math.radians(i/step))
    joint3loc = [x_p, y_p]
    #print(joint3loc)
    #print(joint3loc)
    try:
        calculateab(joint3loc[0], joint3loc[1],"", segment1, segment2, segment3, _range, bypass, x_dist, y_dist)
    except Exception as f:
        print("failed:", f)
        #print(Fore.RED + "OUT OF RANGE", i/step, joint3loc[0], joint3loc[1])
        #continue

an_a = math.radians(30)
an_b = math.radians(50)
an_c = math.radians(50)
destination = [18,20]
currpos = [r1*math.sin(an_a)+r2*math.sin(an_a+an_b)+r3*math.sin(an_a+an_b+an_c),r1*math.cos(an_a)+r2*math.cos(an_a+an_b)+r3*math.cos(an_a+an_b+an_c)]
#print(currpos)
steps = 200
#angc = 50
path = [destination[0] - currpos[0], destination[1] - currpos[1]]
print(path)
offstx = -r3*math.sin(an_a+an_b+an_c) #currpos[0]-r3*math.sin(an_c)
offsty = -r3*math.cos(an_a+an_b+an_c) #currpos[1]-r3*math.cos(an_c)
print(offstx, offsty)
#print(offstx, offsty)
#thetax = round(math.asin(offstx/r3),5)
#thetay = round(math.acos(offsty/r3),5)
#print(thetax, thetay)
#if abs(thetax) == abs(thetay):
#    sol = abs(thetax)
#else:
#    print("Something went wrong")

for x in range(steps):
    xstep = path[0]/steps
    ystep = path[1]/steps
    currpos[0] = currpos[0]+xstep
    currpos[1] = currpos[1]+ystep
    #print(currpos)
    choosepos(r1, r2, r3, currpos[0], currpos[1], step, _range, bypass)

choosepos(r1, r2, r3, destination[0], destination[1], step, _range, bypass)