import pygad.gann as gann
import pygad.nn as nn
import numpy as np
import os, sys

p = os.path.abspath('.')
sys.path.insert(1, p)
from evoman.controller import Controller

# implementation of player controller
class player_controller(Controller):
    def __init__(self, population: int, generations: int):
        self.population = population
        self.generations = generations

        self.networks = gann.GANN(
            num_solutions = population,
            num_neurons_input = 20,
            num_neurons_hidden_layers = [10],
            num_neurons_output = 5,
            output_activation = "sigmoid",
            hidden_activations = "sigmoid"
        )

    def control(self, inputs: np.ndarray, controller=None):
        # nn.predict() returns an array with an integer for each input which represents the activated output neuron
        prediction = nn.predict(self.networks.population_networks[self.current_solution], np.array([inputs]))
        action = [0, 0, 0, 0, 0]
        action[round(prediction[0])] = 1
        return action

def sigmoid_activation(x):
	return 1./(1.+np.exp(-x))

# implements controller structure for player
class player_controller_demo(Controller):
	def __init__(self, _n_hidden):
		# Number of hidden neurons
		self.n_hidden = [_n_hidden]

	# def vector_to_network():
	# 	pass

	def control(self, inputs, controller):
		# Normalises the input using min-max scaling
		inputs = (inputs-min(inputs))/float((max(inputs)-min(inputs)))

		if self.n_hidden[0]>0:
			# Preparing the weights and biases from the controller of layer 1
			# Biases for the n hidden neurons
			bias1 = controller[:self.n_hidden[0]].reshape(1,self.n_hidden[0])
			# Weights for the connections from the inputs to the hidden nodes
			weights1_slice = len(inputs)*self.n_hidden[0] + self.n_hidden[0]
			weights1 = controller[self.n_hidden[0]:weights1_slice].reshape((len(inputs),self.n_hidden[0]))

			# Outputs activation first layer.
			output1 = sigmoid_activation(inputs.dot(weights1) + bias1)

			# Preparing the weights and biases from the controller of layer 2
			bias2 = controller[weights1_slice:weights1_slice + 5].reshape(1,5)
			weights2 = controller[weights1_slice + 5:].reshape((self.n_hidden[0],5))

			# Outputting activated second layer. Each entry in the output is an action
			output = sigmoid_activation(output1.dot(weights2)+ bias2)[0]
		else:
			bias = controller[:5].reshape(1, 5)
			weights = controller[5:].reshape((len(inputs), 5))

			output = sigmoid_activation(inputs.dot(weights) + bias)[0]

		# takes decisions about sprite actions
		if output[0] > 0.5:
			left = 1
		else:
			left = 0

		if output[1] > 0.5:
			right = 1
		else:
			right = 0

		if output[2] > 0.5:
			jump = 1
		else:
			jump = 0

		if output[3] > 0.5:
			shoot = 1
		else:
			shoot = 0

		if output[4] > 0.5:
			release = 1
		else:
			release = 0

		return [left, right, jump, shoot, release]