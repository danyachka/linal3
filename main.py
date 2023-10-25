import sympy as s
import utils as u


def firstTask():
    mesh = u.generateCube()
    u.drawPlot([mesh], "Задание №1")


def secondTask():
    scale = 1.5
    mesh = u.generateCube()
    newMesh = u.generateCube(color=u.Color.pink)

    m: s.Matrix = scale * s.eye(4)
    m[3, 3] = 1

    newMesh.getNewPoints(m)
    u.drawPlot([mesh, newMesh], "Задание №2")


def thirdTask():
    mesh = u.generateCube()
    newMesh = u.generateCube(color=u.Color.pink)

    m: s.Matrix = u.getMovingMatrix(-3, 0, 0)
    newMesh.getNewPoints(m)

    u.drawPlot([mesh, newMesh], "Задание №3")


# В трёх плоскостях
# На вики
def fourthTask():
    matrixZ: s.Matrix = u.getRotationMatrix(z=45)

    meshZ = u.generateCube(color=u.Color.red)
    meshZ.getNewPoints(matrixZ)

    u.drawPlot([meshZ], "Задание №4")


def fifthTask():
    rotationMatrix: s.Matrix = u.getRotationMatrix(y=-45, z=270)

    mesh = u.generateCube()
    newMesh = u.generateCube(color=u.Color.red)

    pnt = list(newMesh.points[2])
    print(pnt)
    movingMatrix: s.Matrix = u.getMovingMatrix(pnt[0], pnt[1], pnt[2])
    print(movingMatrix)

    finalMatrix: s.Matrix = movingMatrix.inv() * rotationMatrix * movingMatrix

    newMesh.getNewPoints(finalMatrix)

    u.drawPlot([mesh, newMesh], "Задание №4")


if __name__ == "__main__":
    firstTask()
    secondTask()
    thirdTask()
    fourthTask()
    fifthTask()
