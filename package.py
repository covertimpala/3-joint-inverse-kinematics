import math

# Returns values in degrees
# Call choosepos to use
# Example of usage:
#  print(choosepos(5, 5, 5, 4, 6, 2, [-90,90], 1))

def calculateab(locx, locy, o, r1, r2, r3, _range, bypass, x_dist, y_dist):
    b = math.acos((locx**2 + locy**2 - r1**2 - r2**2) / (r1**2+r2**2))#(r1**2+r2**2)            (2*r1*r2)
    bt = math.degrees(b)
    val=""
    if bt >= _range[0]*bypass and bt <=_range[1]*bypass:
        a = math.atan(locx/locy)-math.atan((r2*math.sin(b))/(r1+(r2*math.cos(b))))
        at = math.degrees(a)
        if at >= _range[0]*bypass and at <=_range[1]*bypass:
            ys = (((locy-r1*math.cos(a))/(locx-r1*math.sin(a)))*(x_dist-r1*math.sin(a))+r1*math.cos(a)) #equation of the line from r2
            ds = math.sqrt((x_dist-locx)**2 + (ys-locy)**2) #side 1
            ds3 = abs(ys-y_dist) #side 3
            c = math.degrees(math.acos((ds**2+r3**2-ds3**2)/(2*ds*r3))) #Cosine rule
            if x_dist < locx:
                cp = c-180
                if cp >= _range[0]*bypass and cp <= _range[1]*bypass:
                    val = at,bt,cp
            elif c >= _range[0] and c <=_range[1]:
                val = at,bt,c
    return(val)

def choosepos(segment1, segment2, segment3, x_dist, y_dist, step, _range, bypass):
    results = {}
    for i in range(359*step):
        x_p = segment3*math.cos(math.radians(i/step))#r3*math.cos(math.radians(i))
        y_p = segment3*math.sin(math.radians(i/step))#r3*math.sin(math.radians(i))
        joint3loc = [x_dist+x_p, y_dist+y_p]
        try:
            re = calculateab(joint3loc[0], joint3loc[1],i/step, segment1, segment2, segment3, _range, bypass, x_dist, y_dist)
            if re != "":
                results[int(i/step)] = re
        except Exception as f:
            if str(f) == "math domain error":
                continue
            else:
                print(f)
                break
    return(results)
#print(choosepos(5, 5, 5, 4, 6, 2, [-90,90], 1))