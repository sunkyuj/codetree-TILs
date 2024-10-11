SPACE = 0
TRAP = 1
WALL = 2
dydx = [(-1,0), (0,1), (1,0), (0,-1)]
in_range = lambda y,x: 0<=y<L and 0<=x<L

L,N,Q = map(int,input().split())
board = [list(map(int,input().split())) for _ in range(L)]
area = [[0 for _ in range(L)] for _ in range(L)]
kloc, ksize, khp = [None for _ in range(N+1)],[None for _ in range(N+1)],[None for _ in range(N+1)]
khp_full = [None for _ in range(N+1)] # 나중에 비교용

def fill(num, r,c,h,w):
    for i in range(r,r+h):
        for j in range(c,c+w):
            area[i][j] = num

def move(k_num, d, no_dmg=False):
    dy, dx = dydx[d]
    next_edge = get_next_edge(k_num,d)
    for ny,nx in next_edge:
        # 벽이면 못움직임
        if not in_range(ny,nx) or board[ny][nx] == WALL:
            return 0
        
        # 겹치는 기사 밀치기
        if area[ny][nx]:
            movable = move(area[ny][nx], d)
            if not movable:
                return 0
    
    # 못움직이는 것 없으므로 이제 움직임
    y,x = kloc[k_num]
    h,w = ksize[k_num]
    # 기준점
    kloc[k_num] = (y+dy,x+dx)
    # 움직인 곳
    for ny,nx in next_edge:
        area[ny][nx] = k_num
        area[ny-h*dy][nx-w*dx] = 0
    
    # 데미지
    if no_dmg:
        return 1
    for i in range(y+dy,y+dy+h):
        for j in range(x+dx,x+dx+w):
            khp[k_num] -= int(board[i][j]==TRAP)
    if khp[k_num] <= 0:
        for i in range(y+dy,y+dy+h):
            for j in range(x+dx,x+dx+w):
                area[i][j] = 0
    return 1


def get_next_edge(k_num,d): 
    sy,sx = kloc[k_num]
    h,w = ksize[k_num]
    ey,ex = sy+h, sx+w
    if d == 0:
        return [(sy-1,j) for j in range(sx,ex)]
    elif d==1:
        return [(i,ex) for i in range(sy,ey)]
    elif d==2:
        return [(ey,j) for j in range(sx,ex)]
    else:
        return [(i,sx-1) for i in range(sy,ey)]


for i in range(1,N+1):
    r,c,h,w,k = map(int,input().split())
    kloc[i] = (r-1,c-1)
    ksize[i] = (h,w)
    khp[i] = khp_full[i] = k
    fill(i,r-1,c-1,h,w)

for _ in range(Q):
    i,d = map(int,input().split()) # ^ > v <
    move(i,d,True)



# 생존한 기사들이 받은 총 데미지
ans = 0
for i in range(1,N+1):
    if khp[i]>0:
        ans += khp_full[i]-khp[i]
print(ans)