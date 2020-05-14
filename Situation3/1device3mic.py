import numpy as np
import matplotlib.pyplot as plt
import itertools


class Device3:
    """
    This class defines the geometry of the considered sensor set: the microphones are in a triangle layout
    """
    def __init__(self, center_position, angle=0, r=0.1):
        
        self.angle = angle
        self.C = center_position
        iteration = list(itertools.combinations([0,1,2], 2))
        
        ang = 2 * np.pi / 3
        self.M_position = [
            (center_position[0] + r*np.cos(angle + n*ang), 
             center_position[1] + r*np.sin(angle + n*ang)) for n in range(3)] 
        self.C_M_position = []
        
        for a, b in iteration:
            center_mic_iter = ((self.M_position[a][0] + self.M_position[b][0])/2, (self.M_position[a][1] + self.M_position[b][1])/2)
            self.C_M_position.append(center_mic_iter)
        
        self.dist_M = [algebric_distance(self.M_position[a], self.M_position[b]) for a, b in iteration]
        self.slope_M = np.array([(self.M_position[b][1] - self.M_position[a][1]) / (self.M_position[b][0] - self.M_position[a][0]) for a, b in iteration]) 
        self.angle_M = [np.arctan(self.slope_M[i]) for i in range(3)]

    def plot(self, figure):
        for mpos in self.M_position:
            figure.plot(*mpos, "ok")
        for mcen in self.C_M_position:
            figure.plot(*mcen, "or")
        figure.plot(
            [self.M_position[0][0], self.C[0], self.M_position[1][0], self.C[0], self.M_position[2][0]],
            [self.M_position[0][1], self.C[1], self.M_position[1][1], self.C[1], self.M_position[2][1]],
            'k')
        return

####################################################


class Situation3:
    def __init__(self, source, device):
        self.source_position = source
        self.device = device        
        T = 20
        self.c = 20.05 * np.sqrt(T + 273.15)

        self.timedelay_forsimu = [self.get_timedelay_from_pos(dev) for dev in self.device]

    def get_timedelay_from_pos(self, device_i):
        """
        From the source position, we compute the time delays at which each sensor gets the signal
        """
        time_delay = []
        center_time_delay = []
        for s in device_i.M_position:
            time_delay.append(algebric_distance(s, self.source_position)/ self.c)
        for center in device_i.C_M_position:
            center_time_delay.append(algebric_distance(center, self.source_position) / self.c)
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
        alpha.append(np.arccos(self.c * self.get_TDOA_for_device(device_i)[0] / device_i.dist_M))
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
if __name__ == "__main__":
    def algebric_distance(pos0, posi):
        """
        computes the algebric distance between 2 points. Each point in the input must be a tuple 
        Example: algebric_distance((2, 3), (4, 5))
        """
        di = np.sqrt( (posi[0] - pos0[0])**2 + (posi[1] - pos0[1])**2 )
        return di

    mic = Device3((0, 0), angle=0, r=0.1)
    source = Situation3((7,5), [mic])
    x = np.linspace(-5, 5, 100)

    a1, a2, b1, b2 = source.source_position_computation_i(mic)
    y1 = []
    y2 = []

    for i in range(3):
        y1.append(a1[i]*x + b1[i])
        y2.append(a2[i]*x + b2[i])


    fig, ax = plt.subplots()

    mic.plot(ax)
    ax.plot(*source.source_position, 'r^')

    for i in range(3):
        ax.plot(x, y1[i], 'k--')
        ax.plot(x, y2[i], 'k--')
    
    ax.axis('equal')
    plt.show()

