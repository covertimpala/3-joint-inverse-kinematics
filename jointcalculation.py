import math
try:
    from colorama import Fore
    nocolor = 0
except Exception:
    nocolor = 1

r1 = 5 #Length of segment 1 of the arm (between joints a and b (1 and 2))
r2 = 5 #Length of segment 2 of the arm (between joints b and c (2 and 3))
r3 = 5 #Length of segment 3 of the arm (between joints c (3) and end effector)
x_dist = 6
y_dist = 4
step = 2 #359*step|| used to determine the number of points to check
bypass = 1 #switch to  a value >= 4 to bypass filter
_range = [-90, 90] #angle ranges (anything outside the range is filtered out (as long as bypass = 1))
#Degorrad = "deg" # choose between "deg" or "rad" (degrees or radians for output)

def calculateab(locx, locy, o, r1, r2, r3, _range, bypass):
    b = math.acos((locx**2 + locy**2 - r1**2 - r2**2) / (r1**2+r2**2))#(r1**2+r2**2)            (2*r1*r2)
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

def choosepos(segment1, segment2, segment3, x_dist, y_dist, step, _range, bypass):
    #angle = random.randrange(0,359,1)
    for i in range(359*step):
        x_p = r3*math.cos(math.radians(i/step))#r3*math.cos(math.radians(i))
        y_p = r3*math.sin(math.radians(i/step))#r3*math.sin(math.radians(i))
        joint3loc = [x_dist+x_p, y_dist+y_p]
        #print(joint3loc)
        try:
            calculateab(joint3loc[0], joint3loc[1],i/step, segment1, segment2, segment3, _range, bypass)
        except Exception as f:
            #print(f)
            #print(Fore.RED + "OUT OF RANGE", i/step, joint3loc[0], joint3loc[1])
            continue
choosepos(r1, r2, r3, x_dist, y_dist, step, _range, bypass)