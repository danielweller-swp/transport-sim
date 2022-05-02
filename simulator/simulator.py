from queue import PriorityQueue
from typing import List

class Location:
    def __init__(self, name: str):
        self.name = name
    
    def __eq__(self, other):
        if (isinstance(other, Location)):
            return self.name == other.name
        return False

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(str(self))

class Road:
    def __init__(self, start: Location, end: Location):
        self.start = start
        self.end = end

    def __eq__(self, other):
        if (isinstance(other, Road)):
            return self.start == other.start and self.end == other.end
        return False

    def __str__(self):
        return f'{str(self.start)} -> {str(self.end)}'

    def __hash__(self):
      return hash(str(self))

class Map:
    def __init__(self, locations: List[Location], roads: List[Road]):
        self.locations = locations
        self.roads = roads

class MovementModel:
    def get_duration_minutes(self, r: Road) -> float:
        pass

    def get_co2_kg(self, r: Road) -> float:
        pass

class DecisionMetric:
    def get_metric(self, r: Road, m: MovementModel) -> float:
        pass

class Route:
  def __init__(self, legs: List[Road]):
    self.legs = legs

  def __str__(self):
    return str([str(leg) for leg in self.legs])

  def __hash__(self):
    return hash(str(self))

  def __eq__(self, other):
    if (isinstance(other, Route)):
        return self.legs == other.legs
    return False

class _Trip:
    def __init__(self, location: Location, parent: '_Trip'):
        self.parent = parent
        self.location = location

    def set_distance(self, distance: float):
        self.distance = distance

    def to_list(self) -> List[Road]:
        if self.parent is None:
            roads = []
        else:
            roads = self.parent.to_list()
            road = Road(self.parent.location, self.location)
            roads.append(road)

        return roads

    def __lt__(self, other: '_Trip'):
      return self.location.name < other.location.name


class RouteResult:
  def __init__(self, route: Route, model: MovementModel):
    self.route = route
    self.model = model

  def get_co2_kg(self):
    return sum([self.model.get_co2_kg(road) for road in self.route.legs])

  def get_duration_minutes(self):
    return sum([self.model.get_duration_minutes(road) for road in self.route.legs])

  def __str__(self):
    route_str = str([ str(leg) for leg in self.route.legs ])
    return f'Route: {route_str}\nDuration: {self.get_duration_minutes():.2f}m\nCO2 emissions: {self.get_co2_kg():.2f}kg'


def simulate(map: Map, start: Location, end: Location, movement_model: MovementModel, decision_metric: DecisionMetric) -> RouteResult:
    queue = PriorityQueue()
    queue.put((0, _Trip(start, None)))

    visited = []

    while not queue.empty():
        (clock, trip) = queue.get()

        if trip.location in visited:
            continue

        if trip.location == end:
            return RouteResult(Route(trip.to_list()), movement_model)

        visited.append(trip.location)

        roads = [ (road.end, road) for road in map.roads if road.start == trip.location ]

        for destination, road in roads:
            if destination in visited:
                continue

            metric = decision_metric.get_metric(road, movement_model)
            total_metric = clock + metric
            next_hop = _Trip(destination, trip)
            queue.put((total_metric, next_hop))

