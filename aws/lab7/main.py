from typing import Callable, List
import math


class DistanceFuncs:
    def calc_distance(self, point_a: List[float], point_b: List[float], dist_func: Callable) -> float:
        """ Calculates distance between two points using the passed dist_func """
        return dist_func(point_a, point_b)

    @staticmethod
    def euclidean(point_a: List[float], point_b: List[float]) -> float:
        """
        Calculates Euclidean Distance between two points Example:
        >>>DistanceFuncs.euclidean([1,1],[1,1])
        0.0
        """
        return math.dist(point_a, point_b)

    @staticmethod
    def manhattan_distance(point_a: List[float], point_b: List[float]):
        """Compute
        the manhattan_distance between two points"""
        return sum(abs(val1-val2) for val1, val2 in zip(point_a, point_b))

    @staticmethod
    def jaccard_distance(point_a: List[float], point_b: List[float]):
        """Compute
        the jaccard_distance between two points"""
        intersect = set(point_a) & set(point_b)
        return 1 - len(intersect) / len(point_a) + len(point_b) - len(intersect)


def main():

    point_a = [1, 2, 3, 4]
    point_b = [3, 5, 2, 1]

    dist_funcs = DistanceFuncs()
    print('euclidean distance: ', dist_funcs.calc_distance(
        point_a, point_b, DistanceFuncs.euclidean))
    print('manhattan distance: ', dist_funcs.calc_distance(point_a, point_b,
                                                           DistanceFuncs.manhattan_distance))
    print('jaccard distance: ', dist_funcs.calc_distance(point_a, point_b,
                                                         DistanceFuncs.jaccard_distance))


if __name__ == "__main__":
    main()
