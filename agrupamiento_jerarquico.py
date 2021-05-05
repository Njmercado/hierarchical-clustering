from bokeh.plotting import figure, show
from random import randint
from random import uniform
from math import sqrt
from math import pow
from functools import reduce

class Coordinate:
    
    def __init__(self):
        self._coordinate = (0.0,0.0)

    @property
    def coordinate(self):
        return self._coordinate

    @coordinate.setter
    def coordinate(self, coordinate):
        self._coordinate = coordinate
    
    def distanceTo(self, coordinate):
        x_1, y_1 = self._coordinate
        x_2, y_2 = coordinate.coordinate
        return sqrt(pow(x_1-x_2, 2)+pow(y_1-y_2, 2))

class Cluster:
    
    def __init__(self):
        self._list_of_coordinates = []

    def add(self, coordinate):
        self._list_of_coordinates.append(coordinate)

    @property
    def coordinates(self):
        return self._list_of_coordinates

    @coordinates.setter
    def coordinates(self, coordinates):
        self._list_of_coordinates = coordinates

    def join(self, cluster):
        """
            description: This function is used to unify two clusters
        """
        for coordinate in cluster.coordinates:
            self.add(coordinate)

    def distanceTo(self, cluster):
        """
            description: This function is used to find the mininum distance between 2 clusters,
            which is the current distance.
        """
        minimun_distance = 9999999999
        for local_coordinate in self._list_of_coordinates:
            for foreign_coordinate in cluster.coordinates:
                distance = local_coordinate.distanceTo(foreign_coordinate)
                if distance < minimun_distance:
                    minimun_distance = distance
        return minimun_distance
    
    def asListOfPoints(self):
        list_of_points = []
        for coordinate in self._list_of_coordinates:
            list_of_points.append(coordinate.coordinate)
        return list_of_points


class HierarchicalClustering:

    def __init__(self):
        self._list_of_clusters = []

    @property
    def clusters(self):
        return self._list_of_clusters

    @clusters.setter
    def clusters(self, list_of_clusters):
        self._list_of_clusters = list_of_clusters

    def _nearestClusters(self):
        nearest_clusters = []
        minimun_distance = 9999999999
        for index, cluster in enumerate(self._list_of_clusters[:-1]):
            for index_2, cluster_2 in enumerate(self._list_of_clusters[index+1:]):
                distance = cluster.distanceTo(cluster_2)
                if distance < minimun_distance:
                    minimun_distance = distance
                    nearest_clusters = [(cluster, index), (cluster_2, index + index_2 + 1)]
        return nearest_clusters

    def apply(self, max_number_of_clusters = 1):
        number_of_clusters = len(self._list_of_clusters)
        print("applying algorithm...")
        while number_of_clusters > max_number_of_clusters:
            # print("=========================================================\n\n")
            # index = 1
            # for cluster in self._list_of_clusters:
            #     points = cluster.asListOfPoints()
            #     print("-----------------------------------------------\n")
            #     print(f"Cluster {index} with {len(points)} elements, which are {points}")
            #     index += 1
            nearest_clusters = self._nearestClusters()
            cluster_1, index_1 = nearest_clusters[0]
            cluster_2, index_2 = nearest_clusters[1]
            cluster_1.join(cluster_2)
            self._list_of_clusters[index_1] = cluster_1
            # Deleted those clusters which were joined before
            del self._list_of_clusters[index_2]
            number_of_clusters -= 1

def generateRandomCoordinates(number_of_points):
    list_of_coordinates = []
    for _ in range(number_of_points):
        coordinate = Coordinate()
        coordinate.coordinate = (randint(0, 1000), randint(0, 1000))
        list_of_coordinates.append(coordinate)
    return list_of_coordinates

def createListOfClusters(list_of_coordinates):
    list_of_clusters = []
    for coordinate in list_of_coordinates:
        cluster = Cluster()
        cluster.coordinates = [coordinate]
        list_of_clusters.append(cluster)
    return list_of_clusters

def main(number_of_points=10, number_of_clusters = 2):
    random_coordinates = generateRandomCoordinates(number_of_points)
    list_of_clusters = createListOfClusters(random_coordinates)
    hierarchical_clustering = HierarchicalClustering()
    hierarchical_clustering.clusters = list_of_clusters
    hierarchical_clustering.apply(number_of_clusters)

    p = figure()
    index = 0
    colors = ["red", "blue", "green", "gray", "yellow", "purple"]

    for cluster in hierarchical_clustering.clusters:
        points = cluster.asListOfPoints()
        print("-----------------------------\n")
        print(f"Final points cluster {index+1} -> {points} ")
        xs = [i[0] for i in points]
        ys = [i[1] for i in points]
        p.circle(xs, ys, size=10, color=colors[index], alpha=0.5)
        index += 1
    
    show(p)

if __name__ == "__main__":
    number_of_points = int(input("Number of points: "))
    number_of_clusters = int(input("Number of clusters: "))
    main(number_of_points, number_of_clusters)
