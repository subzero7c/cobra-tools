from generated.base_enum import UintEnum


class CollisionType(UintEnum):
	Sphere = 0
	BoundingBox = 1
	Capsule = 2
	HitcheckHeroTree = 3
	ConvexHull = 8
	# widgetball_test.mdl2, Ball_Hitcheck not supported
	Unknown = 10
