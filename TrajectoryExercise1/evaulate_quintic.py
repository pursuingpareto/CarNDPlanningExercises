#!/usr/bin/env python

import numpy as np
from quintic import JMT

TEST_CASES = [
    ([0, 10, 0], [10, 10, 0], 1),
    ([0, 10, 0], [20, 15, 20], 2),
    ([5, 10, 2], [-30, -20, -4], 5),
]

ANSWERS = [[0.0, 10.0, 0.0, 0.0, -0.0, 0.0],
 [0.0,
  10.0,
  0.0,
  -1.2096774193548387,
  0.58467741935483875,
  0.010080645161290322],
 [5.0,
  10.0,
  1.0,
  -1.9244813278008299,
  0.20979253112033192,
  -0.00017925311203319494]
]

def close_enough(poly, target_poly, eps=0.01):
	if type(target_poly) != type(poly):
		target_poly = list(target_poly)
	if len(poly) != len(target_poly):
		print "your solution didn't have the correct number of terms"
		return False
	for term, target_term in zip(poly, target_poly):
		if abs(term-target_term) > eps:
			print "at least one of your terms differed from target by more than {}".format(eps)
			return False
	return True
 
def main():
	for test_case, answer in zip(TEST_CASES, ANSWERS):
		start, end, T = test_case
		jmt = JMT(start, end, T)
		correct = close_enough(jmt, answer)
		if not correct:
			print "try again!"
			return False
	print "Nice work!"
	return True

if __name__ == "__main__":
	main()