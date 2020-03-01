import numpy as np
from random import randint
from copy import deepcopy
import cv2
import utils
import grid
import paho.mqtt.client as mqtt

# Global variables
BROKER_ADRESS = "192.168.9.201"
sudoku_grid = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 0, 9]]
counter = 0
solutions = []
recur_cnt = 0
IMG_NAME = 'puzzle1.jpg'


def on_connect(client, userdata, flags, rc):
    print("Connected to broker with result code " + str(rc))
    client.subscribe("sudoku/photo")


def on_message(client, userdata, msg):
    global counter
    counter = 0
    if msg.topic == "sudoku/photo":
        with open('./mqtt_com/' + IMG_NAME, "wb") as f:
            f.write(msg.payload)
        solve_sudoku()
        send_solution(client)
    if msg.payload.decode() == "End":
        print("Okey! I'm disconnecting :)")
        client.disconnect()


def send_message(client, topic, msg):
    client.publish(topic, msg)


def is_possible(y, x, n):
    global sudoku_grid
    for i in range(0, 9):
        if sudoku_grid[y][i] == n:
            return False
    for j in range(0, 9):
        if sudoku_grid[j][x] == n:
            return False
    x0 = (x//3)*3
    y0 = (y//3)*3
    for k in range(0, 3):
        for l in range(0, 3):
            if sudoku_grid[y0+k][x0+l] == n:
                return False
    return True


def solve_recursion():
    global sudoku_grid, counter, solutions, recur_cnt
    recur_cnt += 1
    if recur_cnt > 10**5:
        return
    for y in range(9):
        for x in range(9):
            if sudoku_grid[y][x] == 0:
                for n in range(1, 10):
                    if is_possible(y, x, n):
                        sudoku_grid[y][x] = n
                        solve_recursion()
                        sudoku_grid[y][x] = 0
                return
    counter += 1
    solutions.append(deepcopy(sudoku_grid))


def solve_sudoku():
    global sudoku_grid, counter, solutions
    model = utils.load_mnist_model()
    img = cv2.imread("./mqtt_com/" + IMG_NAME)
    sudoku_grid = grid.recognize_grid(model, img)

    solve_recursion()
    print("Number or recurrent function invocations: {}".format(recur_cnt))
    print("There are {} possible solutions".format(counter))
    if len(solutions) > 0:
        print("Random solution:")
        solved_grid = solutions[randint(0, counter - 1)]
        print(np.matrix(solved_grid))

        img_solved = grid.draw_solved_grid(model, img, solved_grid)
        cv2.imwrite("./results/" + IMG_NAME, img_solved)
        # cv2.imshow("Solved sudoku", img_solved)
        # cv2.waitKey(0)


def send_solution(client):
    global solutions, counter
    with open("./results/" + IMG_NAME, "rb") as f:
        fileContent = f.read()
        byteArrayPhoto = bytearray(fileContent)
    client.publish("sudoku/solution/photo", byteArrayPhoto)
    client.publish("sudoku/solution/grid", str(solutions[randint(0, counter - 1)]))


def main():
    client = mqtt.Client()
    client.connect(BROKER_ADRESS, 1883, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()


if __name__ == "__main__":
    main()

