import random

class Vertex:
    def __init__(self,value):
        self.value = value
        self.adjacent = {}
        self.neighbors = []
        self.neighbors_weight = []

    def add_adge_to(self, vertex, weight=0):
        self.adjacent[vertex] = weight

    def increment_edge(self, vertex):
        self.adjacent[vertex] = self.adjacent.get(vertex, 0) + 1

    def get_probability_map(self):
        for (vertex, weight) in self.adjacent.items():
            self.neighbors.append(vertex)
            self.neighbors_weight.append(weight)

    def next_word(self):
        return random.choices(self.neighbors, self.neighbors_weight)[0]


class Graph:
    def __init__(self):
        self.vertices = {}

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
