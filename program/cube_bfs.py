from collections import deque, Counter
import time

# 表示用
def show(list, kaku):
    lt = list
    lp = [0]
    for(i) in range(1, len(lt)+1):
        lp.append((lp[i-1] + lt[i-1]) % kaku)
    for i in range(len(lp)):
        if lp[i] == 0:
            print("R", end="")
        elif lp[i] == 1:
            print("Y", end="")
        elif lp[i] == 2:
            print("B", end="")
        elif lp[i] == 3:
            print("G", end="")
        elif lp[i] == 4:
            print("O", end="")
        elif lp[i] == 5:
            print("P", end="")
        elif lp[i] == 6:
            print("G", end="")
    print(end=" ")

# 回転操作
def rotate(lt, kaku, n1, n2, deg):
    le = list(lt)
    le[n1-1] = (le[n1-1] + deg) % kaku
    if(n2 != len(le)):
        le[n2] = (le[n2] - deg + kaku) % kaku
    return tuple(le)

# 手数探索
def bfs(k, t):
    Init = tuple([0] * (t-1))
    T = {Init: 0}
    queue = deque([Init])
    max_depth_states = []
    
    operations = [
        (x1, x2, d)
        for x1 in range(1, t)
        for x2 in range(x1, t)
        for d in range(1, k)
    ]

    time_start = time.time()
    while queue:
        current_X = queue.popleft()
        current_depth = T[current_X]
        for x1, x2, d in operations:
            new_X = rotate(current_X, k, x1, x2, d)
            if new_X in T:
                continue  # 既に探索済みならスキップ
            T[new_X] = current_depth + 1
            queue.append(new_X)
    time_end = time.time()
    max_depth = max(T.values())
    max_depth_states = [state for state, depth in T.items() if depth == max_depth]
    depth_count = Counter(T.values())
    if len(T) == k**(t-1):
        print("All elements are explored")
    else: 
        print("Not explored")
    print(f"探索時間: {time_end - time_start:.10f} 秒")
    return max_depth, max_depth_states, depth_count

while True:
    try:
        k = int(input("側面の数を2~7の自然数で入力してください: "))
        if k < 2 or k > 7:
            raise ValueError("入力が許されるのは2~7の自然数のみです。")
        try:
            t = int(input("タワーの段数を2以上の自然数で入力してください: "))
            if t < 2:
                raise ValueError("入力が許されるのは2以上の自然数のみです。")
            else:
                break
        except ValueError:
            print("指定された自然数ではありません。再入力してください。")
    except ValueError:
        print("指定された自然数ではありません。再入力して下さい。")

depth, states, counts = bfs(k, t)

print("最小手数とその盤面数:", dict(counts))
print("最大最小手数 (", depth, "手) が必要な盤面一覧:", end=" ")
for s in states:
    show(s, k)