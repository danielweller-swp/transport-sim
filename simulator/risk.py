from statistics import stdev
from math import sqrt
from scipy import stats

def probability_for_radius(sample, radius):
  n = len(sample)
  s = stdev(sample)
  return 2*stats.t(df=n-1).cdf(radius/(s*sqrt(1+1/n)))-1

def risk(transport_duration_sample, acceptable_deviation):
  return 1 - probability_for_radius(transport_duration_sample, acceptable_deviation)