# 3-joint-inverse-kinematics
Calculate the angle of a robotic arm with 3 joints quickly and precisely by providing the distance of the object from the base of the arm.
Note:
   The three joints used to reach the object can only move on a two dimentional plane

Since there are an infinite number of possible angles to reach a specific point (most of the time) the ``step`` variable is used to adjust the steps on the circumference of radius ``r3`` around the target object
