import math
import numpy as np

class Plane:
    def __init__(self,Origin,XAxis,YAxis,ZAxis):
        self.Origin = Origin
        self.XAxis = XAxis
        self.YAxis = YAxis
        self.ZAxis = ZAxis


def Angle(v1, v2):
    v1_u = VectorUnitize(v1)
    v2_u = VectorUnitize(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def VectorCrossProduct(vector1,vector2):
    return np.cross(vector1,vector2)

def VectorUnitize(vector):
    return vector / np.linalg.norm(vector)


def VectorCreate(to_point, from_point):
    vector = [to_point[0] - from_point[0], 
              to_point[1] - from_point[1], 
              to_point[2] - from_point[2]]
    return vector

ref = Plane(Origin=[0,0,0],
            XAxis=[1,0,0],
            YAxis=[0,1,0],
            ZAxis=[0,0,1])

plane = Plane(Origin=[0,0,0],
              XAxis=[0.816857,-0.315957,-0.482613],
              YAxis=[0,0.83665,-0.547737],
              ZAxis=[0.57684,0.447423,0.683424])


# Z Axis Quaternion


def axisQuaternion(ref_vector,target_vector,reflex,cross_vector=None):

    if reflex == 0:
        angle = Angle(ref_vector,target_vector)
    else:
        angle = (2 * math.pi) - Angle(ref_vector,target_vector)
    
    if not cross_vector:
        cross = VectorCrossProduct(ref_vector, target_vector)
    else:
        cross = cross_vector
        
    if (np.array(cross) - VectorCreate([0,0,0],[0,0,0])).all():
        if ref_vector == VectorCreate([0,0,1],[0,0,0]):
            cross = VectorCreate([1,0,0],[0,0,0])
        
    cross = VectorUnitize(cross)
    
    q1 = math.cos(angle/2)
    q2 = cross[0] * (math.sin(angle/2))
    q3 = cross[1] * (math.sin(angle/2))
    q4 = cross[2] * (math.sin(angle/2))
    
    return [q1,q2,q3,q4]

zq = axisQuaternion(ref.ZAxis,plane.ZAxis,0)

# Find new X Axis Vector

def vectorRotation(a,b,c,d,x,y,z):
    
    """
    qv' = q * qv * q^-1

    q = a + bi + cj + dk

    q^-1 = q conjugate = a - bi - cj - dk

    qv =0 + xi + yj + zk

    qv' = 0 + x'i + y'j + z'k

    v' = (f',g',h')
    """
    
    e = 0
    #q * qv
    
    qq1 = (a*e) - (b*x) - (c*y) - (d*z)
    qq2 = (a*x) + (b*e) + (c*z) - (d*y)
    qq3 = (a*y) - (b*z) + (c*e) + (d*x)
    qq4 = (a*z) + (b*y) - (c*x) + (d*e)
    
    # q conjugate
    
    qc1 = a
    qc2 = -1 * b
    qc3 = -1 * c
    qc4 = -1 * d
    
    # qv' = (q * qv) * q conjugate

    qv1 = round((qq1*qc1) - (qq2*qc2) - (qq3*qc3) + (qq4*qc4),15)
    qv2 = round((qq1*qc2) + (qq2*qc1) + (qq3*qc4) - (qq4*qc3),15)
    qv3 = round((qq1*qc3) - (qq2*qc4) + (qq3*qc1) + (qq4*qc2),15)
    qv4 = round((qq1*qc4) + (qq2*qc3) - (qq3*qc2) + (qq4*qc1),15)
    
    return VectorUnitize([qv2,qv3,qv4])

x_vector = vectorRotation(zq[0],zq[1],zq[2],zq[3],ref.XAxis[0],ref.XAxis[1],ref.XAxis[2])

# X Axis Quaternion

xq = axisQuaternion(x_vector,plane.XAxis,1,ref.ZAxis)

# Z&X Quaternion Combination

def multiplyQuaternion(q1,q2):
    qm1 = (q1[0]*q2[0]) - (q1[1]*q2[1]) - (q1[2]*q2[2]) - (q1[3]*q2[3])
    qm2 = (q1[0]*q2[1]) + (q1[1]*q2[0]) + (q1[2]*q2[3]) - (q1[3]*q2[2])
    qm3 = (q1[0]*q2[2]) - (q1[1]*q2[3]) + (q1[2]*q2[0]) + (q1[3]*q2[1])
    qm4 = (q1[0]*q2[3]) + (q1[1]*q2[2]) - (q1[2]*q2[1]) + (q1[3]*q2[0])
    
    return [qm1,qm2,qm3,qm4]

q = multiplyQuaternion(zq,xq)

q1 = q[0]
q2 = q[1]
q3 = q[2]
q4 = q[3]

x_vector2 = vectorRotation(q1,q2,q3,q4,ref.XAxis[0],ref.XAxis[1],ref.XAxis[2])

test = 0

for i in range(3):
    if round(x_vector2[i],5) != round(plane.XAxis[i],5):
        test += 1
        
if test > 0:
    xq = axisQuaternion(x_vector,plane.XAxis,0,ref.ZAxis)
    q = multiplyQuaternion(zq,xq)
    q1 = -1 * q[0]
    q2 = -1 * q[1]
    q3 = -1 * q[2]
    q4 = -1 * q[3]
    


#print(test)
#print("target =",plane.XAxis)
#print("final  =",x_vector2)
m = x_vector2


# Misc Outputs

x = round(plane.Origin[0],6)
y = round(plane.Origin[1],6)
z = round(plane.Origin[2],6)

q1 = round(q[0],6)
q2 = round(q[1],6)
q3 = round(q[2],6)
q4 = round(q[3],6)

print(f'{q1}\n{q2}\n{q3}\n{q4}')