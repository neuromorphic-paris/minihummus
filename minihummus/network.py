import loris
import numpy as np
from tqdm import tqdm
from . import layer

class Network:
    """
    Network class in charge of handling the spikes
    """
    def __init__(self):
        self.previous_t = 0
        self.layer = layer.Layer()
        self.spikes = list()
    
    # In this simplified simulator we will only add support for one-layer networks.
    def make_layer(self, input_neurons, output_neurons, tau_m, refractory_period, V_th, V_rest):
        self.layer = layer.Layer(input_neurons, output_neurons, tau_m, refractory_period, V_th, V_rest)
    
    # Injecting spikes in the network. data can be:
    #    1- string - path to .npy file containing spikes with the format (t,neuron_idx)
    #    2- string - path to .es file containing events with the format (t,x,y,p). 2D to 1D mapping is applied in this case
    #    3- python container (list, numpy array, deque) of spikes with the format (t,neuron_idx)
    def inject_spikes(self,data):
        # if a container is given then convert that to deque
        if isinstance(data,(list, np.ndarray)):
            self.spikes = np.array(data)
        # if string is given then load data
        elif isinstance(data, str):
            # handles .es files containing events with the format (t,x,y,p)
            if data_path.endswith('.es'):
                data_file = loris.read_file(data_path)
                for event in data_file['events']:
                    self.spikes.append([event.t, event.x + data_file['width'] * event.y])
                self.spikes = np.array(self.spikes)
            # handles .npy files containing numpy arrays with the format (t,neuron_idx)
            elif data_path.endswith('.npy'):
                self.spikes = np.load(data_path)
        else:
            raise Exception("unsupported data format")
    
    # run the network
    # runtime: in microsecond
    # step: in microseconds defines the temporal resolution
    def run(self, runtime, step):
        for t in tqdm(range(0, runtime+step, step)):
            # getting spikes between t-1 and t
            current_spikes = self.spikes[(self.spikes[:,0] <= t) & (self.spikes[:,0] > self.previous_t)]
            
            # update neurons if we have spikes
            if len(current_spikes) > 0:
                self.layer.update(current_spikes, t, step)
            
            # save current timestamp
            self.previous_t = t
                    
        print("Network finished running at t=%s" % t)