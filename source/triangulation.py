import pygame
import math


def circum_center(a, b, c):
    ad = a[0] * a[0] + a[1] * a[1]
    bd = b[0] * b[0] + b[1] * b[1]
    cd = c[0] * c[0] + c[1] * c[1]
    D = 2 * (a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1]))
    return pygame.Vector2((1 / D * (ad * (b[1] - c[1]) + bd * (c[1] - a[1]) + cd * (a[1] - b[1])),
                           1 / D * (ad * (c[0] - b[0]) + bd * (a[0] - c[0]) + cd * (b[0] - a[0]))))


def line_is_equal(line1, line2):
    if (line1[0] == line2[0] and line1[1] == line2[1]) or (line1[0] == line2[1] and line1[1] == line2[0]):
        return True
    return False


def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


class Triangle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.edges = [[self.a, self.b],
                      [self.b, self.c],
                      [self.c, self.a]]
        self.circum_center = circum_center(a, b, c)

    def is_point_in_circum_circle(self, point):
        if self.a.distance_to(self.circum_center) > point.distance_to(self.circum_center):
            return True
        return False

    def has_vertex(self, point):
        if (self.a == point) or (self.b == point) or (self.c == point):
            return True
        return False

    def show(self, screen, colour):
        for edge in self.edges:
            pygame.draw.aaline(screen, colour, edge[0], edge[1])


def delaunay_triangulation(points, width, height):
    triangulation = []
    superTriangleA = pygame.Vector2(-100, -100)
    superTriangleB = pygame.Vector2(2 * width + 100, -100)
    superTriangleC = pygame.Vector2(-100, 2 * height + 100)
    superTriangle = Triangle(superTriangleA, superTriangleB, superTriangleC)
    triangulation.append(superTriangle)

    for point in points:

        badTriangles = []
        for triangle in triangulation:
            if triangle.is_point_in_circum_circle(point):
                badTriangles.append(triangle)

        polygon = []
        for triangle in badTriangles:
            for triangleEdge in triangle.edges:
                isShared = False
                for other in badTriangles:
                    if triangle == other:
                        continue
                    for otherEdge in other.edges:
                        if line_is_equal(triangleEdge, otherEdge):
                            isShared = True
                if not isShared:
                    polygon.append(triangleEdge)

        for badTriangle in badTriangles:
            triangulation.remove(badTriangle)

        for edge in polygon:
            newTriangle = Triangle(edge[0], edge[1], point)
            triangulation.append(newTriangle)

    for i in range(len(triangulation)-1, -1, -1):
        triangle = triangulation[i]
        if triangle.has_vertex(superTriangleA) and triangle in triangulation:
            triangulation.remove(triangle)
        if triangle.has_vertex(superTriangleB) and triangle in triangulation:
            triangulation.remove(triangle)
        if triangle.has_vertex(superTriangleC) and triangle in triangulation:
            triangulation.remove(triangle)

    return triangulation


def get_lines_from_triangulation(points, width, height):
    triangles = delaunay_triangulation(points, width, height)
    lines = []
    for triangle in triangles:
        line = []
        for edge in triangle.edges:
            line.extend([(point.x, point.y) for point in edge])
        if line in lines:
            continue
        lines.extend(line)
    return lines
