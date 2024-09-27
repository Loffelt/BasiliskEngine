import sys
sys.path.append(sys.path[0] + '/cpp')
import narrow_collisions # type: ignore
from glm import vec3
import time

points1 = [ 3.93571, 1.69435, -2.08957 ,  6.03169, -0.643134, -1.71144 ,  4.78513, 1.95388, -2.54905 ,  5.18226, -0.902661, -1.25196 ,  5.7064, -1.07122, -2.5546 ,  4.85697, -1.33075, -2.09512 ,  3.61041, 1.26627, -2.93274 ,  4.45984, 1.5258, -3.39221 ]

points2 = [ 5.72767, -0.726182, -2.98119 ,  5.72956, 1.23175, -3.7976 ,  4.80673, 0.45541, -2.90558 ,  6.6505, 0.0501548, -3.87321 ,  4.98776, 0.730608, -5.00117 ,  5.9087, -0.450984, -5.07678 ,  4.98587, -1.22732, -4.18477 ,  4.06493, -0.045729, -4.10916 ]

position1 = [            4.80687,     0.292441,     -2.36028 ]
position2 = [    5.35772,    0.0022129,     -3.99118 ]

time1 = time.time()
tup = narrow_collisions.get_narrow_collision(points1, points2, position1, position2)
time2 = time.time()

print(tup)

print(time2 - time1)

# 5.412101745605469e-05

# [vec3( 3.93571, 1.69435, -2.08957 ), vec3( 6.03169, -0.643134, -1.71144 ), vec3( 4.78513, 1.95388, -2.54905 ), vec3( 5.18226, -0.902661, -1.25196 ), vec3( 5.7064, -1.07122, -2.5546 ), vec3( 4.85697, -1.33075, -2.09512 ), vec3( 3.61041, 1.26627, -2.93274 ), vec3( 4.45984, 1.5258, -3.39221 )] 
# [vec3( 5.72767, -0.726182, -2.98119 ), vec3( 5.72956, 1.23175, -3.7976 ), vec3( 4.80673, 0.45541, -2.90558 ), vec3( 6.6505, 0.0501548, -3.87321 ), vec3( 4.98776, 0.730608, -5.00117 ), vec3( 5.9087, -0.450984, -5.07678 ), vec3( 4.98587, -1.22732, -4.18477 ), vec3( 4.06493, -0.045729, -4.10916 )] 
# vec3(      4.80687,     0.292441,     -2.36028 ) 
# vec3(      5.35772,    0.0022129,     -3.99118 ) 

# [(vec3( 0.899664, -1.52663, 0.350983 ), vec3( 5.7064, -1.07122, -2.5546 ), vec3( 4.80673, 0.45541, -2.90558 )), (vec3( -1.26783, 2.25198, -0.411019 ), vec3( 4.45984, 1.5258, -3.39221 ), vec3( 5.72767, -0.726182, -2.98119 )), (vec3( -0.346895, 1.07039, -0.486632 ), vec3( 4.45984, 1.5258, -3.39221 ), vec3( 4.80673, 0.45541, -2.90558 )), (vec3( -2.11915, 0.0345215, 0.864858 ), vec3( 3.61041, 1.26627, -2.93274 ), vec3( 5.72956, 1.23175, -3.7976 )), (vec3( 1.04582, 0.584187, 2.47334 ), vec3( 6.03169, -0.643134, -1.71144 ), vec3( 4.98587, -1.22732, -4.18477 )), (vec3( 0.0502377, -1.78616, 0.810461 ), vec3( 4.85697, -1.33075, -2.09512 ), vec3( 4.80673, 0.45541, -2.90558 ))]

# vec3(    -0.325295,    -0.428086,    -0.843164 ) 0.06493619084358215