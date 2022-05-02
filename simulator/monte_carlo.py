from typing import Dict, List
from .data import RoadData, generate_random_movement_model_from_data
from .simulator import DecisionMetric, Location, Map, Road, MovementModel, Route, RouteResult, simulate

class MonteCarloResult:
  def __init__(self):
      self.route_results = []

  def add_route_result(self, route_result: RouteResult):
      self.route_results.append(route_result)

  def route_counts(self) -> Dict[Route, int]:
      route_counts = {}
      for route_result in self.route_results:
          route = route_result.route
          if route in route_counts:
            n = route_counts[route]
          else:
            n = 0
          route_counts[route] = n + 1
      return route_counts

  def routes_with_co2_kg(self):
    return [(route_result.route, route_result.get_co2_kg()) for route_result in self.route_results]

  def average_co2_kg(self):
    total_co2_kg = sum([co2 for (_, co2) in self.routes_with_co2_kg()])
    return total_co2_kg / len(self.route_results)

  def routes_with_duration_minutes(self):
    return [(route_result.route, route_result.get_duration_minutes()) for route_result in self.route_results]

  def average_duration_minutes(self):
    total_duration_minutes = sum([duration for (_, duration) in self.routes_with_duration_minutes()])
    return total_duration_minutes / len(self.route_results)


  def routes_with_duration(self):
    return [(route_result.route, route_result.get_duration_minutes()) for route_result in self.route_results]

  def __str__(self):
    route_counts = self.route_counts()
    route_counts_str = "\n".join([ f'{str(route)}: {count}' for route, count in route_counts.items() ])

    result = f"Chosen routes:\n{route_counts_str}\nAverage Duration: {self.average_duration_minutes():.2f}m\nAverage CO2 emissions: {self.average_co2_kg():.2f}kg"
    return result

def simulate_monte_carlo(map: Map, start: Location, end: Location, historical_data: Dict[Road, List[RoadData]], decision_metric: DecisionMetric, n: int) -> MonteCarloResult:
    result = MonteCarloResult()

    for _ in range(n):
        movement_model = generate_random_movement_model_from_data(historical_data)
        route_result = simulate(map, start, end, movement_model, decision_metric)
        result.add_route_result(route_result)

    return result