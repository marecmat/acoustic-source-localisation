import numpy as np
import matplotlib.pyplot as plt

class Point:
    def __init__(self, x, y ,source=False):
        self.x = x
        self.y = y
        self.source = source
        self.toa = 0 if self.source==True else dist(self, S)/c
     

class Sensor:
    def __init__(self, ma, mb):
        self.A1 = ma if ma.toa < mb.toa else mb
        self.A2 = mb if ma.toa < mb.toa else ma
        self.centre = Point((self.A1.x + self.A2.x)/2, (self.A1.y + self.A2.y)/2, (self.A1.toa + self.A2.toa)/2)
        self.tdoa = (self.A2.toa - self.A1.toa)
        if self.A1.y - self.A2.y != 0:  #A expliquer
            self.signeBeta = (self.A1.y - self.A2.y)/np.abs(self.A1.y - self.A2.y) 
        else:
            self.signeBeta = 0

def dist(A1, A2):
    return np.sqrt((A1.x - A2.x)**2 + (A1.y - A2.y)**2)

def get_alpha(S1):
    # Entry : class Sensor
    # Return : angle alpha between the sensor and the source
    alpha = np.arccos(c*S1.tdoa/dist(S1.A1, S1.A2))
    return alpha

def get_beta(S1):
    beta = np.arctan((S1.A1.y - S1.A2.y)/(S1.A1.x - S1.A2.x))
    beta = beta + S1.signeBeta*np.pi if S1.A1.x - S1.A2.x < 0 else beta
    return beta

def dt_inter(S1,S2,X,Y):
    dt = np.abs(dist(S2.centre, Point(X, Y)) - dist(S1.centre, Point(X, Y)))/c
    return dt


S = Point(6.2, 4.75, source=True)            #Position of the source   
T = 20                                       #Temperature
c = 20.05 * np.sqrt(T + 273.15)              #Speed of sound

if __name__ == "__main__":

#DEFINITIONS OF POSITIONS OF THE PHYSICAL DATA OF THE PROBLEM  

    #Position of the sensor 1
    A1 = Point(3, 4)  
    A2 = Point(2, 5)
    S1 = Sensor(A1, A2)
    
    #Position of the sensor 2
    B1 = Point(6, 2)
    B2 = Point(7, 3)
    S2 = Sensor(B1, B2)
    
    #List of sensors (Useful for generalization to N sensor)
    listSn=[S1,S2]
    
    #Delay of TOAs between both sensor centers 
    dt = np.abs(S2.centre.toa - S1.centre.toa)  

#COMPUTING OF ALL THE PROBABLE SOLUTIONS
    #Computing of angle alpha between the sensor and the source   
    listAlpha = [get_alpha(n) for n in listSn]
   
    #Computing of angle alpha between the sensor and the X-axis  
    listBeta = [get_beta(n) for n in listSn]
    
    #Computing of linear functions with alpha and -alpha (to improve for N sensors)    
    #Computing of a for all combinaison of +-Alpha and Beta
    a=[]
    for i in range(len(listAlpha)):
        a.append(np.tan(listAlpha[i]+listBeta[i]))
    for i in range(len(listAlpha)):
        a.append(np.tan(-listAlpha[i]+listBeta[i]))
    
    #Computing of a for all a        
    b=[]
    n=0
    while n < len(a):
        for i in range(len(listSn)):
            b.append(listSn[i].centre.y - a[n]*listSn[i].centre.x)
            n += 1
            
    #Computing of the 4 intersections
    #Computing of the X-coordinate of the intersection (to improve for N sensors)
    Xinter = [(b[1] - b[0])/(a[0] - a[1]),
              (b[3] - b[0])/(a[0] - a[3]),
              (b[3] - b[2])/(a[2] - a[3]),
              (b[1] - b[2])/(a[2] - a[1])]
    
    #Computing of the Y-coordinate of the intersection (to improve for N sensors)
    Yinter = [a[0]*Xinter[0] + b[0],
              a[0]*Xinter[1] + b[0],
              a[2]*Xinter[2] + b[2],
              a[2]*Xinter[3] + b[2]]
    
#SELECT THE RIGHT SOLUTION
    #Computing all the delay from each intersection to the center of each sensor
    dt_Inter=[]
    for n in range(len(Xinter)):
        dt_Inter.append(dt_inter(S1,S2,Xinter[n],Yinter[n]))
        
    #Select the position in the dt_list with minimum delay between dt and dt_Inter
    inter = [i for i in range(len(dt_Inter)) if np.abs(dt - dt_Inter[i]) == min([np.abs(dt - dt_Inter[j]) for j in range(4)])][0]
 
#PRINTING OF THE FINAL SOLUTION
    #Print the final solution
    A, B = Xinter[inter], Yinter[inter]
    print('position estimée de la source: ({:.3f}, {:.3f})'.format(A, B))

    x = np.linspace(-10, 20, 1000)
    plt.figure()
    #plt.plot(x, a[inter]*x + b[inter])
    for g in range(4):
        plt.plot(x, a[g]*x+b[g], 'k', alpha=0.5)
        plt.plot(Xinter[g], Yinter[g], 'ok')
    plt.plot([A1.x, A2.x], [A1.y, A2.y], '^-b', label='Sensor1')
    plt.plot([B1.x, B2.x], [B1.y, B2.y], '^-c', label='Sensor2')
    plt.plot(S.x, S.y, 'r*', label='source')
    plt.plot(A, B, '+y', label='estimation')
    plt.ylim(-5, 20)
    plt.legend()
    plt.show()
