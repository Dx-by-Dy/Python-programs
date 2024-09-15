import pygame
from random import randint as rint


class Config:
    WIN_SIZE = (1801, 901)
    RECT_SIZE = 15
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
        START_POINT_COLOR = GREEN
        END_POINT_COLOR = BLUE


class Wall_rects:
    wall_points = []
    cnt_points = 0

    def clear():
        Wall_rects.wall_points = []
        Wall_rects.cnt_points = 0

    def add_point(point):
        Wall_rects.wall_points += [point]
        Wall_rects.cnt_points += 1

    def create_walls():
        Wall_rects.clear()
        while Wall_rects.cnt_points < Config.CNT_RECTS[0] * Config.CNT_RECTS[1] * Config.COEF_WALL:
            r_point = (rint(0, Config.CNT_RECTS[0] - 1), rint(0, Config.CNT_RECTS[1] - 1))
            if r_point not in Wall_rects.wall_points:
                Wall_rects.add_point(r_point)


class Way:
    start_end_points = [(), ()]
    front_log = []
    way = []

    def dist(point1, point2, metric):
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

    def rects_near(point, metric):
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


def start():
    Wall_rects.create_walls()
    Way.create_points()
    Way.wave_method()


def update():
    win.fill(Config.color.B_COLOR)

    for i in range(Config.CNT_RECTS[0] + 1):
        pygame.draw.line(win, Config.color.LINE_COLOR, (Config.RECT_SIZE * i, 0), (Config.RECT_SIZE * i, Config.WIN_SIZE[1]))

    for i in range(Config.CNT_RECTS[1] + 1):
        pygame.draw.line(win, Config.color.LINE_COLOR, (0, Config.RECT_SIZE * i) ,(Config.WIN_SIZE[0], Config.RECT_SIZE * i))

    for point in Wall_rects.wall_points:
        pygame.draw.rect(win, Config.color.WALL_RECT_COLOR, (point[0] * Config.RECT_SIZE, point[1] * Config.RECT_SIZE, Config.RECT_SIZE, Config.RECT_SIZE), border_radius=Config.RECT_SIZE // 3)

    pygame.draw.rect(win, Config.color.START_POINT_COLOR, (Way.start_end_points[0][0] * Config.RECT_SIZE, Way.start_end_points[0][1] * Config.RECT_SIZE, Config.RECT_SIZE, Config.RECT_SIZE), border_radius=Config.RECT_SIZE // 3)
    pygame.draw.rect(win, Config.color.END_POINT_COLOR, (Way.start_end_points[1][0] * Config.RECT_SIZE, Way.start_end_points[1][1] * Config.RECT_SIZE, Config.RECT_SIZE, Config.RECT_SIZE), border_radius=Config.RECT_SIZE // 3)

    if show_sim:
        for idx_log in range(1, len(Way.front_log)):
            if idx_log <= step_sim:
                for point in Way.front_log[idx_log]:
                    if idx_log < step_sim:
                        pygame.draw.rect(win, Config.color.BLACK_MAGENTA, (point[0] * Config.RECT_SIZE, point[1] * Config.RECT_SIZE, Config.RECT_SIZE, Config.RECT_SIZE), border_radius=Config.RECT_SIZE // 3)
                    else:
                        pygame.draw.rect(win, Config.color.MAGENTA, (point[0] * Config.RECT_SIZE, point[1] * Config.RECT_SIZE, Config.RECT_SIZE, Config.RECT_SIZE), border_radius=Config.RECT_SIZE // 3)

    if step_sim == len(Way.front_log) or (show_sim == False and step_sim == 1):
        for point in Way.way:
            pygame.draw.rect(win, Config.color.GRAY_2, (point[0] * Config.RECT_SIZE, point[1] * Config.RECT_SIZE, Config.RECT_SIZE, Config.RECT_SIZE), border_radius=Config.RECT_SIZE // 3)

    pygame.display.update()


if __name__ == "__main__":
    win = pygame.display.set_mode(Config.WIN_SIZE)
    pygame.display.set_caption('Tutorial')

    start()
    step_sim = 0
    show_sim = False

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