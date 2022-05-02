from simulator import Location, Map, Road, MovementModel, simulate
from data import generate_map_from_data, generate_mean_movement_model_from_data, load_data, generate_random_movement_model_from_data
from monte_carlo import simulate_monte_carlo

class DurationDecisionMetric:
   def get_metric(self, r: Road, m: MovementModel) -> float:
      return m.get_duration_minutes(r)

vienna = Location('Vienna')
innsbruck = Location('Innsbruck')


historical_data = load_data('sample_data.csv')
map = generate_map_from_data(historical_data)

movement_model = generate_mean_movement_model_from_data(historical_data)

route_result = simulate(map, vienna, innsbruck, movement_model, DurationDecisionMetric())
print(route_result)

monte_carlo_result = simulate_monte_carlo(map, vienna, innsbruck, historical_data, DurationDecisionMetric(), 1000)

print(monte_carlo_result)
