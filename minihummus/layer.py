import numpy as np

class Layer:
    """
    Layer of current-based Leaky-Integrate-and-Fire neurons
    """
    def __init__(self, input_neurons=0,
                       output_neurons=0,
                       tau_m=10,
                       refractory_period=3,
                       V_th=-50,
                       V_rest=-70
                       I_ex=100):

        # Layer parameters
        self.output_neurons = output_neurons # number of neurons
        self.input_neurons = np.zeros(input_neurons) # defines active input neurons
        self.active = np.ones(output_neurons, dtype=bool) # defines active LIF neurons
        self.previous_spike_in = np.zeros(input_neurons)
        self.previous_spike_out = np.zeros(output_neurons)

        # Neuron parameters
        self.tau_m = tau_m # resting membrane time constant
        self.refractory_period = refractory_period # absolute refractory period (μs)
        self.V_th = V_th # voltage threshold (mV)
        self.V_rest = V_rest # resting membrane potential (mV)
        self.V_m = np.ones(output_neurons) * V_rest # membrane potential (mV)
        self.I_m = np.zeros(output_neurons) # membrane current (pA)
        self.I_ex = I_ex # external current (pA)

        # Synapse parameters
        self.w = np.random.uniform(size=output_neurons) # synaptic weights

    def update(self, spikes, t, step):
        
        # making sure the input neurons exist
        idx = spikes[:,1]

        if (idx > len(self.input_neurons) - 1).any() or (idx < 0).any():
            raise Exception("Spike out of range. Check that you have enough input neurons or that you don't have any negative indices.")
        else:
            
            # checking status of refractory period
            self.active[idx] = True if (t - self.previous_spike_out[idx]) >= self.refractory_period
            
            # we exponentially decay the membrane potential for all neurons
            self.V_m += (self.V_rest - self.V_th) * step / self.tau_m
            
            # calculating current
            
            # calculating potential
            
            # saving values
            self.previous_spike_in[idx] == t

    def learn(self):
        pass
