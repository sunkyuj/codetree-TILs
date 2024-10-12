from collections import deque

dydx = [(-1,0),(0,1),(1,0),(0,-1)] # ^>v<
in_range = lambda y,x: 0<=y<R+3 and 0<=x<C

R,C,K = map(int,input().split()) # 70 70 1000
# 우선순위: v, <v, >v
# 내릴때는 항상 본인 골렘의 출구로 내려야함
ans = 0
board = [[0 for _ in range(C)] for _ in range(R+3)] # 위에 0~2행은 바깥

gy = [-1 for _ in range(K+1)] # 골렘 중앙 y
gx = [-1 for _ in range(K+1)] # 골렘 중앙 x
gd = [-1 for _ in range(K+1)] # 골렘 출구 방향
d_chk = [(1,1),(1,-1),(2,0)]
ld_chk = [(-1,-1),(0,-2),(1,-1),(1,-2),(2,-1)]
rd_chk = [(-1,1),(0,2),(1,1),(1,2),(2,1)]

def check(y,x,chk):
    for dy,dx in chk:
        ny,nx = y+dy,x+dx
        if not in_range(ny,nx) or board[ny][nx]!=0:
            return False
    return True

def down(num):
    # check
    if not check(gy[num],gx[num],d_chk):
        return 0
    # move 
    gy[num] += 1
    return 1

def left_down(num):
    # check
    if not check(gy[num],gx[num],ld_chk):
        return 0
    # move 
    gy[num] += 1
    gx[num] -= 1
    gd[num] = (gd[num]-1)%4
    return 1

def right_down(num):
    # check
    if not check(gy[num],gx[num],rd_chk):
        return 0
    # move 
    gy[num] += 1
    gx[num] += 1
    gd[num] = (gd[num]+1)%4
    return 1


def go(num):
    while True:
        if down(num):
            continue
        
        if left_down(num):
            continue

        if right_down(num):
            continue
        break
    
    if gy[num] <= 3: # 삐져나옴
        return 0 
    
    # board에 반영
    y,x = gy[num], gx[num]
    board[y][x] = num
    for k in range(4):
        dy,dx = dydx[k]
        ny,nx = y+dy, x+dx
        board[ny][nx] = num if k != gd[num] else -num
    
    # for row in board[3:]:
    #     print(row)
    
    # 골렘들 타고다니기
    return person_bfs(num)

def person_bfs(num):
    ret = 0
    q = deque()
    visit = set()
    q.append((gy[num],gx[num],num))
    
    while q:
        y,x,cur = q.popleft()
        ret = max(ret, y)        
        for dy,dx in dydx:
            ny,nx = y+dy, x+dx
            if not in_range(ny,nx) or board[ny][nx]==0 or (ny,nx) in visit:
                continue
            if board[y][x] == -cur: # 출구, 다른골렘 갈수있음
                q.append((ny,nx,abs(board[ny][nx])))
                visit.add((ny,nx))
            else: # 출구 아니라 다른 같은 골렘만 감
                if abs(board[ny][nx]) == cur:
                    q.append((ny,nx,cur))
                    visit.add((ny,nx))

    return ret-2

def clear():
    for i in range(R+3):
        for j in range(C):
            board[i][j] = 0


for i in range(1,K+1):
    c,d = map(int,input().split())
    gy[i] = 1
    gx[i] = c-1
    gd[i] = d

    result = go(i)
    if result == 0:
        clear()
    else:
        ans+=result
print(ans)