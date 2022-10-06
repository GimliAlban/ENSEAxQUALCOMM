import pandas as pd
from math import hypot
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


class Chain:
    """Chain class, contains all the methods to chain a pandas dataframe containing x, y name of pin and macros.
    Main use is by using route method. Return a df having order column.
    """

    class ChainException(Exception):
        """Exception for class classname
        """
        def __init__(self, errmsg: str) -> None:
            """init

            Args:
                errmsg (str): Error message
            """
            self.errmsg = errmsg

    @staticmethod
    def route(df: pd.DataFrame,
              start: int,
              end: int) -> pd.DataFrame:
        """Chain the df (dataframe) from start index to end index. Chain must contain x, y coordinate, pin name and macro name.


        Args:
            df (pd.DataFrame): Pandas dataframe
            start (int): Start index of df
            end (int): End index of df

        Raises:
            Chain.ChainException: Start and End index can't be same.
            Chain.ChainException: Head must contain x, y, pin, macro.

        Returns:
            pd.DataFrame: Dataframe having order column added
        """
        if start == end:
            raise Chain.ChainException("Start chaining index can't be the same as the end")
        for column in {'x', 'y', 'pin', 'macro'}:
            if column not in df.head():
                raise Chain.ChainException(f"{column} not found in dataframe")
        locations: list[tuple[int, int]] = [(x, y) for (x, y) in zip(df['x'], df['y'])]
        data_set = {
            'num_vehicles': 1,
            'locations': locations,
            'depot': 0,
            'starts': [start],
            'ends': [end]
        }
        dist_matrix = Chain.get_dist_matrix(locations)
        path = Chain.solve_routing(data_set, dist_matrix)
        order = [0]*len(path)
        for k, index in enumerate(path):
            order[index] = k
        df['order'] = order
        return df

    @staticmethod
    def solve_routing(data: dict, dist_matrix: dict) -> tuple:
        """Solve routing using ortools

        Args:
            data (dict): dataset
            dist_matrix (dict): distance matrix

        Returns:
            list: list of indexes, by order of routing
        """
        manager = pywrapcp.RoutingIndexManager(
            len(data['locations']),
            data['num_vehicles'],
            data['starts'],
            data['ends'])

        routing = pywrapcp.RoutingModel(manager)

        transit_callback_index = routing.RegisterTransitCallback(
            lambda from_i, to_i:
                dist_matrix[manager.IndexToNode(from_i)][
                    manager.IndexToNode(to_i)])

        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.LOCAL_CHEAPEST_INSERTION)

        solution = routing.SolveWithParameters(search_parameters)
        path: tuple = ()
        index = routing.Start(0)
        while not routing.IsEnd(index):
            path += (manager.IndexToNode(index), )
            index = solution.Value(routing.NextVar(index))
        path += (manager.IndexToNode(index), )
        return path

    @staticmethod
    def get_dist_matrix(locations: list[tuple[int, int]]) -> dict:
        """Compute the euclidian distance matrix

        Args:
            locations (list): List of coordinates from df

        Returns:
            dict: dict of ditances [index_from][index_to] = dist
        """
        distances = {diag: {diag: 0} for diag in range(len(locations))}
        for from_c, from_n in enumerate(locations):
            for to_c, to_n in list(enumerate(locations))[from_c+1:]:
                # Euclidean distance
                val = hypot((from_n[0] - to_n[0]), (from_n[1] - to_n[1]))
                distances[from_c][to_c] = val
                distances[to_c][from_c] = val
        return distances
