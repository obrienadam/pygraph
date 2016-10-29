from math import isinf

class CsrGraph(object):
    def __init__(self):
        self.adj = [0]
        self.xadj = []
        self.vertex_weights = []
        self.edge_weights = []

    def add_vertex(self, w = 1., **kwargs):
        idx = len(self.adj)
        self.adj.append(self.adj[-1])
        self.vertex_weights.append(w)
        return idx

    def connect_vertices(self, vtx0, vtxs = [], weights = []):
        if not isinstance(vtxs, list):
            vtxs = [vtxs]

        if not isinstance(weights, list):
            weights = [weights]

        num_verts = len(vtxs)

        if not weights:
            weights = [1.]*num_verts
        else:
            assert num_verts == len(weights)

        for i in xrange(vtx0 + 1, len(self.adj)):
            self.adj[i] += num_verts

        for vtx, w in zip(vtxs, weights):
            self.xadj.insert(self.adj[vtx0], vtx)
            self.edge_weights.insert(self.adj[vtx0], w)

    def num_verts(self):
        return len(self.adj) - 1

    def num_neighbours(self, vtx):
        return self.adj[vtx + 1] - self.adj[vtx]

    def get_neighbours(self, vtx):
        return self.xadj[self.adj[vtx]:self.adj[vtx + 1]]

    def get_edge_weights(self, vtx):
        return self.edge_weights[self.adj[vtx]:self.adj[vtx + 1]]

    def get_properties(self, vtx):
        return self.properties[vtx]

    def edge_exists(self, vtx0, vtx1):
        return vtx1 in self.get_neighbours(vtx0)

    def get_edge_weight(self, vtx0, vtx1):
        return self.get_edge_weights(vtx0)[self.get_neighbours(vtx0).index(vtx1)]

    def get_path_distance(self, path):
        dist = 0.
        for i in xrange(len(path) - 1):
            dist += self.get_edge_weight(path[i], path[i + 1])

        return dist

    def djikstra_shortest_path(self, vtx0, vtx1):
        distances = [float('inf')]*self.num_verts()
        visited = [False]*self.num_verts()

        path = [[]]*self.num_verts()
        path[vtx0].append(vtx0)
        distances[vtx0] = 0.

        while False in visited:
            current = distances.index(min([distances[i] for i in [j for j in xrange(self.num_verts()) if not visited[j]]]))

            if isinf(distances[current]):
                raise ValueError('No path possible!')

            for nb, w in zip(self.get_neighbours(current), self.get_edge_weights(current)):
                dist = distances[current] + w

                if dist < distances[nb]: # shorter path has been found
                    path[nb] = path[current] + [nb]
                    distances[nb] = dist

            visited[current] = True

        return path[vtx1], self.get_path_distance(path[vtx1])

    def __str__(self):
        return 'adj: {}\nxadj: {}'.format(self.adj, self.xadj)

if __name__ == '__main__':
    from random import random
    from random import randint

    graph = CsrGraph()

    for i in xrange(50):
        graph.add_vertex(w=random())

    for i in xrange(300):
        graph.connect_vertices(randint(0, 49), randint(0, 49), random())

    print graph
    print 'edge weights:', graph.edge_weights

    path = graph.djikstra_shortest_path(1, 36)
    print 'Shortest path between vertices {} and {}:'.format(path[0][0], path[0][-1]), path