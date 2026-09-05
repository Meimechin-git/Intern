from collections import deque
import time

# 表示用（ルックアップテーブルで高速化）
_COLOR = "RYBGOPVWAS"  # 0=R, 1=Y, 2=B, 3=G, 4=O, 5=P, 6=V, 7=W, 8=A, 9=S

def show(diff, kaku):
    c = 0
    print("R", end="")  # 最下段は常に赤
    for d in diff:
        c = (c + d) % kaku
        print(_COLOR[c], end="")
    print(end=" ")


def bfs(k, n):
    size = n - 1
    total = k ** size

    # kpow[i] = k^i（エンコード用）
    kpow = [1] * size
    for i in range(1, size):
        kpow[i] = kpow[i-1] * k
    
    single_ops = []
    double_ops = []
    for x1 in range(1, n):
        for x2 in range(x1, n):
            for d in range(1, k):
                i1 = x1 - 1
                d1 = d
                if x2 < size:
                    double_ops.append((i1, d1, x2, k - d))
                else:
                    single_ops.append((i1, d1))

    # bytearray で深さを管理（0xff = 未訪問）
    depth_arr = bytearray([0xff] * total)
    depth_arr[0] = 0  # 初期状態 (0,0,...,0) → インデックス 0

    queue = deque([0])  # エンコードされた整数のキューに変更
    depth_count = {0: 1}
    max_depth = 0

    time_start = time.time()

    while queue:
        enc = queue.popleft()
        current_depth = depth_arr[enc]
        nd = current_depth + 1

        # デコードして state リストを復元
        state = []
        tmp = enc
        for _ in range(size):
            state.append(tmp % k)
            tmp //= k

        for i1, d1 in single_ops:
            v1 = state[i1]
            nv1 = (v1 + d1) % k
            new_enc = enc + (nv1 - v1) * kpow[i1]
            if depth_arr[new_enc] == 0xff:
                depth_arr[new_enc] = nd
                depth_count[nd] = depth_count.get(nd, 0) + 1
                if nd > max_depth:
                    max_depth = nd
                queue.append(new_enc)

        for i1, d1, i2, d2 in double_ops:
            v1, v2 = state[i1], state[i2]
            nv1, nv2 = (v1 + d1) % k, (v2 + d2) % k
            new_enc = enc + (nv1 - v1) * kpow[i1] + (nv2 - v2) * kpow[i2]
            if depth_arr[new_enc] == 0xff:
                depth_arr[new_enc] = nd
                depth_count[nd] = depth_count.get(nd, 0) + 1
                if nd > max_depth:
                    max_depth = nd
                queue.append(new_enc)

    time_end = time.time()

    max_depth_states = []
    for enc in range(total):
        if depth_arr[enc] == max_depth:
            # インデックス → 状態タプルにデコード
            state = []
            tmp = enc
            for _ in range(size):
                state.append(tmp % k)
                tmp //= k
            max_depth_states.append(tuple(state))

    if depth_arr.count(0xff) == 0:
        print("All elements are explored")
    else:
        print("Not explored")
    print(f"探索時間: {time_end - time_start:.10f} 秒")
    return max_depth, max_depth_states, depth_count


# ── 入力 ──────────────────────────────────────────────────────────
while True:
    try:
        k = int(input("側面の数を3~10の自然数で入力してください: "))
        if k < 3 or k > 10:
            raise ValueError("Error: 入力が許されるのは3~10の自然数のみです。")
        break
    except ValueError as e:
        print(e)

while True:
    try:
        n = int(input("タワーの段数を自然数で入力してください: "))
        if n < 2:
            raise ValueError("Error: 入力が許されるのは2以上の自然数のみです。")
        break
    except ValueError as e:
        print(e)

depth, states, counts = bfs(k, n)
print("最大最小手数:", depth, "手")
print("最小手数と盤面数:", dict(counts))
print(depth, "手が必要な盤面一覧:", end=" ")
for s in states:
    show(s, k)