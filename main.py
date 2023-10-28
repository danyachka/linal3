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
    # Сначала "опустим" камеру для большей наглядности
    camera = u.CameraPosition(0, 0, 10)

    meshes = u.generateThreeCubes()

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


def seventhTask():
    frontCameraView = u.CameraPosition(0, 0, 10)
    camera = u.CameraPosition()

    meshes = u.generateThreeCubes()

    T: s.Matrix = s.eye(4)
    T[0, 3] = -0.05
    T[0, 0] = 0
    print(T)

    def plot_func(freq):
        # Обычная отрисовка сцены
        u.drawPlot(meshes, "Задание №7, без проецирования", frontCameraView)
        u.drawPlot(meshes, "Задание №7, без проецированием, вид сбоку", camera)

        # Применяем матрицу проецирования
        for mesh in meshes:
            mesh.updatePoints(T)

        u.drawPlot(meshes, "Задание №7, с проецированием", frontCameraView)

        u.drawPlot(meshes, "Задание №7, с проецированием, вид сбоку", camera)

    interact(plot_func, freq=widgets.FloatSlider(value=7.5, min=1, max=10, step=0.5))


def eighthTask():
    camera = u.CameraPosition(0, 0, 10)
    camera2 = u.CameraPosition(0, -90, 10)

    def getCube(color=u.Color.green) -> u.Mesh:
        mesh = u.generateCube("", color, 0.5)
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
            cube = getCube(color=u.Color.blue)
            cube.moveTo(roof)
            cubes.append(cube)

            roof[1] += 1

        roof[0] += 1
        roof[1] = -3

    u.drawPlot(cubes, "Задание №8")
    u.drawPlot(cubes, "Задание №8", cameraPosition=camera)
    u.drawPlot(cubes, "Задание №8", cameraPosition=camera2)


if __name__ == "__main__":
    # firstTask()
    # secondTask()
    # thirdTask()
    # fourthTask()
    # fifthTask()
    # sixthTask()
    # seventhTask()
    eighthTask()
