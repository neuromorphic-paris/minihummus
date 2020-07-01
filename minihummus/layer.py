import numpy as np

class Layer:
    """
    Layer of current-based Leaky-Integrate-and-Fire neurons
    """
    def __init__(self, input_neurons=0,
                       output_neurons=0,
                       tau_m=20,
                       tau_s=10,
                       refractory_period=3,
                       V_th=-50,
                       V_rest=-70,
                       I_ext=100):

        # Layer parameters
        self.output_neurons = output_neurons # number of neurons
        self.input_neurons = input_neurons # defines active input neurons
        self.active = np.ones(output_neurons, dtype=bool) # defines active LIF neurons
        self.previous_spike_out = np.zeros(output_neurons)

        # Neuron parameters
        self.tau_m = tau_m # resting membrane time constant
        self.refractory_period = refractory_period # absolute refractory period (μs)
        self.V_th = V_th # voltage threshold (mV)
        self.V_rest = np.ones(output_neurons) * V_rest # resting membrane potential (mV)
        self.V_m = np.ones(output_neurons) * V_rest # membrane potential (mV)
        self.I_m = np.zeros(output_neurons) # membrane current (pA)

        # Synapse parameters
        self.tau_s = tau_s # synaptic time constant (μs)
        self.I_ext = I_ext # external current injected into the synapses (pA)
        self.w = np.random.uniform(size=(input_neurons,output_neurons)) # synaptic weights
        self.I_syn = np.zeros([input_neurons,output_neurons])

    def update(self, spikes, t, step):

        # checking status of refractory period
        self.active[(t - self.previous_spike_out) >= self.refractory_period] = True
            
        # we decay the membrane potential for all neurons
        self.V_m += (self.V_rest - self.V_m) * (step / self.tau_m) #np.exp(- step / self.tau_m)
        
        # we decay synaptic currents
        self.I_syn -= step / self.tau_s #np.exp(- step / self.tau_s)
        
        print("t:", t, " V_m:", self.V_m)

        # handle spikes
        if len(spikes) > 0:
                
            # making sure the input neurons exist
            idx = spikes[:,1][:,None]
            print("spike for inputs:",idx)
            
            # error checking
            if (idx > self.input_neurons - 1).any() or (idx < 0).any():
                raise Exception("Spike out of range. Check that you have enough input neurons or that you don't have any negative indices.")
            else:
                
                if self.active.any():
                    # integrating spike with synaptic current
                    self.I_syn[idx,self.active] += self.w[idx,self.active] * self.I_ext

                    # calculating membrane current
                    self.I_m[self.active] = np.sum(self.I_syn, axis=0)

                    # calculating potential
                    self.V_m[self.active] += self.I_m[self.active] * (1 - np.exp(- step / self.tau_m))

                    # find neurons that crossed the threshold
                    fired = (self.V_m[self.active] >= self.V_th)

                    if fired.any():
                        print("Neurons ", np.arange(self.output_neurons)[fired]," fired!")
                        
                        # learning
                        self.learn(fired)

                        # winner-takes-all
                        self.winner_takes_all()

                        # deactivate neurons that fired (refractory period)
                        self.active[fired] = False
 
                        # saving values
                        self.previous_spike_out[fired] = t
    
    # winner-takes-all
    def winner_takes_all(self):
        self.V_m = self.V_rest
        self.I_m = np.zeros(self.output_neurons)
        self.I_syn = np.zeros([self.input_neurons,self.output_neurons])
        
    # learning rule
    def learn(self, fired):
        pass 
