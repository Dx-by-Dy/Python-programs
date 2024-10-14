import pygame
from random import randint as rint


class Config:
    WIN_SIZE = (1801, 901)
    RECT_SIZE = 60
    CNT_RECTS = (WIN_SIZE[0] // RECT_SIZE, WIN_SIZE[1] // RECT_SIZE)
    COEF_WALL = 0.3

    class color:
        BLACK = (0, 0, 0)
        B_COLOR = BLACK
        WHITE = (255, 255, 255)
        GRAY = (100, 100, 100)
        GRAY_2 = (160, 160, 160)
        LINE_COLOR = GRAY
        ORANGE = (255, 153, 51)
        WALL_RECT_COLOR = ORANGE
        GREEN = (0, 204, 0)
        BLUE = (0, 0, 204)
        MAGENTA = (204, 0, 204)
        BLACK_MAGENTA = (102, 0, 102)
        START_POINT_COLOR = (204, 0, 0)
        END_POINT_COLOR = (204, 0, 0)

        OU = (0, 204, 204)
        DARK_OU = (0, 102, 102)
        DARK_DARK_OU = (0, 51, 51)

        COLOR_CELL = {1: ORANGE, 2: GREEN, 3: BLUE}


class Cell:
    def __init__(self, coord, cost=None):
        self.parent = None
        self.cost = cost if cost is not None else rint(1, 3)
        self.coord = coord
        self.range = 10000000
        self.was_active = False


class Lab:
    start_point = ()
    end_point = ()


    def fill_near_cell(point, cost, radius=3):
        cells = [point.coord]

        while cells != []:
            new_cells = []
            for f_cell in cells:
                for cell in Way.rects_near(f_cell):
                    if Way.in_map(cell) and Lab.array[cell[1]][cell[0]].cost != cost and Way.dist(point.coord, cell) <= radius:
                        Lab.array[cell[1]][cell[0]].cost = cost
                        new_cells += [cell]

            cells = new_cells.copy()

    array = [[]]

    def create_array():
        Lab.array = [[Cell((i, j), 1) for i in range(Config.CNT_RECTS[0])] for j in range(Config.CNT_RECTS[1])]

        for i in range(10):
            r_point = (rint(0, Config.CNT_RECTS[0] - 1), rint(0, Config.CNT_RECTS[1] - 1))
            Lab.fill_near_cell(Lab.array[r_point[1]][r_point[0]], rint(1, 3))

        Lab.start_point = (rint(0, Config.CNT_RECTS[0] - 1), rint(0, Config.CNT_RECTS[1] - 1))
        
        while True:
            r_point = (rint(0, Config.CNT_RECTS[0] - 1), rint(0, Config.CNT_RECTS[1] - 1))
            if Way.dist(Lab.start_point, r_point) > (Config.CNT_RECTS[0] + Config.CNT_RECTS[1]) // 2:
                Lab.end_point = r_point
                break


class Way:
    queue_log = []
    active_cell_log = []
    was_active_log = []
    way = []

    def dist(point1, point2, metric=4):
        if metric == 4:
            return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

    def create_points():
        while True:
            Way.start_end_points[0] = (rint(0, Config.CNT_RECTS[0] - 1), rint(0, Config.CNT_RECTS[1] - 1))
            if Way.start_end_points[0] not in Wall_rects.wall_points:
                break

        while True:
            Way.start_end_points[1] = (rint(0, Config.CNT_RECTS[0] - 1), rint(0, Config.CNT_RECTS[1] - 1))
            if Way.start_end_points[1] not in Wall_rects.wall_points and Way.start_end_points[0] != Way.start_end_points[1] and Way.dist(Way.start_end_points[0], Way.start_end_points[1], 4) >= (Config.CNT_RECTS[0] + Config.CNT_RECTS[1]) // 2:
                break

    def in_map(point):
        if 0 <= point[0] < Config.CNT_RECTS[0] and 0 <= point[1] < Config.CNT_RECTS[1]:
            return True
        return False

    def rects_near(point, metric=4):
        if metric == 4:
            return (point[0] + 1, point[1]),\
                    (point[0] - 1, point[1]),\
                    (point[0], point[1] + 1),\
                    (point[0], point[1] - 1)
        
    def get_way_in_wave_method(mp):
        Way.way = [Way.start_end_points[1]]
        step = mp[Way.start_end_points[1][1]][Way.start_end_points[1][0]]

        if step == None:
            print("NO WAY")
            return

        while True:
            step -= 1
            for point in Way.rects_near(Way.way[-1], 4):
                if Way.in_map(point) and mp[point[1]][point[0]] == step:
                    Way.way += [point]
                    break

            if step == 0:
                break 

    def wave_method():
        mp = [[None for i in range(Config.CNT_RECTS[0])] for j in range(Config.CNT_RECTS[1])]
        for point in Wall_rects.wall_points:
            mp[point[1]][point[0]] = -1

        step = 0
        mp[Way.start_end_points[0][1]][Way.start_end_points[0][0]] = step

        front = [Way.start_end_points[0]]
        Way.front_log += [front]

        stop = False
        while front != []:
            step += 1

            new_front = []
            for point in front:
                for npoint in Way.rects_near(point, 4):
                    if Way.in_map(npoint) and mp[npoint[1]][npoint[0]] == None:
                        mp[npoint[1]][npoint[0]] = step
                        new_front += [npoint]

                        if npoint == Way.start_end_points[1]:
                            stop = True

            front = new_front.copy()
            Way.front_log += [front]

            if stop:
                break

        Way.get_way_in_wave_method(mp)

    def Dei_method():
        active_cell = Lab.array[Lab.start_point[1]][Lab.start_point[0]]
        active_cell.was_active = True
        active_cell.range = 0
        queue = [active_cell.coord]

        while queue != []:
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:

                    if (i != 0 and j != 0) or (i == 0 and j == 0) or not Way.in_map((active_cell.coord[0] + i, active_cell.coord[1] + j)): 
                        continue

                    cell = Lab.array[active_cell.coord[1] + j][active_cell.coord[0] + i]
                    if cell.was_active:
                        continue

                    if cell.range > active_cell.range + cell.cost:
                        cell.range = active_cell.range + cell.cost
                        cell.parent = active_cell.coord

                        if cell.coord not in queue:
                            queue += [cell.coord]

            try:
                queue.pop(queue.index(active_cell.coord))
                if queue == []:
                    break
            except ValueError:
                pass

            min_queue = 10000000000000000
            min_coord = ()
            for point in queue:
                cell = Lab.array[point[1]][point[0]] 
                if cell.range < min_queue:
                    min_queue = cell.range
                    min_coord = cell.coord

            active_cell = Lab.array[min_coord[1]][min_coord[0]]
            active_cell.was_active = True

            Way.queue_log += [queue.copy()]
            Way.active_cell_log += [active_cell]
            Way.was_active_log += [active_cell.coord]


def start():
    Lab.create_array()
    Way.Dei_method()


def update():
    win.fill(Config.color.B_COLOR)

    for i in range(Config.CNT_RECTS[0] + 1):
        pygame.draw.line(win, Config.color.LINE_COLOR, (Config.RECT_SIZE * i, 0), (Config.RECT_SIZE * i, Config.WIN_SIZE[1]))

    for i in range(Config.CNT_RECTS[1] + 1):
        pygame.draw.line(win, Config.color.LINE_COLOR, (0, Config.RECT_SIZE * i) ,(Config.WIN_SIZE[0], Config.RECT_SIZE * i))

    for row in range(Config.CNT_RECTS[1]):
        for clm in range(Config.CNT_RECTS[0]):
            cell = Lab.array[row][clm]
            if cell.coord == Lab.start_point:
                pygame.draw.rect(win, Config.color.START_POINT_COLOR, (cell.coord[0] * Config.RECT_SIZE, cell.coord[1] * Config.RECT_SIZE, Config.RECT_SIZE, Config.RECT_SIZE))
            elif cell.coord == Lab.end_point:
                pygame.draw.rect(win, Config.color.END_POINT_COLOR, (cell.coord[0] * Config.RECT_SIZE, cell.coord[1] * Config.RECT_SIZE, Config.RECT_SIZE, Config.RECT_SIZE))
            else:
                pygame.draw.rect(win, Config.color.COLOR_CELL[cell.cost], (cell.coord[0] * Config.RECT_SIZE, cell.coord[1] * Config.RECT_SIZE, Config.RECT_SIZE, Config.RECT_SIZE))

    for point in Way.queue_log[step_sim]:
        pygame.draw.rect(win, Config.color.DARK_OU, (point[0] * Config.RECT_SIZE, point[1] * Config.RECT_SIZE, Config.RECT_SIZE, Config.RECT_SIZE))
    for point in Way.was_active_log[:step_sim]:
        pygame.draw.rect(win, Config.color.DARK_DARK_OU, (point[0] * Config.RECT_SIZE, point[1] * Config.RECT_SIZE, Config.RECT_SIZE, Config.RECT_SIZE))

    cell = Way.active_cell_log[step_sim]
    pygame.draw.rect(win, Config.color.OU, (cell.coord[0] * Config.RECT_SIZE, cell.coord[1] * Config.RECT_SIZE, Config.RECT_SIZE, Config.RECT_SIZE))

    pygame.display.update()


if __name__ == "__main__":
    win = pygame.display.set_mode(Config.WIN_SIZE)
    pygame.display.set_caption('Tutorial')

    start()
    step_sim = 0

    run = True
    while run:
        for event in pygame.event.get():
            # print(event)

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    step_sim += 1

            update()

        pygame.time.delay(60)

    pygame.quit()