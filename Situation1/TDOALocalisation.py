import numpy as np
import intersection

class TDOALocalisation:
    """
    source = (0, 0)
    sensors = 
    [
            (350, -300),
            (650, -150),
            (150, 200),
        ]
    ++ other parameters
    time_noise should be written in microseconds
    """
    def __init__(self, source, sensors, T=20, 
            n_elts=50, step=0.5, max_dist=500, time_noise=0):
        # Number of points per circle
        self.n_elts = n_elts
        
        # Circles step in meters for computations
        self.step = step
        # Max distance between 2 sensors
        self.max_dist = max_dist
        self.steps = np.arange(0, self.max_dist, self.step)
        # Temperature in degree Celsius 
        self.T = T
        # Position of the source
        self.source = source
        # List of tuples that represent the position of each sensor
        self.sensors = sensors
        # Celerity calculationfor dry air
        self.c = 20.05 * np.sqrt(self.T + 273.15)
        
        self.time_noise = time_noise
        # computations 
        self.tdoa, self.first_sensor_idx = self.TDOA()
        self.distance = self.get_distance_fromtime(self.tdoa)


    def algebric_distance(self, pos0, posi):
        """
        computes the algebric distance between 2 points. Each point in the input must be a tuple 
        Example: algebric_distance((2, 3), (4, 5))
        """
        xi, yi = posi
        x0, y0 = pos0
        di = np.sqrt( (xi - x0)**2 + (yi - y0)**2 )
        return di


    def get_timedelay_from_pos(self):
        """
        From the source position, we compute the time delays at which each sensor gets the signal
        """
        time_delay = []
            
        for s in self.sensors:
            time_delay.append(self.algebric_distance(s, self.source)/ self.c)
        return np.array(time_delay)
    

    def get_distance_fromtime(self, time_delay):
        """
        Uses temperature data and time delay measured to compute the distance 
        where the event occured for each sensor
        """
        # Computes the distance at which the event occured for each sensor
        dist = self.c * time_delay
        return dist


    def TDOA(self):
        """
        From the computed time delays, we get the TDOA values as well as the indice of the sensor which is the first to receive the signal
        
        """
        time_delay = self.get_timedelay_from_pos() 
        d_time_noise = np.random.uniform(-1 * self.time_noise, self.time_noise) * 1e-6

        # the sensor with the shortest time delay is the first one to receive the signal
        first_sensor = np.argmin(time_delay)
        TDOA = time_delay - time_delay[first_sensor] + d_time_noise
        return TDOA, first_sensor


    def get_circle(self, r, origin):
        """
        returns the equation x,y of a circle depending on the origin point (tuple) and the radius (float)
        """
        theta = np.linspace(0, 2 * np.pi, self.n_elts)
        x = r * np.cos(theta) + origin[0]
        y = r * np.sin(theta) + origin[1]
        return x, y


    def get_circle_intersections(self, P1, r1, P2, r2):
        """
        Center of the two circles whose intersections are computed
        P1 = (x1, y1)
        P2 = (x2, y2)
        Based on: 
        https://gamedev.stackexchange.com/questions/7172/how-do-i-find-the-intersections-between-colliding-circles
        """
        x1, y1 = P1
        x2, y2 = P2
        # distance between the 2 circles, equation 1
        d = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        # equation 2: simple cases
        # no collision
        if d > (r2 + r1):
            return ((None, None), (None, None))
        # full containment
        elif d == 0 or d < abs(r2 - r1):
            return ((None, None), (None, None))
        # equation 3
        a = (r1**2 - r2**2 + d**2) / (2 * d)
        # equation 4
        h = np.sqrt(r1**2 - a**2)
        # equation 5, P3 = P1 + a * (P2 - P1) / d
        x3 = x1 + a * (x2 - x1) / d
        y3 = y1 + a * (y2 - y1) / d
        # only 1 intersection point --> equation 6
        if d == r1 + r2:
            x_alpha = x3
            y_alpha = y3
            x_beta = None
            y_beta = None
        
        else:
            # 2 intersection points called "alpha" and "beta" --> equation 8 
            x_alpha = x3 + h * (y2 - y1) / d
            y_alpha = y3 - h * (x2 - x1) / d
            # equation 9
            x_beta = x3 - h * (y2 - y1) / d
            y_beta = y3 + h * (x2 - x1) / d
        return (x_alpha, y_alpha), (x_beta, y_beta)


    def get_2circles_hyperbola(self, sensor_idx):
        hyperbola = []
        first_part = []
        second_part = []
        
        # position of the n-th sensor
        sensor = self.sensors[sensor_idx]
        # position of the reference sensor
        first_sensor = self.sensors[self.first_sensor_idx]
        for r in self.steps:
            # plotting in this loop would give concentric circles
            
            # radius of the circle around the n-th sensor
            r_sensor = r + self.distance[sensor_idx]
            # radius of the circle around the reference sensor
            r_first = r + self.distance[self.first_sensor_idx]
            # circ = self.get_circle(r_sensor, sensor)
            intersec = self.get_circle_intersections(first_sensor, r_first, sensor, r_sensor)
            # add the points of intersection only if they exist.
            if (None, None) not in intersec:
                first_part.append(intersec[0])
                second_part.append(intersec[1])
        # computation of each part of the hyperboloid (see scheme included)
        hyperbola = first_part[::-1] + second_part
        return hyperbola
    

    def get_all_hyperboloid(self):
        """
        computes the previous function for the number of sensors and returns a list of lists of hyperboloids
        """
        result = []
        for p in range(len(self.sensors)):
            if p != self.first_sensor_idx:
                hyperb = self.get_2circles_hyperbola(p)
                result.append(hyperb)
        return result


    def intersection_estimation(self, data):
        """
        Estimates a single intersection point between every curve computed
        """
        position = []
        for i in range(len(data)):
            position.append(np.array([list(j) for j in zip(*data[i])]))

        x_inters, y_inters = [], []
        approxx, approxy = [], []

        for i in range(len(data) - 1):
            for j in range(i + 1, len(data)):
                x_inter, y_inter = intersection.intersection(position[i][0], position[i][1], position[j][0], position[j][1])
                if len(x_inter) == 1:
                    approxx.append(float(x_inter))
                    approxy.append(float(y_inter))
                x_inters.append(x_inter)
                y_inters.append(y_inter)

        mean = np.mean([float(x_inters[i]) for i in range(len(x_inters)) if len(x_inters[i]) == 1])
        ambig = [i for i in range(len(x_inters)) if len(x_inters[i]) > 1]
        for i in ambig:
            indice = np.argmin([np.abs(pt - mean) for pt in x_inters[i]])
            approxx.append(x_inters[i][indice])
            approxy.append(y_inters[i][indice])
        mean = (np.mean(approxx), np.mean(approxy))
        return x_inters, y_inters, mean