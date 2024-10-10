q = int(input()) # 10만
n,m =0,0 # 10만, 10만
belts = [] # len m (10만)
presents = [None]

class Present:
    def __init__(self, num):
        self.num = num
        self.prev = None
        self.nxt = None
        

class Belt:
    def __init__(self):
        self.size = 0
        self.head = None
        self.tail = None

    def append(self,p):
        if self.size == 0:
            self.head = p
            self.tail = p
        else:
            self.tail.nxt = p
            p.prev = self.tail
            self.tail = p
        self.size +=1

    def append_left(self,p):
        if self.size == 0:
            self.head = p
            self.tail = p
        else:
            self.head.prev = p
            p.nxt = self.head
            self.head = p
        self.size +=1

    def append_n_left(self,new_size,new_head,new_tail):
        new_head.prev = None
        new_tail.nxt = self.head
        if self.size == 0:
            self.head = new_head
            self.tail = new_tail
        else:
            self.head.prev = new_tail
            self.head = new_head
        self.size += new_size


    def pop_left(self):
        p = self.head
        self.size -= 1
        if self.size == 0:
            self.clear()
        else:
            self.head = self.head.nxt
            self.head.prev = None
        p.nxt = None  
        return p
    
    def pop_n_left(self,n):
        new_size = 1
        new_head = self.head
        new_tail = self.head
        for _ in range(n-1):
            new_tail = new_tail.nxt
            new_size += 1
        
        self.size -= n
        self.head = new_tail.nxt
        if self.head:
            self.head.prev = None
        new_tail.nxt = None
        if self.size == 0:
            self.clear()
        return (new_size, new_head, new_tail)
    
    def pop_all(self):
        new_size, new_head, new_tail = self.size, self.head, self.tail
        self.clear()
        return (new_size, new_head, new_tail)
    
    def clear(self):
        self.size = 0
        self.head = None
        self.tail = None
    

def init(cmd):
    global n,m,belt,head
    n,m = cmd[1], cmd[2]
    for _ in range(n+1):
        belts.append(Belt())

    p_num = 1
    for loc in cmd[3:]:
        p = Present(p_num)
        presents.append(p)
        belts[loc].append(p)
        p_num+=1
    

def move_all(src, dst): # 10만
    src_belt = belts[src]
    dst_belt = belts[dst]

    if src_belt.size > 0:
        new_size, new_head, new_tail = src_belt.pop_all()
        dst_belt.append_n_left(new_size, new_head, new_tail)

    return dst_belt.size


def move_front(src, dst): # 10만
    src_belt = belts[src]
    dst_belt = belts[dst]

    if src_belt.size == 0 and dst_belt.size == 0:
        return 0
    if src_belt.size != 0 and dst_belt.size != 0:
        p1 = src_belt.pop_left()
        p2 = dst_belt.pop_left()
        dst_belt.append_left(p1)
        src_belt.append_left(p2)
        return dst_belt.size

    if src_belt.size != 0:
        p = src_belt.pop_left()
        p.prev = p.nxt = None
        dst_belt.append(p)
    else:
        p = dst_belt.pop_left()
        p.prev = p.nxt = None
        src_belt.append(p)
    return dst_belt.size


def div(src, dst): # 최대 100회 호출
    src_belt = belts[src]
    dst_belt = belts[dst]
    if src_belt.size <= 1:
        return dst_belt.size

    half_size = src_belt.size // 2
    new_size, new_head, new_tail = src_belt.pop_n_left(half_size)
    dst_belt.append_n_left(new_size, new_head, new_tail)
    return dst_belt.size

def get_present(p_num): # 10만
    # p 앞(a), 뒤(b) -> a+2b (없으면 각각 -1)
    p = presents[p_num]
    a = p.prev.num if p.prev else -1
    b = p.nxt.num if p.nxt else -1
    return a+2*b

def get_belt(b_num): # 10만
    # b 맨앞(a), 맨뒤(b), 선물수(c) -> a+2b+3c (선물 없으면 -3)
    belt = belts[b_num]
    a = belt.head.num if belt.head else -1
    b = belt.tail.num if belt.tail else -1
    c = belt.size
    return a+2*b+3*c

def print_belts():
    for i in range(1,n+1):
        belt = belts[i]
        h = belt.head
        print("belt",i,":", end=' ')
        while h:
            print(h.num, end=' ')
            h = h.nxt
        print()
    print()



for _ in range(q):
    # print("this trial is ",_+1)
    cmd = list(map(int,input().split()))
    if cmd[0] == 100: # 공장 설립
        init(cmd)
    elif cmd[0] == 200: # 물건 모두 옮기기
        print(move_all(cmd[1], cmd[2]))
    elif cmd[0] == 300: # 앞 물건만 교체
        print(move_front(cmd[1], cmd[2]))
    elif cmd[0] == 400: # 물건 나누기
        print(div(cmd[1], cmd[2]))
    elif cmd[0] == 500: # 선물 정보 얻기
        print(get_present(cmd[1]))
    elif cmd[0] == 600: # 벨트 정보 얻기
        print(get_belt(cmd[1]))
    else:
        pass
    # print_belts()