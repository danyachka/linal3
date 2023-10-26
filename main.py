from ipywidgets import interact
import ipywidgets as widgets
import matplotlib
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

    newMesh.updatePoints(m)
    u.drawPlot([mesh, newMesh], "Задание №2")


def thirdTask():
    mesh = u.generateCube()
    newMesh = u.generateCube(color=u.Color.pink)

    m: s.Matrix = u.getMovingMatrix(-3, 0, 0)
    newMesh.updatePoints(m)

    u.drawPlot([mesh, newMesh], "Задание №3")


# В трёх плоскостях
# На вики
def fourthTask():
    matrix: s.Matrix = u.getRotationMatrix(z=45)

    mesh = u.generateCube(color=u.Color.pink, name="Rotated cube")
    mesh.updatePoints(matrix)

    u.drawPlot([mesh], "Задание №4")


def fifthTask():
    rotationMatrix: s.Matrix = u.getRotationMatrix(x=90, z=90)

    mesh = u.generateCube()
    newMesh = u.generateCube(color=u.Color.pink)

    pnt = list(newMesh.points[0])
    movingMatrix: s.Matrix = u.getMovingMatrix(-pnt[0], -pnt[1], -pnt[2])

    finalMatrix: s.Matrix = movingMatrix.inv() * rotationMatrix * movingMatrix

    newMesh.updatePoints(finalMatrix)

    def plot_func(freq):
        u.drawPlot([mesh, newMesh], "Задание №5")

    interact(plot_func, freq=widgets.FloatSlider(value=7.5, min=1, max=10, step=0.5))


def sixthTask():
    greenMesh = u.generateCube("green", color=u.Color.green)
    blueMesh = u.generateCube("blue", color=u.Color.blue)
    pinkMesh = u.generateCube("pink", color=u.Color.pink)

    x45 = u.getRotationMatrix(x=45)
    greenMesh.updatePoints(x45)

    moveY = u.getMovingMatrix(0, -3, 0)
    blueMesh.updatePoints(moveY)

    moveYBack = u.getMovingMatrix(0, 3, 0)
    z45 = u.getRotationMatrix(z=45)
    pinkMesh.updatePoints(z45)
    pinkMesh.updatePoints(moveYBack)

    # Сначала "опустим" камеру для большей наглядности
    camera = u.CameraPosition(0, 0, 10)

    meshes = [blueMesh, greenMesh, pinkMesh]

    def plot_func(freq):
        # Обычная отрисовка сцены
        u.drawPlot(meshes, "Задание №6", camera)

        # С применением видовой матрицы
        # вектор перемещения (Сейчас камера на (10, 0, 0)
        C = s.Matrix([[-10, 0, 0]]).T

        # Вертикальная, горизонтальная и направляющая составляющие
        N = s.Matrix([[0, 0, 1]]).T
        V = s.Matrix([[-1, 1, 0]]).T / 2**0.5
        U = s.Matrix([[-1, -1, 0]]).T / 2**0.5

        # Таким образом матрица T поворачивает камеру на 45
        # градусов в плоскости xOy и осуществляет перенос на 10 по x

        T: s.Matrix = u.getPerspectiveMatrix(U, V, N, C).T
        print(T)

        for mesh in meshes:
            mesh.updatePoints(T)
        u.drawPlot(meshes, "Задание №6", camera)

    interact(plot_func, freq=widgets.FloatSlider(value=7.5, min=1, max=10, step=0.5))


if __name__ == "__main__":
    # firstTask()
    # secondTask()
    # thirdTask()
    # fourthTask()
    # fifthTask()
    sixthTask()
