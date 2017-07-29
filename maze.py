import random
import graphics
import time
import sys


global GLOBAL_WAIT;
GLOBAL_WAIT = 0


def draw_line(win, x1, x2, y1, y2):
    p1 = graphics.Point(x1, y1)
    p2 = graphics.Point(x2, y2)
    l1 = graphics.Line(p1, p2)
    l1.draw(win)


def recurse_render(win, maze, x, y, size, render_size, visited, wait):
    if x < 0 or x == size:
        return
    if y < 0 or y == size:
        return

    visited[str(x) + "_" + str(y)] = True
    time.sleep(GLOBAL_WAIT)

    if maze[x][y][0] == 1:
        pass
    else:
        draw_line(win, x*render_size, x*render_size, y*render_size, (y+1)*render_size)

    if maze[x][y][1] == 1:
        pass
    else:
        draw_line(win, (x+1)*render_size, (x+1)*render_size, y*render_size, (y+1)*render_size)

    if maze[x][y][2] == 1:
        pass
    else:
        draw_line(win, x*render_size, (x+1)*render_size, y*render_size, y*render_size)

    if maze[x][y][3] == 1:
        pass
    else:
        draw_line(win, x*render_size, (x+1)*render_size, (y+1)*render_size, (y+1)*render_size)


    if maze[x][y][0] == 1 and str(x-1) + "_" + str(y) not in visited:
        recurse_render(win, maze, x - 1, y, size, render_size, visited, wait)

    if maze[x][y][1] == 1 and str(x+1) + "_" + str(y) not in visited:
        recurse_render(win, maze, x + 1, y, size, render_size, visited, wait)


    if maze[x][y][2] == 1 and str(x) + "_" + str(y-1) not in visited:
        recurse_render(win, maze, x, y - 1, size, render_size, visited, wait)


    if maze[x][y][3] == 1 and str(x) + "_" + str(y+1) not in visited:
        recurse_render(win, maze, x, y + 1, size, render_size, visited, wait)




def render_board(win, maze, size, startx, starty, render_size):
    visited = {}
    global GLOBAL_WAIT;
    recurse_render(win, maze, startx, starty, size, render_size, visited, GLOBAL_WAIT)



def recurse(pos, visited, maze, size):
    visited[str(pos[0]) + "_" + str(pos[1])] = 1
    

    left = pos[0] - 1
    right = pos[0] + 1
    up = pos[1] - 1
    down = pos[1] + 1


    while(True):
        posibi = []

        if not left < 0 and str(left) + "_" + str(pos[1]) not in visited:
            posibi.append((1, left, pos[1], 0))

        if not up < 0 and str(pos[0]) + "_" + str(up) not in visited:
            posibi.append((3, pos[0], up, 2))

        if not right == size and str(right) + "_" + str(pos[1]) not in visited:
            posibi.append((0, right, pos[1], 1))

        if not down == size and str(pos[0]) + "_" + str(down) not in visited:
            posibi.append((2, pos[0], down, 3))



        if len(posibi) == 0:
            break

        r = random.randint(0, len(posibi)-1)

        maze[posibi[r][1]][posibi[r][2]][posibi[r][0]] = 1
        maze[pos[0]][pos[1]][posibi[r][3]] = 1
        recurse([posibi[r][1], posibi[r][2]], visited, maze, size)




def create_maze(size, startx, starty):
    maze = []
    # walls = []

    for i in range(size):
        a = []
        for j in range(size):
            a.append([0, 0, 0, 0])
        maze.append(a)

    start_pos = [startx, starty]

    visited = {}
    recurse(start_pos, visited, maze, size)

    return maze






def main():
    sys.setrecursionlimit(5000)
    global GLOBAL_WAIT;
    GLOBAL_WAIT = .01
    size = 70
    render_size = 14
    width = size * render_size
    height = size * render_size
    
    win = graphics.GraphWin("Maze!", width, height)
    win.setBackground("tan2")

    startx = random.randint(0, size-1)
    starty = random.randint(0, size-1)

    endx = random.randint(0, size-1)
    endy = random.randint(0, size-1)

    while endx == startx and starty == endy:
        endx = random.randint(0, size-1)
        endy = random.randint(0, size-1)

    print("STARTING", startx, starty)

    maze = create_maze(size, startx, starty)

    render_board(win, maze, size, startx, starty, render_size)

    exp = 3
    r1 = graphics.Rectangle(graphics.Point(startx*render_size + exp, starty*render_size + exp), graphics.Point((startx+1)*render_size - exp, (starty+1)*render_size - exp))
    r2 = graphics.Rectangle(graphics.Point(endx*render_size + exp, endy*render_size + exp), graphics.Point((endx+1)*render_size - exp, (endy+1)*render_size - exp))

    r1.setFill("green")
    r2.setFill("red")

    r1.draw(win)
    r2.draw(win)

    currx = startx
    curry = starty

    while(True):
        if currx == endx and curry == endy:
            print("you win")
            break

        win.update()
        keys = win.keyState
        
        if keys[0] == 1 and maze[currx][curry][0] == 1:
            currx -= 1
            r1.move(-render_size, 0)

        elif keys[1] == 1 and maze[currx][curry][2] == 1:
            curry -= 1
            r1.move(0, -render_size)

        elif keys[2] == 1 and maze[currx][curry][1] == 1:
            currx += 1
            r1.move(render_size, 0)

        elif keys[3] == 1 and maze[currx][curry][3] == 1:
            curry += 1
            r1.move(0, render_size)

        time.sleep(.18)

main()