import numpy as np
import matplotlib.pyplot as plt

ang = 2 * np.pi / 3
T = 20
c = 20.05 * np.sqrt(T + 273.15)


class Device3:
    def __init__(self, center_position, angle=0, r=0.1):
        
        self.angle = angle
        self.C = center_position
        self.M1 = (center_position[0] + r*np.cos(angle), center_position[1] + r*np.sin(angle))
        self.M2 = (center_position[0] + r*np.cos(angle + ang), center_position[1] + r*np.sin(angle + ang))
        self.M3 = (center_position[0] + r*np.cos(angle + 2*ang), center_position[1] + r*np.sin(angle + 2*ang))
        self.M_position = [self.M1, self.M2, self.M3]
        
        self.C_M1_2 = ((self.M1[0] + self.M2[0])/2, (self.M1[1] + self.M2[1])/2)
        self.C_M2_3 = ((self.M2[0] + self.M3[0])/2, (self.M2[1] + self.M3[1])/2)
        self.C_M3_1 = ((self.M1[0] + self.M3[0])/2, (self.M1[1] + self.M3[1])/2)
        self.C_M_position = [self.C_M1_2, self.C_M2_3, self.C_M3_1]
        
#        self.dist_M1_2 = np.sqrt( (self.M1[0] - self.M2[0])**2 + (self.M1[1] - self.M2[1])**2 )
        self.dist_M1_2 = algebric_distance(self.M1, self.M2)
        self.dist_M2_3 = algebric_distance(self.M2, self.M3)
        self.dist_M3_1 = algebric_distance(self.M1, self.M3)
        self.dist_M = [self.dist_M1_2, self.dist_M2_3, self.dist_M3_1]
        
        self.slope_M1_2 = (self.M2[1]- self.M1[1])/(self.M2[0]- self.M1[0])
        self.angle_M1_2 = np.arctan(self.slope_M1_2)
        self.slope_M2_3 = (self.M3[1]- self.M2[1])/(self.M3[0]- self.M2[0])
        self.angle_M2_3 = np.arctan(self.slope_M2_3)
        self.slope_M3_1 = (self.M1[1]- self.M3[1])/(self.M1[0]- self.M3[0])
        self.angle_M3_1 = np.arctan(self.slope_M3_1)
        self.slope_M = np.array([self.slope_M1_2, self.slope_M2_3, self.slope_M3_1])
        self.angle_M = [self.angle_M1_2, self.angle_M2_3, self.angle_M3_1]
        
    def plot(self, figure):
        figure.plot(*self.M1, "ok")
        figure.plot(*self.C_M1_2, "or")
        figure.plot(*self.M2, "ok")
        figure.plot(*self.C_M2_3, "or")
        figure.plot(*self.M3, "ok")
        figure.plot(*self.C_M3_1, "or")
        figure.plot([self.M1[0], self.C[0], self.M2[0], self.C[0], self.M3[0]], 
                    [self.M1[1], self.C[1], self.M2[1], self.C[1], self.M3[1]],
                    'k')
        return
####################################################


class Situation3:
    def __init__(self, source, device):
        self.source_position = source
        self.device = device
        
        self.timedelay_forsimu = [self.get_timedelay_from_pos(dev) for dev in self.device]

    def get_timedelay_from_pos(self, device_i):
        """
        From the source position, we compute the time delays at which each sensor gets the signal
        """
        time_delay = []
        center_time_delay = []
        for s in device_i.M_position:
            time_delay.append(algebric_distance(s, self.source_position)/ c)
        for center in device_i.C_M_position:
            center_time_delay.append(algebric_distance(center, self.source_position)/c)
        return np.array(time_delay), np.array(center_time_delay)
    
    def get_TDOA_for_device(self, device_i):
        time_delay, center_time_delay = self.get_timedelay_from_pos(device_i)
        first_sensor = np.argmin(time_delay)
        first_center = np.argmin(center_time_delay)
        TDOA = time_delay - time_delay[first_sensor]
        center_TDOA = center_time_delay - center_time_delay[first_center]
        return TDOA, center_TDOA, first_sensor, first_center
    
    def get_order(self, device_i):
        time_delay, center_time_delay = self.get_timedelay_from_pos(device_i)
        order_S, order_C = np.argsort(time_delay), np.argsort(center_time_delay)
        return order_S, order_C

    def get_alpha(self, device_i):
        # Entry : class Sensor
        # Return : angle alpha between the sensor and the source
        alpha = []
        alpha.append(np.arccos(c*self.get_TDOA_for_device(device_i)[0]/device_i.dist_M))
        return alpha[0]
    
    def get_beta(self, device_i):
        beta = []
        for i in range(3):
            if device_i.M_position[i][0] < device_i.M_position[(i+1)%3][0]:
                if device_i.M_position[i][1] < device_i.M_position[(i+1)%3][1]:
                    beta.append(np.arctan(device_i.slope_M[i]))
                else:
                    beta.append(-np.arctan(device_i.slope_M[i]))
            else:
                if device_i.M_position[i][1] < device_i.M_position[(i+1)%3][1]:
                    beta.append(-np.arctan(device_i.slope_M[i]))
                else:
                    beta.append(np.arctan(device_i.slope_M[i]))
        return np.array(beta)
                
    def TDOA(self):
        """
        From the computed time delays, we get the TDOA values as well as the indice 
        of the sensor which is the first to receive the signal
        """
