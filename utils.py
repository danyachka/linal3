from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
from typing import Final
from enum import Enum
import math
import numpy as np
import sympy as s
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

SPACE_LIMIT: Final[float] = 5

FACES = [(1, 0, 2, 3),
         (1, 0, 4, 5),
         (7, 6, 2, 3),
         (5, 4, 6, 7),
         (1, 5, 7, 3),
         (0, 4, 6, 2)
         ]

VERTICES = [
    s.Matrix([[-1, -1, -1, 1]]).T,
    s.Matrix([[-1, -1, 1, 1]]).T,
    s.Matrix([[-1, 1, -1, 1]]).T,
    s.Matrix([[-1, 1, 1, 1]]).T,
    s.Matrix([[1, -1, -1, 1]]).T,
    s.Matrix([[1, -1, 1, 1]]).T,
    s.Matrix([[1, 1, -1, 1]]).T,
    s.Matrix([[1, 1, 1, 1]]).T
]


class Color(Enum):
    red = "Red"
    green = "Green"
    blue = "Blue"
    pink = "Pink"
    black = "Black"


class Mesh:
    points: [s.Matrix]
    color: Color
    name: str
    faces: [(float, float)]

    def __init__(self, points: [s.Matrix], color: Color, name: str, faces=None):
        if faces is None:
            faces = FACES
        self.points = points
        self.color = color
        self.faces = faces
        if name is None:
            name = "Mesh"
        self.name = name

    def generatePolygons(self) -> [[]]:
        faces = []
        for face in self.faces:
            plane = []
            for pointIndex in face:
                v = self.points[pointIndex]
                plane.append([v[0, 0], v[1, 0], v[2, 0]])
            faces.append(plane)
        return faces

    def updatePoints(self, m: s.Matrix):
        points = []

        for i in range(len(self.points)):
            v = m * self.points[i]
            points.append(v)

        self.points = points

    def printPoints(self):
        print(self.name + " coordinates are:")
        for v in self.points:
            print(list(v))

    def moveTo(self, coords):
        T: s.Matrix = getMovingMatrix(coords[0], coords[1], coords[2])
        self.updatePoints(T)


class CameraPosition:
    elev: float
    azim: float
    dist: float

    def __init__(self, elev=30, azim=45, dist=10):
        self.elev = elev
        self.azim = azim
        self.dist = dist


def drawPlot(meshes: [Mesh], screenName: str, cameraPosition: CameraPosition = None):
    fig = plt.figure(figure=(7, 7))
    # ax = plt.axes(projection="3d")
    # ax = Axes3D(fig)
    ax = fig.add_subplot(111, projection="3d")

    if cameraPosition is not None:
        ax.view_init(cameraPosition.elev, cameraPosition.azim)
        ax.dist = cameraPosition.dist

    legend = []
    # Create mesh
    for mesh in meshes:
        drawMesh(ax, mesh)

        if mesh.name != "":
            legend.append(mesh.name)

    ax.set_xlim([-SPACE_LIMIT, SPACE_LIMIT])
    ax.set_ylim([-SPACE_LIMIT, SPACE_LIMIT])
    ax.set_zlim([-SPACE_LIMIT, SPACE_LIMIT])

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.gca().legend(legend)
    ax.grid()

    ax.set_title(screenName)

    plt.show()


def getRotationMatrix(x=None, y=None, z=None) -> s.Matrix:
    rotations: [s.Matrix] = []

    if x is not None and x != 0:
        x = x * s.pi / 180
        sin = s.sin(x)
        cos = s.cos(x)
        xR: s.Matrix = s.Matrix([[1, 0, 0, 0],
                                 [0, cos, -sin, 0],
                                 [0, sin, cos, 0],
                                 [0, 0, 0, 1]])
        rotations.append(xR)

    if y is not None and y != 0:
        y = y * s.pi / 180
        sin = s.sin(y)
        cos = s.cos(y)
        yR: s.Matrix = s.Matrix([[cos, 0, sin, 0],
                                 [0, 1, 0, 0],
                                 [-sin, 0, cos, 0],
                                 [0, 0, 0, 1]])
        rotations.append(yR)

    if z is not None and z != 0:
        z = z * s.pi / 180
        sin = s.sin(z)
        cos = s.cos(z)
        zR: s.Matrix = s.Matrix([[cos, -sin, 0, 0],
                                 [sin, cos, 0, 0],
                                 [0, 0, 1, 0],
                                 [0, 0, 0, 1]])
        rotations.append(zR)

    size = len(rotations)
    if size == 0:
        raise Exception("No angles given")

    m = s.eye(4)
    for v in rotations:
        m = m * v

    return m


def getMovingMatrix(x, y, z) -> s.Matrix:
    v = [x, y, z]

    m: s.Matrix = s.eye(4)
    for i in range(3):
        m[i, 3] = v[i]

    return m


def getPerspectiveMatrix(U, V, N, C) -> s.Matrix:
    T: s.Matrix = s.eye(4)
    vectors = [U, V, N]
    array = [list(U), list(V), list(N)]

    for i in range(3):
        for j in range(3):
            T[j, i] = array[i][j]

        T[3, i] = -vectors[i].T * C

    return T


def generateCube(name: str = "КУБ", color: Color = Color.blue, scale=1) -> Mesh:
    m: s.Matrix = s.eye(4) * scale
    m[3, 3] = 1
    mesh = Mesh(VERTICES, color, name, FACES)

    mesh.updatePoints(m)
    return mesh


def generateThreeCubes() -> [s.Matrix]:
    greenMesh = generateCube("green", color=Color.green)
    blueMesh = generateCube("blue", color=Color.blue)
    pinkMesh = generateCube("pink", color=Color.pink)

    x45 = getRotationMatrix(x=45)
    greenMesh.updatePoints(x45)

    moveY = getMovingMatrix(0, -3, 0)
    blueMesh.updatePoints(moveY)

    moveYBack = getMovingMatrix(0, 3, 0)
    z45 = getRotationMatrix(z=45)
    pinkMesh.updatePoints(z45)
    pinkMesh.updatePoints(moveYBack)

    return [blueMesh, greenMesh, pinkMesh]


def drawMesh(ax, mesh: Mesh):
    faces = mesh.generatePolygons()
    ax.add_collection3d(Poly3DCollection(faces, alpha=0.9, linewidths=1, edgecolors=Color.black.value,
                                         facecolors=mesh.color.value))
