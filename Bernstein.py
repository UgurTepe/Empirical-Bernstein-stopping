import numpy as np

# Welford method to get the running standard deviation and the running mean
class Welford():
    def __init__(self,a_list=None):
        self.n = 0
        self.M = 0
        self.S = 0

    def update(self,x):
        self.n += 1
        newM = self.M + (x - self.M) / self.n
        newS = self.S + (x - self.M) * (x - newM)
        self.M = newM
        self.S = newS

    @property
    def mean(self):
        return self.M

    @property
    def std(self):
        if self.n == 1:
            return 0
        return np.sqrt(self.S / (self.n - 1))

class Bernstein_simple():
    # Initlialize Bernstein with epsilon and delta
    def __init__(self, delta=0.1, epsilon=0.01, rng=1):
        self.delta = delta
        self.epsilon = epsilon
        self.rng = rng
        self.samples = []
        self.running_mean = []
        self.sample_sum = 0
        self.running_variance = []
        self.ct = []
        self.p = 1.1
        self.current_step = 1
        self.cons = 3/((delta*(self.p-1))/self.p)
        self.welf = Welford()

    # Should add sample to self.samples and should update all the parameters
    def add_sample(self, sample):
        # Insert new sample
        self.samples.append(sample)

        # cummulative sum
        self.sample_sum += sample

        # Calculates the running mean efficiently with sample_sum
        cur_mean = self.sample_sum / self.current_step
        self.running_mean.append(cur_mean)

        # Running variance
        self.welf.update(sample)
        self.running_variance.append(np.square(self.welf.std))

        # Update ct
        self.ct.append(self.calc_ct(self.current_step))

        # Update current step
        self.current_step = self.current_step + 1

    # Either returns true or false, depending on wheter EBS stopped or not
    # Loop in main program should check this every iteration to determine
    # Loop in application should check for this to be False --> termiante 
    def cond_check(self):
        if self.current_step == 1:
            return True
        if self.ct[-1] > self.epsilon*self.running_mean[-1]:
            return True
        else:
            return False

    # Just a function to calculate c_t for a given time t  
    def calc_ct(self,time):
            ln_constant = np.log(self.cons, dtype=np.float64)/time
            ln_vari = self.p*np.log(time, dtype=np.float64)/time
            ln_compl = (ln_constant+ln_vari)
            result = (np.sqrt(2*self.running_variance[-1]*ln_compl) + (3*self.rng*ln_compl))
            return result

    def show_ct(self):
        return np.asarray(self.ct)

    # Should return the latest estimated mean
    def get_estimate(self):
        return self.running_mean[-1]

    # Should return the array of the estimated means
    def get_mean(self):
        return np.asarray(self.running_mean)
    
    # Should return the array of the variances
    def get_var(self):
        return np.asarray(self.running_variance)