from functools import partial
from six.moves import xrange

from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

def create_data_model():
    data = {}
    # km
    _locations = [
        (4, 4),  # depot
        (8, 0),  # locations to visit
        (2, 0),
    ]
    # 转换成 m
    data['locations'] = [(l[0] * 1000, l[1] * 1000) for l in _locations]
    data['num_locations'] = len(data['locations'])
    
    # 吨
    _demands = [0, # depot
           1, 1] # 1, 2
    
    # 千克
    data['demands'] = [l * 1000 for l in _demands]

    # 车的数量及最大载重
    _capacity = [3000]
    data['vehicle_capacity'] = [l * 1000 for l in _capacity]
    data['num_vehicles'] = len(data['vehicle_capacity'])

    # 每个配送点下货所需时间（分钟）
    data['time_per_location'] = 5

    # 每个配送点的时间窗口（分钟）
    data['time_windows'] = \
          [(0, 0), # depot
           (0, 10000), (0, 8500)]

    # 速度（m/min）
    data['vehicle_speed'] = 10 * 60 / 3.6
    
    data['depot'] = 0
    
    # 最大里程（m）
    data['max_dis_per_vehicle'] = 35 * 1000;

    # 最大工作时间
    data['max_time_per_vehicle'] = 8 * 60

    return data


# 计算两点曼哈顿距离
def manhattan_distance(position_1, position_2):
    return (abs(position_1[0] - position_2[0]) +
            abs(position_1[1] - position_2[1]))


def create_distance_evaluator(data):
    _distances = {}
    # 预处理距离矩阵
    for from_node in xrange(data['num_locations']):
        _distances[from_node] = {}
        for to_node in xrange(data['num_locations']):
            if from_node == to_node:
                _distances[from_node][to_node] = 0
            else:
                _distances[from_node][to_node] = (manhattan_distance(
                    data['locations'][from_node], data['locations'][to_node]))


    def distance_evaluator(manager, from_node, to_node):
        """Returns the manhattan distance between the two nodes"""
        return _distances[manager.IndexToNode(from_node)][manager.IndexToNode(
            to_node)]

    return distance_evaluator


def add_distance_dimension(routing, distance_evaluator_index, data):
    distance = 'Distance'
    routing.AddDimension(
        distance_evaluator_index,
        0,  # null slack
        data['max_dis_per_vehicle'],  # 车辆最大里程
        True,
        distance)
    distance_dimension = routing.GetDimensionOrDie(distance)
    # 使最长里程尽可能短
    distance_dimension.SetGlobalSpanCostCoefficient(100)


def create_demand_evaluator(data):
    _demands = data['demands']

    def demand_evaluator(manager, from_node):
        """Returns the demand of the current node"""
        return _demands[manager.IndexToNode(from_node)]

    return demand_evaluator


def add_capacity_constraints(routing, manager, data, demand_evaluator_index):
    routing.AddDimensionWithVehicleCapacity(
        demand_evaluator_index,
        0,  # Null slack
        data['vehicle_capacity'],
        True,  # start cumul to zero
        'Capacity')


def create_time_evaluator(data):
    def service_time(data, node):
        # 每个服务点的下货时间
        return data['time_per_location']

    def travel_time(data, from_node, to_node):
        # 路径的用时
        if from_node == to_node:
            travel_time = 0
        else:
            travel_time = manhattan_distance(data['locations'][
                from_node], data['locations'][to_node]) / data['vehicle_speed']
        return travel_time

    # 时间矩阵
    _total_time = {}
    for from_node in xrange(data['num_locations']):
        _total_time[from_node] = {}
        for to_node in xrange(data['num_locations']):
            if from_node == to_node:
                _total_time[from_node][to_node] = 0
            else:
                _total_time[from_node][to_node] = int(
                    service_time(data, from_node) + travel_time(
                        data, from_node, to_node))

    def time_evaluator(manager, from_node, to_node):
        return _total_time[manager.IndexToNode(from_node)][manager.IndexToNode(
            to_node)]

    return time_evaluator
    

