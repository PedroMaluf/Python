import random
import numpy as np

class Vertex:
    def __init__(self,value):
        self.value = value
        self.adjacent = {}
        self.neighbors = []
        self.neighbors_weight = []
        self.multiplier_correlateds = []

    #Increment the weight if a word succed the other
    def increment_weight(self, vertex):
        self.adjacent[vertex] = self.adjacent.get(vertex, 0) + 1 

    #Increment the weight based on multiplier that varies for each new word compose
    def multiply_weight(self, vertex, multiplier_correlateds):
        self.adjacent[vertex] = self.adjacent.get(vertex, 0) * (1 + np.mean(multiplier_correlateds))

    def get_probability_map(self):
        self.neighbors = []
        self.neighbors_weight = []
        for (vertex, weight) in self.adjacent.items():
            self.neighbors.append(vertex)
            self.neighbors_weight.append(weight)

    def next_word(self):
        return random.choices(self.neighbors, self.neighbors_weight)[0]


class Graph:
    def __init__(self):
        self.vertices = {}
        self.words_to_multiply = []

    def get_vertex_value(self):
        return set(self.vertices.keys())

    def add_vertex(self, value):
        self.vertices[value] = Vertex(value)

    def get_vertex(self, value):
        if value not in self.vertices:
            self.add_vertex(value)
        return self.vertices[value]

    def get_next_word(self, current_vertex):
        return self.vertices[current_vertex.value].next_word()

    def generate_probability_mapping(self):
        for vertex in self.vertices.values():
            vertex.get_probability_map()
