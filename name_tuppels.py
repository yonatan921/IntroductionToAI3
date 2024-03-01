from collections import namedtuple

Point = namedtuple("Point", "x, y")
VPackage = namedtuple("VPackage", "point, f, prob")
Edge = namedtuple("Edge", "v1 ,v2,prob")

