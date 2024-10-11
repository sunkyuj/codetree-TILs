OK = 0
FAINT = 2
DEAD = -1
MAX = 99999
NO_MOVE = 8
dydx = [
    (-1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
    (1, 0),
    (1, -1),
    (0, -1),
    (-1, -1),
]  # 위 부터 시계방향
in_range = lambda y, x: 1 <= y <= N and 1 <= x <= N

N, M, P, C, D = map(int, input().split())
board = [[0 for _ in range(N + 1)] for _ in range(N + 1)]
r, c = map(int, input().split())
santas = [None for _ in range(P + 1)]  # santas[i] = [y,x,status, score]
board = [[0 for _ in range(N + 1)] for _ in range(N + 1)]


def get_dist(r1, c1, r2, c2):
    return (r1 - r2) ** 2 + (c1 - c2) ** 2


for i in range(1, P + 1):
    num, y, x = map(int, input().split())
    santas[num] = [y, x, OK, 0]
    board[y][x] = num


def r_move():
    global r, c
    # 루돌프 움직임: 가장 가까운 산타 선택(거리 짧,r큰,c큰) -> 8 방향 중 가장 가까워지는 방향으로 이동
    # pick closeset santa
    best = (MAX, 0, 0, 0)  # dist, -r, -c, i
    for i in range(1, P + 1):
        y, x, status, score = santas[i]
        if status == DEAD:
            continue
        dist = get_dist(r, c, y, x)
        best = min(best, (dist, -y, -x, i))

    target = santas[best[3]]
    new_dist, best_y, best_x = MAX, 0, 0
    best_dy, best_dx = -1, -1
    # move
    for dy, dx in dydx:
        ny, nx = r + dy, c + dx
        if not in_range(ny, nx):
            continue
        dist = get_dist(target[0], target[1], ny, nx)
        if dist < new_dist:
            new_dist = dist
            best_y, best_x = ny, nx
            best_dy, best_dx = dy, dx
    r, c = best_y, best_x

    # colide
    if board[r][c]:
        num = board[r][c]
        # print(f"R hit santa{num}")
        santas[num][2] = FAINT
        santas[num][3] += C
        nuckback(num, best_dy, best_dx, C)
    return


def s_move():
    global r, c
    # 산타 움직임: 1번부터 p 순, OK산타만, 루돌프랑 가까워지는 4방향으로 이동(상우하좌 순)
    # 다른 산타 있으면 그칸 못감

    for i in range(1, P + 1):
        santa = santas[i]
        # 기절하거나 탈락하면 안됨
        if santa[2] != OK:
            # print(f"santa{i} cant move")
            continue

        # 움직일 수 있더라도 가까워지지 않으면 움직이지 않음
        y, x = santa[0], santa[1]
        dist = get_dist(r, c, y, x)
        best = (dist, NO_MOVE)  # dist, dir
        for dir in range(0, 8, 2):
            dy, dx = dydx[dir]
            ny, nx = y + dy, x + dx
            if not in_range(ny, nx) or board[ny][nx]:
                continue
            new_dist = get_dist(r, c, ny, nx)
            best = min(best, (new_dist, dir))

        if best[1] != NO_MOVE:
            # move
            dy, dx = dydx[best[1]]
            ny, nx = y + dy, x + dx
            santas[i][0], santas[i][1] = ny, nx
            board[ny][nx] = board[y][x]
            board[y][x] = 0

            # colide
            if (ny, nx) == (r, c):
                # print(f"santa{i} hit R")
                op_dir = (best[1] + 4) % 8
                dy, dx = dydx[op_dir]
                santas[i][2] = FAINT
                santas[i][3] += D
                nuckback(i, dy, dx, D)
    return


def nuckback(num, dy, dx, CD):
    y, x, status, score = santas[num]
    board[y][x] = 0
    ny, nx = y + dy * CD, x + dx * CD  # 착지 위치
    # 산타 밀림
    tmp = num
    while in_range(ny, nx) and board[ny][nx]:
        santas[tmp][0], santas[tmp][1] = ny, nx
        tmp, board[ny][nx] = board[ny][nx], tmp
        ny, nx = ny + dy, nx + dx

    if not in_range(ny, nx):
        santas[tmp][0] = 0
        santas[tmp][1] = 0
        santas[tmp][2] = DEAD
        # print(f"santa{tmp} dead")
    else:
        santas[tmp][0], santas[tmp][1] = ny, nx
        board[ny][nx] = tmp

    return


def live_bonus():
    alive = 0
    for i in range(1, P + 1):
        status = santas[i][2]
        if status != DEAD:
            alive += 1
            santas[i][3] += 1
            if status != OK:
                santas[i][2] -= 1
    return alive


def print_stat():
    global r, c
    for row in board[1:]:
        print(row[1:])
    for santa in santas[1:]:
        print(santa[3], end=" ")
    print("\nR:", r, c)


for _ in range(M):
    # print("#", _ + 1)
    # print("R:", r, c)
    r_move()
    s_move()
    life = live_bonus()
    if life == 0:
        break
    # print_stat()

for santa in santas[1:]:
    print(santa[3], end=" ")