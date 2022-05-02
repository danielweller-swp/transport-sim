import unittest
from .simulator import Location, Map, MovementModel, Road, Route, simulate

class DurationDecisionMetric:
   def get_metric(self, r: Road, m: MovementModel) -> float:
      return m.get_duration_minutes(r)

class ConstantMovementModel(MovementModel):
   def get_duration_minutes(self, r: Road) -> float:
      return 1

   def get_co2_kg(self, r: Road) -> float:
       return 1

class SimulatorTest(unittest.TestCase):
    def test_route_found(self):
        vienna = Location('Vienna')
        liezen = Location('Liezen')
        innsbruck = Location('Innsbruck')
        locations = [ vienna, liezen, innsbruck ]

        vienna_to_liezen = Road(vienna, liezen)
        liezen_to_innsbruck = Road(liezen, innsbruck)

        roads = [ vienna_to_liezen, liezen_to_innsbruck ]

        map = Map(locations, roads)

        route_result = simulate(map, vienna, innsbruck, ConstantMovementModel(), DurationDecisionMetric())

        expected_route = Route([vienna_to_liezen, liezen_to_innsbruck])

        self.assertEqual(route_result.route, expected_route)