import csv
import random
from statistics import mean
from typing import Dict, List

from .simulator import Map, Road, Location, MovementModel
from .copert_co2 import get_co2_emissions_kg_per_100km

class RoadData:
    def __init__(self, duration_minutes: float, average_speed_kmh: float):
        self.duration_minutes = duration_minutes
        self.average_speed_kmh = average_speed_kmh

def load_data(file: str) -> Dict[Road, List[RoadData]]:
    result = {}

    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            start = Location(row['FROM'])
            end = Location(row['TO'])
            road = Road(start, end)
            if road in result:
              road_datas = result[road]
            else:
              road_datas = []
            road_datas.append(RoadData(float(row['DURATION_MINUTES']), float(row['AVERAGE_SPEED_KMH'])))
            result[road] = road_datas

    return result

class ConstantDataMovementModel(MovementModel):
    def __init__(self, road_data: Dict[Road, RoadData]):
      self.road_data = road_data

    def get_duration_minutes(self, r: Road) -> float:
      return self.road_data[r].duration_minutes
   
    def get_co2_kg(self, r: Road) -> float:
      road_data = self.road_data[r]
      duration_hours = road_data.duration_minutes / 60
      distance_km = road_data.average_speed_kmh * duration_hours
      co2_per_km = get_co2_emissions_kg_per_100km(road_data.average_speed_kmh) / 100

      return co2_per_km * distance_km

def generate_map_from_data(road_datas: Dict[Road, List[RoadData]]):
  locations_from = [ road.start for road in road_datas.keys()]
  locations_to = [ road.end for road in road_datas.keys()]
  locations = set(locations_from + locations_to)

  return Map(locations, road_datas.keys())

def generate_random_movement_model_from_data(road_datas: Dict[Road, List[RoadData]]):
  road_data = { road : random.choice(road_datas[road]) for road in road_datas.keys()}
  return ConstantDataMovementModel(road_data)

def get_mean_road_data(road_datas: List[RoadData]):
  mean_duration_minutes = mean([ road_data.duration_minutes for road_data in road_datas])
  mean_average_speed_kmh = mean([ road_data.average_speed_kmh for road_data in road_datas])

  return RoadData(mean_duration_minutes, mean_average_speed_kmh)

def generate_mean_movement_model_from_data(road_datas: Dict[Road, List[RoadData]]):
  road_data = { road : get_mean_road_data(road_datas[road]) for road in road_datas.keys()}
  return ConstantDataMovementModel(road_data)