import math
try:
    from colorama import Fore
    nocolor = 0
except Exception:
    nocolor = 1

r1 = 15 #Length of segment 1 of the arm (between joints a and b (1 and 2))
r2 = 7.9 #Length of segment 2 of the arm (between joints b and c (2 and 3))
r3 = 14.5 #Length of segment 3 of the arm (between joints c (3) and end effector)
x_dist = 18
y_dist = 20
step = 2 #359*step|| used to determine the number of points to check
bypass = 4 #switch to  a value >= 4 to bypass filter
_range = [-90, 90, -90, 90, -90, 90] #angle ranges (anything outside the range is filtered out (as long as bypass = 1)) (a,a,b,b,c,c)
#Degorrad = "deg" # choose between "deg" or "rad" (degrees or radians for output)

#def loc_of_J3():
 #   print(r3*math.cos(an_c)/r3, r3*math.sin(an_c)/r3)
  #  x_x = math.acos(-math.sin(an_c))
   # x_y = math.asin(math.cos(an_c))
    #print(x_x, ":", r1*math.cos(x_x), x_y)
    #if x_x == x_y:
     #   return(x_x)
    #else:
    #    return("no solution")


def calculateab(locx, locy, o, r1, r2, r3, _range, bypass, x_dist, y_dist):
    #print((-locx**2 - locy**2 + r1**2 + r2**2) / (2*r1*r2))
    b = math.pi - math.acos((-locx**2 - locy**2 + r1**2 + r2**2) / (2*r1*r2))#(r1**2+r2**2)            (2*r1*r2)
    #print("b:", b)
    bt = math.degrees(b)
    if bt >= _range[2]*bypass and bt <=_range[3]*bypass:
        a = -math.asin((r2*math.sin(b))/(math.sqrt(locx**2 + locy**2)))+math.asin((locx)/(math.sqrt(locx**2 + locy**2)))
        #print("a:", a)
        at = math.degrees(a)
        if at >= _range[0]*bypass and at <=_range[1]*bypass:
            ys = (((locy-r1*math.cos(a))/(locx-r1*math.sin(a)))*(x_dist-r1*math.sin(a))+r1*math.cos(a)) #equation of the line from r2
            ds = math.sqrt((x_dist-locx)**2 + (ys-locy)**2) #side 1
            ds3 = abs(ys-y_dist) #side 3
            c = math.degrees(math.acos((ds**2+r3**2-ds3**2)/(2*ds*r3))) #Cosine rule
            if x_dist < locx:
                cp = c-180
                if cp >= _range[4]*bypass and cp <= _range[5]*bypass:
                    if nocolor == 0:
                        print(Fore.RED + "Additional", o) #Uncertain has been updated to "Additional"
                        print(Fore.RESET + "",at,bt,c, "or", cp)
                        return [at, bt, c, "a"]
                    else:
                        print("Additional", o)
                        print(at,bt,cp)
                        return [at, bt, c, "a"]
                else:
                    #print(Fore.RED + "angle out of range" + Fore.RESET)
                    return ("out of range")
            elif c >= _range[4] and c <=_range[5]:
                if nocolor == 0:
                    print(Fore.GREEN + "Point on circle (angle degrees):", o, "location:", locx, locy)
                    print(Fore.RESET + "Degrees:",at,bt,c)
                    return [at, bt, c, ""]
                else:
                    print("Point on circle (angle degrees):", o, "location:", locx, locy)
                    print("Degrees:",at,bt,c)
                    return [at, bt, c, ""]
        else:
            #print(Fore.RED + "angle out of range" + Fore.RESET)
            return ("out of range")
    else:
        #print(Fore.RED + "angle out of range" + Fore.RESET)
        #print()
        return ("out of range")

