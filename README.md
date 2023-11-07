# 3-joint-inverse-kinematics
Calculate the angle of a robotic arm with 3 joints quickly and precisely by providing the distance of the object from the base of the arm.
Note:
   The three joints used to reach the object can only move on a two dimentional plane

Since there are an infinite number of possible angles to reach a specific point (most of the time) the ``step`` variable is used to adjust the steps on the circumference of radius ``r3`` around the target object

## Approach
The target object with known distance from the origin will naturally have a radius of `r3` at which the third joint `L` (in diagram below) must be located in order to reach the object

![image](https://github.com/covertimpala/3-joint-inverse-kinematics/assets/77851547/a04ab50c-4fe3-40a6-9ecd-faa8da68c48c)

Hence the angles for joints 1 and 2 (`E and K` in diagram) can be solved when trying to reach a point on the circumference with radius `r3`

## Angles
The angles represent the offset from the straight position (see image below)

![image](https://github.com/covertimpala/3-joint-inverse-kinematics/assets/77851547/9ce1d924-dfde-42e0-927a-f2faff7a9286)


### To solve the angles of joints 1 and 2 (`E and K` in diagram)
#### For joint 2 (`b` in code):
joint 2 is solved first since joint 1 depends on the angle of joint 2

the cosine rule is used to obtain the following:

b = math.acos((locx^2 + locy^2 - r1^2 - r2^2) / (r1^2+r2^2))

where `locx` and `locy` represent the location on the circumference around the target object, `r1` and `r2` represents the length of the sections of the arm (see diagrams)

#### For joint 1 (`a` in code):

Calculating the angle for joint one requires more trigonometry

this section will be updated later

a = math.atan(locx/locy)-math.atan((r2*math.sin(b))/(r1+(r2*math.cos(b))))
