#from colorama import Fore
import math
import time
try:
    from colorama import Fore
    nocolor = 0
except Exception:
    nocolor = 1

r1 = 15
r2 = 7.9
r3 = 14.5
step = 2
run = 0
lock = 0
speed = 0
bypass = 1
_range = [-90, 90, -90, 90, -90, 90]


def spdcntrl(selserv, stp, an): #servo, step, angle
    curran = round(int(kit.servo[selserv].angle))
    an_n = (an-curran)/stp
    for z in range(stp):
        if z != 0:
            #print(z, z*an/stp)
            kit.servo[selserv].angle = curran+z*an_n
            time.sleep(0.01)

#========================================================================================================================#
################################################### Inverse Kinematics ###################################################
#========================================================================================================================#

def calculateab(locx, locy, o, r1, r2, r3, _range, bypass, x_dist, y_dist):
    b = math.pi - math.acos((-locx**2 - locy**2 + r1**2 + r2**2) / (2*r1*r2))#(r1**2+r2**2)            (2*r1*r2)
    #print("b:", b)
    bt = math.degrees(b)
    if bt >= _range[2]*bypass and bt <=_range[3]*bypass:
        a = -math.asin((r2*math.sin(b))/((locx**2 + locy**2)**(1/2)))+math.asin((locx)/((locx**2 + locy**2)**(1/2)))
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
    try:
        return(calculateab(joint3loc[0], joint3loc[1],"", segment1, segment2, segment3, _range, bypass, x_dist, y_dist))
    except Exception as f:
        print("failed:", f)
        #print(Fore.RED + "OUT OF RANGE", i/step, joint3loc[0], joint3loc[1])
        #continue


an_a = math.radians(kit.servo[1].angle)
an_b = math.radians(kit.servo[2].angle)
an_c = math.radians(kit.servo[3].angle)
print(Fore.BLUE + "destination x-dist (cm)" + Fore.RESET)
d_x = int(input())
print(Fore.BLUE + "destination y-dist (cm)" + Fore.RESET)
d_y = int(input())
destination = [d_x,d_y]
currpos = [r1*math.sin(an_a)+r2*math.sin(an_a+an_b)+r3*math.sin(an_a+an_b+an_c),r1*math.cos(an_a)+r2*math.cos(an_a+an_b)+r3*math.cos(an_a+an_b+an_c)]
#steps = 200
path = [destination[0] - currpos[0], destination[1] - currpos[1]]
print(path)
offstx = -r3*math.sin(an_a+an_b+an_c) #currpos[0]-r3*math.sin(an_c)
offsty = -r3*math.cos(an_a+an_b+an_c) #currpos[1]-r3*math.cos(an_c)
print(offstx, offsty)

abcang = choosepos(r1, r2, r3, destination[0], destination[1], step, _range, bypass, offstx, offsty, False, 1)
print(abcang)
if abcang != "out of range":
    #dan_a = math.degrees(an_a)
    #dan_b = math.degrees(an_b)
    #dan_c = math.degrees(an_c)
    m1 = multiprocessing.Process(target=spdcntrl,args=[1,200,(abcang[0])]) # +- 90
    m2 = multiprocessing.Process(target=spdcntrl,args=[2,200,(abcang[1])]) # +- 90
    m3 = multiprocessing.Process(target=spdcntrl,args=[3,200,(abcang[2])])
    if __name__ == '__main__':
        m1.start()
        m2.start()
        m3.start()
    print("moving to point")

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
                liovar[len(liovar)] = z,va
        print(liovar)
        print(liovar[1][0])
        cv = -5
        thetax = round(math.asin(offstx/r3),5)
        thetay = round(math.acos(offsty/r3),5)
        print(thetax, thetay)
        if abs(thetax) == abs(thetay):
            sol = math.degrees(abs(thetax))
        else:
            print("Something went wrong")
        for p in range(len(liovar)):
            print(p)
            ck_ = liovar[p][0]/sol
            if abs(ck_) < abs(cv):
                cv = ck_
                ck = liovar[p][0]
                pval = p
        print(sol)
        print(ck)
        print(ck_)
        m1 = multiprocessing.Process(target=spdcntrl,args=[1,200,(liovar[pval][1][0])]) # +- 90
        m2 = multiprocessing.Process(target=spdcntrl,args=[2,200,(liovar[pval][1][1])]) # +- 90
        m3 = multiprocessing.Process(target=spdcntrl,args=[3,200,(liovar[pval][1][2])]) # +- 90
        if __name__ == '__main__':
            m1.start()
            m2.start()
            m3.start()
        print("moving to point")