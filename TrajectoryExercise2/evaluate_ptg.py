from ptg import PTG

left_lane_slow = [
	(0,0,0),
	(5,0,1),
	(10,0,2),
	(15,0,3),
	(20,0,4),
	(25,0,5)
]

right_lane_slow = [
	(0,4,0),
	(5,4,1),
	(10,4,2),
	(15,4,3),
	(20,4,4),
	(25,4,5)
]

left_lane_fast = [
	(0,0,0),
	(10,0,1),
	(20,0,2),
	(30,0,3),
	(40,0,4),
	(50,0,5)
]

right_lane_fast = [
	(0,4,0),
	(10,4,1),
	(20,4,2),
	(30,4,3),
	(40,4,4),
	(50,4,5)
]

left_to_right = [
	(0,0,0),
	(5,1,1),
	(10,2,2),
	(15,3,3),
	(20,4,4),
	(25,4,5)
]

start_right = (-4,4,0)
start_left  = (-4,0,0)
end_right_slow   = (25,4,5)
end_right_fast   = (50,4,5)
end_left_slow   = (25,0,5)
end_left_fast   = (50,0,5)

TEST_CASES = [
	(start_right, end_left_fast, 5, ())
]