#        time_delay = self.get_timedelay_from_pos() 
#        d_time_noise = np.random.uniform(-1 * self.time_noise, self.time_noise) * 1e-6
        # the sensor with the shortest time delay is the first one to receive the signal
        TDOA = []
        i = 0
        for t_delay in self.timdelay_forsimu:
            first_sensor_i = np.argmin(t_delay)
            TDOA.append([])
            TDOA[i].append(t_delay - t_delay[first_sensor_i]) #+ d_time_noise
        return TDOA
    
    def source_position_computation_i(self, device_i):
        TDOA_i, center_TDOA_i, first_sensor_i, first_center_i= self.get_TDOA_for_device(device_i)
        order_S, order_C = self.get_order(device_i)
        
        list_alpha =  self.get_alpha(device_i)
        list_beta = self.get_beta(device_i)
        theta_pos = list_beta + list_alpha
        theta_neg = list_beta - list_alpha
        
        b_line_pos = np.array(device_i.C_M_position)[:,1] - np.tan(theta_pos) * np.array(device_i.C_M_position)[:,1]
        b_line_neg = np.array(device_i.C_M_position)[:,1] - np.tan(theta_neg) * np.array(device_i.C_M_position)[:,1]
        
        return np.tan(theta_pos), np.tan(theta_neg), b_line_pos, b_line_neg
    
    def plot_result(self,figure, device_i):
        figure.plot([self.source_position[0], device_i.C_M1_2[0]], [self.source_position[1], device_i.C_M1_2[1]])
        figure.plot([self.source_position[0], device_i.C_M2_3[0]], [self.source_position[1], device_i.C_M2_3[1]])
        figure.plot([self.source_position[0], device_i.C_M3_1[0]], [self.source_position[1], device_i.C_M3_1[1]])
        
        

####################################################

def algebric_distance(pos0, posi):
    """
    computes the algebric distance between 2 points. Each point in the input must be a tuple 
    Example: algebric_distance((2, 3), (4, 5))
    """
    di = np.sqrt( (posi[0] - pos0[0])**2 + (posi[1] - pos0[1])**2 )
    return di

def dt_inter(S1,S2,point):
    dt = np.abs(algebric_distance(S2, point) - algebric_distance(S1, point))/c
    return dt

#def dt_inter(S1,S2,X,Y):
#    dt = np.abs(dist(S2.centre, Point(X, Y)) - dist(S1.centre, Point(X, Y)))/v
#    return dt

mic = Device3((0,0), angle=0, r=0.1)

test = Situation3((2,2), [mic])
#pos = test.source_position_computation_i(mic)
x = np.linspace(-10, 10, 100)

a1, a2, b1, b2 = test.source_position_computation_i(mic)

y1 = []
y2 = []
for i in range(3):
    y1.append(a1[i]*x + b1[i])
    y2.append(a2[i]*x + b2[i])

fig, ax = plt.subplots()

mic.plot(ax)
#test.plot_result(ax, mic)
ax.axis("equal")
#ax.plot(*pos, 'b^')
ax.plot(*test.source_position, 'r^')

for i in range(3):
    ax.plot(x, y1[i])
    ax.plot(x, y2[i])

# test.plot_result(ax, mic)

# angl = [np.pi/6 *i for i in range(12)]

# for i in angl:
#     mic_test = Device3((0,0), angle = i, r=0.1)
#     testt = Situation3((0.2,0.2),[mic_test])
#     print(testt.get_beta(mic_test))