def add_time_window_constraints(routing, manager, data, time_evaluator):
    time = 'Time'
    routing.AddDimension(
        time_evaluator,
        data['max_time_per_vehicle'],  # allow waiting time
        data['max_time_per_vehicle'],  # maximum time per vehicle
        False,  # don't force start cumul to zero since we are giving TW to start nodes
        time)
    time_dimension = routing.GetDimensionOrDie(time)

    # 对各个 location 加入时间窗口
    for location_idx, time_window in enumerate(data['time_windows']):
        if location_idx == 0:
            continue
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
        routing.AddToAssignment(time_dimension.SlackVar(index))

    for vehicle_id in xrange(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        time_dimension.CumulVar(index).SetRange(data['time_windows'][0][0],
                                                data['time_windows'][0][1])
        routing.AddToAssignment(time_dimension.SlackVar(index))

    # 选择性加入，让车尽早出发
    # for i in range(data['num_vehicles']):
    # routing.AddVariableMinimizedByFinalizer(
    #     time_dimension.CumulVar(routing.Start(i)))
    # routing.AddVariableMinimizedByFinalizer(
    #     time_dimension.CumulVar(routing.End(i)))

def print_solution(data, manager, routing, assignment):  # pylint:disable=too-many-locals
    """Prints assignment on console"""
    print('Objective: {}'.format(assignment.ObjectiveValue()))
    total_distance = 0
    total_load = 0
    total_time = 0
    capacity_dimension = routing.GetDimensionOrDie('Capacity')
    time_dimension = routing.GetDimensionOrDie('Time')
    dropped = []
    for order in xrange(0, routing.nodes()):
        index = manager.NodeToIndex(order)
        if assignment.Value(routing.NextVar(index)) == index:
            dropped.append(order)
    print('dropped orders: {}'.format(dropped))

    for vehicle_id in xrange(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        distance = 0
        while not routing.IsEnd(index):
            load_var = capacity_dimension.CumulVar(index)
            time_var = time_dimension.CumulVar(index)
            plan_output += ' {0} Load({1}) Time({2},{3}) ->'.format(
                manager.IndexToNode(index),
                assignment.Value(load_var),
                assignment.Min(time_var), assignment.Max(time_var))
            previous_index = index
            index = assignment.Value(routing.NextVar(index))
            distance += routing.GetArcCostForVehicle(previous_index, index,
                                                     vehicle_id)
        load_var = capacity_dimension.CumulVar(index)
        time_var = time_dimension.CumulVar(index)
        plan_output += ' {0} Load({1}) Time({2},{3})\n'.format(
            manager.IndexToNode(index),
            assignment.Value(load_var),
            assignment.Min(time_var), assignment.Max(time_var))
        plan_output += 'Distance of the route: {}m\n'.format(distance)
        plan_output += 'Load of the route: {}\n'.format(
            assignment.Value(load_var))
        plan_output += 'Time of the route: {}min\n'.format(
            assignment.Value(time_var))
        print(plan_output)
        total_distance += distance
        total_load += assignment.Value(load_var)
        total_time += assignment.Value(time_var)
    print('Total Distance of all routes: {}m'.format(total_distance))
    print('Total Load of all routes: {}'.format(total_load))
    print('Total Time of all routes: {}min'.format(total_time))


def main():
    data = create_data_model()
    manager = pywrapcp.RoutingIndexManager(data['num_locations'],
                                           data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    # distance dimension
    distance_evaluator_index = routing.RegisterTransitCallback(
        partial(create_distance_evaluator(data), manager))
    routing.SetArcCostEvaluatorOfAllVehicles(distance_evaluator_index)
    add_distance_dimension(routing, distance_evaluator_index, data)

    # capacity constraint
    demand_evaluator_index = routing.RegisterUnaryTransitCallback(
        partial(create_demand_evaluator(data), manager))
    add_capacity_constraints(routing, manager, data, demand_evaluator_index)

    # Time Window constraint
    time_evaluator_index = routing.RegisterTransitCallback(
        partial(create_time_evaluator(data), manager))
    add_time_window_constraints(routing, manager, data, time_evaluator_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)  # pylint: disable=no-member
    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)
    if assignment:
        print_solution(data, manager, routing, assignment)
    
if __name__ == '__main__':
    main()