def choosepos(segment1, segment2, segment3, x_dist, y_dist, step, _range, bypass, offstx_, offsty_, simpl, z):
    if simpl == False:
        x_p = offstx_
        y_p = offsty_
    else:
        x_p = r3*math.cos(math.radians(z/step))#r3*math.cos(math.radians(i))
        y_p = r3*math.sin(math.radians(z/step))#r3*math.sin(math.radians(i))
    joint3loc = [x_dist+x_p, y_dist+y_p]
    #print("-==-", joint3loc[0], joint3loc[1],"", segment1, segment2, segment3, _range, bypass, x_dist, y_dist)
    try:
        return(calculateab(joint3loc[0], joint3loc[1],"", segment1, segment2, segment3, _range, bypass, x_dist, y_dist))
    except Exception as f:
        #print("failed:", f)
        #print(Fore.RED + "OUT OF RANGE", i/step, joint3loc[0], joint3loc[1])
        #continue
        return(None)

an_a = math.radians(30)
an_b = math.radians(50)
an_c = math.radians(50)
destination = [18,20]
currpos = [r1*math.sin(an_a)+r2*math.sin(an_a+an_b)+r3*math.sin(an_a+an_b+an_c),r1*math.cos(an_a)+r2*math.cos(an_a+an_b)+r3*math.cos(an_a+an_b+an_c)]
steps = 200
path = [destination[0] - currpos[0], destination[1] - currpos[1]]
print(path)
offstx = -r3*math.sin(an_a+an_b+an_c) #currpos[0]-r3*math.sin(an_c)
offsty = -r3*math.cos(an_a+an_b+an_c) #currpos[1]-r3*math.cos(an_c)
print(offstx, offsty)

abcang = choosepos(r1, r2, r3, destination[0], destination[1], step, _range, bypass, offstx, offsty, False, 1)
#        choosepos(r1, r2, r3, destination[0], destination[1], step, _range, bypass)
print(abcang)
if abcang != "out of range" and abcang != None:
    dan_a = math.degrees(an_a)
    dan_b = math.degrees(an_b)
    dan_c = math.degrees(an_c)
    a_mstp = (abcang[0] - dan_a)/steps
    b_mstp = (abcang[1] - dan_b)/steps
    c_mstp = (abcang[2] - dan_c)/steps
    for i in range(steps-1):
        #if i != 0:
        dan_a = dan_a + a_mstp
        dan_b = dan_b + b_mstp
        dan_c = dan_c + c_mstp
        print(dan_a, dan_b, dan_c)
else:
    print(Fore.CYAN + "Check for closest match? (y/n)")
    print("(this will shift the locked segment)")
    an_s = input()
    if an_s == "y" or an_s == "yes":
        print(Fore.GREEN + "finding closest match" + Fore.RESET)
        #print(chsp(r1, r2, r3, x_dist, y_dist, step, _range, bypass, ))
        liovar = {}
        for z in range(359*step):
            va = choosepos(r1, r2, r3, destination[0], destination[1], step, _range, bypass, offstx, offsty, True, z)
            if va != "out of range" and va != None:
# <<===========================>>   <<===========================>>   <<===========================>>   <<===========================>>
                liovar[len(liovar)] = z,va # <<===========================>>   <<===========================>>   <<===========================>>
# <<===========================>>   <<===========================>>   <<===========================>>   <<===========================>>
#                 change liovar z to angle on circle
# <<===========================>>   <<===========================>>   <<===========================>>   <<===========================>>
        print(liovar)
        #print(liovar[1][0])
        cv = -5
        thetax = round(math.asin(offstx/r3),5)
        thetay = round(math.acos(offsty/r3),5)
        print(thetax, thetay)
        if abs(thetax) == abs(thetay):
            sol = math.degrees(abs(thetax))
        else:
            print("Something went wrong")
        global ck_
        global ck
        ck = 0
        
        for p in range(len(liovar)):
            #print(p)
            
            ck_ = liovar[p][0]/sol
            if abs(ck_) < abs(cv):
                cv = ck_
                ck = liovar[p][0]
        print(sol)
        print(ck)
        print(ck_)
