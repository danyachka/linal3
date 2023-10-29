import random

from ipywidgets import interact
import ipywidgets as widgets
import matplotlib
import sympy as s
import utils


def firstTask():
    mesh = utils.generateCube()
    utils.drawPlot([mesh], "Задание №1")


def secondTask():
    scale = 1.5
    mesh = utils.generateCube()
    newMesh = utils.generateCube(color=utils.Color.pink)

    m: s.Matrix = scale * s.eye(4)
    m[3, 3] = 1

    newMesh.updatePoints(m)
    utils.drawPlot([mesh, newMesh], "Задание №2")


def thirdTask():
    mesh = utils.generateCube()
    newMesh = utils.generateCube(color=utils.Color.pink, name="Moved")

    m: s.Matrix = utils.getMovingMatrix(-3, 0, 0)
    newMesh.updatePoints(m)

    scaledMesh = utils.generateCube(color=utils.Color.pink, name="Moved and scaled cube")
    m: s.Matrix = utils.getMovingMatrix(0, 3, 0)
    scaledMesh.updatePoints(m)
    scale = 1.5
    sm: s.Matrix = scale * s.eye(4)
    sm[3, 3] = 1
    scaledMesh.updatePoints(sm)
    scaledMesh.printPoints()

    camera = utils.CameraPosition(0, 0, 10)

    utils.drawPlot([mesh, newMesh, scaledMesh], "Задание №3")
    utils.drawPlot([mesh, newMesh, scaledMesh], "Задание №3", cameraPosition=camera)


# В трёх плоскостях
# На вики
def fourthTask():
    matrix: s.Matrix = utils.getRotationMatrix(z=45)

    mesh = utils.generateCube(color=utils.Color.pink, name="Rotated cube")
    mesh.updatePoints(matrix)

    utils.drawPlot([mesh], "Задание №4")


def fifthTask():
    rotationMatrix: s.Matrix = utils.getRotationMatrix(x=45, z=135)

    mesh = utils.generateCube()
    newMesh = utils.generateCube(color=utils.Color.pink)

    pnt = list(newMesh.points[0])
    movingMatrix: s.Matrix = utils.getMovingMatrix(-pnt[0], -pnt[1], -pnt[2])

    finalMatrix: s.Matrix = movingMatrix.inv() * rotationMatrix * movingMatrix

    newMesh.updatePoints(finalMatrix)

    def plot_func(freq):
        utils.drawPlot([mesh, newMesh], "Задание №5")

    interact(plot_func, freq=widgets.FloatSlider(value=7.5, min=1, max=10, step=0.5))


def sixthTask():
    # Сначала "опустим" камеру для большей наглядности
    camera = utils.CameraPosition(0, 0, 10)

    meshes = utils.generateThreeCubes()

    def plot_func(freq):
        # Обычная отрисовка сцены
        utils.drawPlot(meshes, "Задание №6", camera)

        # С применением видовой матрицы
        # вектор перемещения (Сейчас камера на (10, 0, 0)
        C = s.Matrix([[-10, 0, 0]]).T

        # Вертикальная, горизонтальная и направляющая составляющие
        N = s.Matrix([[0, 0, 1]]).T
        V = s.Matrix([[-1, 1, 0]]).T / 2**0.5
        U = s.Matrix([[-1, -1, 0]]).T / 2**0.5

        # Таким образом матрица T поворачивает камеру на 45
        # градусов в плоскости xOy и осуществляет перенос на 10 по x

        T: s.Matrix = utils.getPerspectiveMatrix(U, V, N, C).T
        print(T)

        for mesh in meshes:
            mesh.updatePoints(T)
        utils.drawPlot(meshes, "Задание №6", camera)

    interact(plot_func, freq=widgets.FloatSlider(value=7.5, min=1, max=10, step=0.5))


def seventhTask():
    frontCameraView = utils.CameraPosition(0, 0, 10)
    camera = utils.CameraPosition()

    meshes = utils.generateThreeCubes()

    T: s.Matrix = s.eye(4)
    T[0, 3] = -0.05
    T[0, 0] = 0
    print(T)

    def plot_func(freq):
        # Обычная отрисовка сцены
        utils.drawPlot(meshes, "Задание №7, без проецирования", frontCameraView)
        utils.drawPlot(meshes, "Задание №7, без проецированием, вид сбоку", camera)

        # Применяем матрицу проецирования
        for mesh in meshes:
            mesh.updatePoints(T)

        utils.drawPlot(meshes, "Задание №7, с проецированием", frontCameraView)

        utils.drawPlot(meshes, "Задание №7, с проецированием, вид сбоку", camera)

    interact(plot_func, freq=widgets.FloatSlider(value=7.5, min=1, max=10, step=0.5))


def eighthTask():
    camera = utils.CameraPosition(0, 0, 10)
    camera2 = utils.CameraPosition(0, -90, 10)

    colors = [utils.Color.green, utils.Color.pink]

    def getCube(color=None) -> utils.Mesh:
        if color is None:
            color = colors[random.randint(0, len(colors) - 1)]
        mesh = utils.generateCube("", color, 0.5)
        return mesh

    cubes = []

    dl = [-2.5, -2.5, 0]
    dr = [-2.5, 2.5, 0]
    db = [-2.5, -3.5, 0]
    df = [2.5, -3.5, 0]

    roof = [-3, -3, 3]

    for i in range(3):
        for j in range(5):
            dl[0] += 1
            dr[0] += 1
            l = getCube()
            l.moveTo(dl)
            cubes.append(l)

            r = getCube()
            r.moveTo(dr)
            cubes.append(r)

        for j in range(6):
            db[1] += 1
            df[1] += 1

            b = getCube()
            b.moveTo(db)
            cubes.append(b)

            if df == [2.5, 0.5, 0] or df == [2.5, 0.5, 1]:
                continue
            f = getCube()
            f.moveTo(df)
            cubes.append(f)

        dl[2] += 1
        dr[2] += 1
        db[2] += 1
        df[2] += 1
        dl[0] = -2.5
        dr[0] = -2.5
        db[1] = -3.5
        df[1] = -3.5

    for i in range(7):
        for j in range(7):
            cube = getCube(color=utils.Color.blue)
            cube.moveTo(roof)
            cubes.append(cube)

            roof[1] += 1

        roof[0] += 1
        roof[1] = -3

    utils.drawPlot(cubes, "Задание №8")
    utils.drawPlot(cubes, "Задание №8", cameraPosition=camera)
    utils.drawPlot(cubes, "Задание №8", cameraPosition=camera2)


if __name__ == "__main__":
    # firstTask()
    # secondTask()
    # thirdTask()
    # fourthTask()
    # fifthTask()
    # sixthTask()
    seventhTask()
    eighthTask()
