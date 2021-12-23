import math
import random

# 실험 매개변수 선언
# num_of_nodes = pow(2, 10)       # 전체 노드 개수 n (2의 제곱승으로 가정)
# num_of_triggers = pow(2, 20)    # 검출하고자 하는 트리거 개수 w
num_of_nodes = pow(2, 10)
num_of_triggers = 1000000

# TreeFill 매개변수 계산
detect_tree_depth = int(math.log2(num_of_nodes)) # DetectTree 높이

# TreeFill 노드 클래스 정의
class TreeFillNode:
    def __init__(self, node_num):
        # 전체 노드 정보
        self.node_num = node_num    # 노드 번호 in [0, n)
        self.send_message = 0       # 보낸 메시지 수
        self.receive_message = 0    # 받은 메시지 수

        # leaf 노드 정보
        self.leaf_counter = 0       # leaf 노드 카운터

        # internal 노드 정보
        self.left_full = False      # 왼쪽 자녀 노드 FULL 여부
        self.right_full = False     # 오른쪽 자녀 노드 FULL 여부

    def send(self):
        self.send_message += 1

    def receive(self):
        self.receive_message += 1

    def clear(self):
        self.leaf_counter = 0       # leaf 노드 카운터
        self.left_full = False      # 왼쪽 자녀 노드 FULL 여부
        self.right_full = False     # 오른쪽 자녀 노드 FULL 여부

# 메시지 전송 함수
def message_sr(sender, receiver, count):
    sender.send()
    receiver.receive()
    return count + 1

# DetectTree와 노드 초기화
tree_fill_nodes = []                                # 전체 노드 집합 초기화
for c in range(num_of_nodes):
    node = TreeFillNode(c)                          # 노드 생성
    tree_fill_nodes.append(node)                    # 전체 노드 집합에 노드 추가

# 실험 시작
w = num_of_triggers             # 검출하고자 하는 트리거 개수 w 초기화
trigger = 0                     # 현재까지 발생한 트리거의 수 trigger 초기화
round = 0                       # 라운드 초기화
message_count = 0               # 전체 메시지 수

# FULL 메시지 처리 함수
def receive_full(sender_index):
    global message_count
    global tree_fill_nodes
    if sender_index == 0:
        return
    sender = tree_fill_nodes[sender_index]
    direction = sender_index % 2                                        # direction이 1이면 왼쪽, 0이면 오른쪽
    receiver_index = (sender_index - 1) // 2                            # FULL 메시지를 받을 부모 노드
    receiver = tree_fill_nodes[receiver_index]
    message_count = message_sr(sender, receiver, message_count)         # FULL 메시지 전달
    if direction == 1:
        tree_fill_nodes[receiver_index].left_full = True
    else:
        tree_fill_nodes[receiver_index].right_full = True
    if tree_fill_nodes[receiver_index].left_full and tree_fill_nodes[receiver_index].right_full:
        receive_full(receiver_index)

# 코인 메시지 처리 함수
def receive_coin(sender_index, receiver_index):
    global num_of_nodes
    global message_count
    global tree_fill_nodes
    sender = tree_fill_nodes[sender_index]
    receiver = tree_fill_nodes[receiver_index]
    message_count = message_sr(sender, receiver, message_count)         # 코인 메시지 전달
    if receiver_index >= (num_of_nodes / 2 - 1):
        if not receiver.left_full:
            receiver.left_full = True
        elif not receiver.right_full:
            receiver.right_full = True
            receive_full(receiver_index)
        else:
            print("Error: Something wrong!!!")
            quit()
    else:
        if receiver.left_full and receiver.right_full:
            receive_coin(receiver_index, (receiver_index - 1) // 2)
        elif receiver.left_full:
            receive_coin(receiver_index, receiver_index * 2 + 2)
        else:
            receive_coin(receiver_index, receiver_index * 2 + 1)

# First Phase (w > 2n일 때)
while (w > num_of_nodes * 2):
    round += 1                                                  # 새로운 라운드 시작
    leaf_threshold = math.floor(w / (2 * num_of_nodes))         # 리프 노드 threshold 값 계산
    while (True):
        trigger += 1                                            # 트리거 발생
        trigger_node_index = random.randrange(0, num_of_nodes)  # 트리거 발생 노드 결정
        tree_fill_nodes[trigger_node_index].leaf_counter += 1   # 해당 리프 노드 카운터 값 증가
        if (tree_fill_nodes[trigger_node_index].leaf_counter == leaf_threshold):            # 리프 노드 카운터 값이 threshold에 이르면
            tree_fill_nodes[trigger_node_index].leaf_counter = 0                            # 리프 노드 카운터 초기화
            sender = tree_fill_nodes[trigger_node_index]
            dt_leaf_node_index = random.randrange(0, pow(2, detect_tree_depth - 1))         # 코인을 받을 DetectTree의 리프 노드 결정
            dt_node_index = (pow(2, detect_tree_depth - 1) - 1) + dt_leaf_node_index
            receiver = tree_fill_nodes[dt_node_index]
            message_count = message_sr(sender, receiver, message_count)                     # 코인 메시지 전달
            if not tree_fill_nodes[dt_node_index].left_full:
                tree_fill_nodes[dt_node_index].left_full = True
            elif not tree_fill_nodes[dt_node_index].right_full:
                tree_fill_nodes[dt_node_index].right_full = True
                receive_full(dt_node_index)
            else:
                receive_coin(dt_node_index, (dt_node_index - 1) // 2)
            if tree_fill_nodes[0].left_full and tree_fill_nodes[0].right_full:              # end-of-round 프로시저 시작 조건
                for d in range(0, detect_tree_depth - 1):                                   # end-of-round notification broadcast
                    for i in range(0, pow(2, d)):
                        sender = tree_fill_nodes[(pow(2, d) - 1) + i]                       # 부모 노드
                        receiver = tree_fill_nodes[(pow(2, d + 1) - 1) + (i * 2)]           # 왼쪽 자식 노드
                        message_count = message_sr(sender, receiver, message_count)         # 왼쪽 자식 노드에게 notification 전달
                        receiver = tree_fill_nodes[(pow(2, d + 1) - 1) + (i * 2) + 1]       # 오른쪽 자식 노드
                        message_count = message_sr(sender, receiver, message_count)         # 오른쪽 자식 노드에게 notification 전달
                message_count = message_sr(tree_fill_nodes[0], tree_fill_nodes[num_of_nodes - 1], message_count)    # internal 노드에 포함되지 않은 노드
                for d in range(0, detect_tree_depth - 1):                                # end-of-round upcast
                    for i in range(0, pow(2, d)):
                        receiver = tree_fill_nodes[(pow(2, d) - 1) + i]                     # 부모 노드
                        sender = tree_fill_nodes[(pow(2, d + 1) - 1) + (i * 2)]             # 왼쪽 자식 노드
                        message_count = message_sr(sender, receiver, message_count)         # 왼쪽 자식 노드의 트리거 및 코인 수 전달
                        sender = tree_fill_nodes[(pow(2, d + 1) - 1) + (i * 2) + 1]         # 오른쪽 자식 노드
                        message_count = message_sr(sender, receiver, message_count)         # 오른쪽 자식 노드의 트리거 및 코인 수 전달
                message_count = message_sr(tree_fill_nodes[num_of_nodes - 1], tree_fill_nodes[0], message_count)    # internal 노드에 포함되지 않은 노드
                w = w - trigger
                #print(f"1st Phase: {round:2d} 라운드 끝, 발생 트리거: {trigger:6d}, 남은 트리거: {w:6d}, 현재 message complexity: {message_count:6d}")
                trigger = 0
                for c in range(0, num_of_nodes):
                    tree_fill_nodes[c].clear()
                break

# Second Phase (n >= w >= 2n일 때)
while (w >= num_of_nodes):
    round += 1                                                  # 새로운 라운드 시작
    leaf_threshold = 1                                          # 리프 노드 threshold 값 = 1
    while (True):
        trigger += 1                                            # 트리거 발생
        trigger_node_index = random.randrange(0, num_of_nodes)  # 트리거 발생 노드 결정
        tree_fill_nodes[trigger_node_index].leaf_counter += 1   # 해당 리프 노드 카운터 값 증가
        if (tree_fill_nodes[trigger_node_index].leaf_counter == leaf_threshold):            # 리프 노드 카운터 값이 threshold에 이르면
            tree_fill_nodes[trigger_node_index].leaf_counter = 0                            # 리프 노드 카운터 초기화
            sender = tree_fill_nodes[trigger_node_index]
            dt_leaf_node_index = random.randrange(0, pow(2, detect_tree_depth - 1))         # 코인을 받을 DetectTree의 리프 노드 결정
            dt_node_index = (pow(2, detect_tree_depth - 1) - 1) + dt_leaf_node_index
            receiver = tree_fill_nodes[dt_node_index]
            message_count = message_sr(sender, receiver, message_count)                     # 코인 메시지 전달
            if not tree_fill_nodes[dt_node_index].left_full:
                tree_fill_nodes[dt_node_index].left_full = True
            elif not tree_fill_nodes[dt_node_index].right_full:
                tree_fill_nodes[dt_node_index].right_full = True
                receive_full(dt_node_index)
            else:
                receive_coin(dt_node_index, (dt_node_index - 1) // 2)
            if tree_fill_nodes[0].left_full and tree_fill_nodes[0].right_full:              # end-of-round 프로시저 시작 조건
                for d in range(0, detect_tree_depth - 1):                                   # end-of-round notification broadcast
                    for i in range(0, pow(2, d)):
                        sender = tree_fill_nodes[(pow(2, d) - 1) + i]                       # 부모 노드
                        receiver = tree_fill_nodes[(pow(2, d + 1) - 1) + (i * 2)]           # 왼쪽 자식 노드
                        message_count = message_sr(sender, receiver, message_count)         # 왼쪽 자식 노드에게 notification 전달
                        receiver = tree_fill_nodes[(pow(2, d + 1) - 1) + (i * 2) + 1]       # 오른쪽 자식 노드
                        message_count = message_sr(sender, receiver, message_count)         # 오른쪽 자식 노드에게 notification 전달
                message_count = message_sr(tree_fill_nodes[0], tree_fill_nodes[num_of_nodes - 1], message_count)    # internal 노드에 포함되지 않은 노드
                for d in range(0, detect_tree_depth - 1):                                # end-of-round upcast
                    for i in range(0, pow(2, d)):
                        receiver = tree_fill_nodes[(pow(2, d) - 1) + i]                     # 부모 노드
                        sender = tree_fill_nodes[(pow(2, d + 1) - 1) + (i * 2)]             # 왼쪽 자식 노드
                        message_count = message_sr(sender, receiver, message_count)         # 왼쪽 자식 노드의 트리거 및 코인 수 전달
                        sender = tree_fill_nodes[(pow(2, d + 1) - 1) + (i * 2) + 1]         # 오른쪽 자식 노드
                        message_count = message_sr(sender, receiver, message_count)         # 오른쪽 자식 노드의 트리거 및 코인 수 전달
                message_count = message_sr(tree_fill_nodes[num_of_nodes - 1], tree_fill_nodes[0], message_count)    # internal 노드에 포함되지 않은 노드
                w = w - trigger
                #print(f"2nd Phase: {round:2d} 라운드 끝, 발생 트리거: {trigger:6d}, 남은 트리거: {w:6d}, 현재 message complexity: {message_count:6d}")
                trigger = 0
                for c in range(0, num_of_nodes):
                    tree_fill_nodes[c].clear()
                break

# Third Phase (w < n일 때)
while (w != 0):
    round += 1                                                  # 새로운 라운드 시작
    leaf_threshold = 1                                          # 리프 노드 threshold 값 = 1
    for c in range(0, num_of_nodes - w):
        trigger_node_index = random.randrange(0, num_of_nodes)  # 트리거 발생 노드 결정
        sender = tree_fill_nodes[trigger_node_index]
        dt_leaf_node_index = random.randrange(0, pow(2, detect_tree_depth - 1))         # 코인을 받을 DetectTree의 리프 노드 결정
        dt_node_index = (pow(2, detect_tree_depth - 1) - 1) + dt_leaf_node_index
        receiver = tree_fill_nodes[dt_node_index]
        message_count = message_sr(sender, receiver, message_count)                     # 코인 메시지 전달
        if not tree_fill_nodes[dt_node_index].left_full:
            tree_fill_nodes[dt_node_index].left_full = True
        elif not tree_fill_nodes[dt_node_index].right_full:
            tree_fill_nodes[dt_node_index].right_full = True
            receive_full(dt_node_index)
        else:
            receive_coin(dt_node_index, (dt_node_index - 1) // 2)
    while (True):
        trigger += 1                                            # 트리거 발생
        trigger_node_index = random.randrange(0, num_of_nodes)  # 트리거 발생 노드 결정
        tree_fill_nodes[trigger_node_index].leaf_counter += 1   # 해당 리프 노드 카운터 값 증가
        if (tree_fill_nodes[trigger_node_index].leaf_counter == leaf_threshold):            # 리프 노드 카운터 값이 threshold에 이르면
            tree_fill_nodes[trigger_node_index].leaf_counter = 0                            # 리프 노드 카운터 초기화
            sender = tree_fill_nodes[trigger_node_index]
            dt_leaf_node_index = random.randrange(0, pow(2, detect_tree_depth - 1))         # 코인을 받을 DetectTree의 리프 노드 결정
            dt_node_index = (pow(2, detect_tree_depth - 1) - 1) + dt_leaf_node_index
            receiver = tree_fill_nodes[dt_node_index]
            message_count = message_sr(sender, receiver, message_count)                     # 코인 메시지 전달
            if not tree_fill_nodes[dt_node_index].left_full:
                tree_fill_nodes[dt_node_index].left_full = True
            elif not tree_fill_nodes[dt_node_index].right_full:
                tree_fill_nodes[dt_node_index].right_full = True
                receive_full(dt_node_index)
            else:
                receive_coin(dt_node_index, (dt_node_index - 1) // 2)
            if tree_fill_nodes[0].left_full and tree_fill_nodes[0].right_full:              # end-of-round 프로시저 시작 조건
                for d in range(0, detect_tree_depth - 1):                                   # end-of-round notification broadcast
                    for i in range(0, pow(2, d)):
                        sender = tree_fill_nodes[(pow(2, d) - 1) + i]                       # 부모 노드
                        receiver = tree_fill_nodes[(pow(2, d + 1) - 1) + (i * 2)]           # 왼쪽 자식 노드
                        message_count = message_sr(sender, receiver, message_count)         # 왼쪽 자식 노드에게 notification 전달
                        receiver = tree_fill_nodes[(pow(2, d + 1) - 1) + (i * 2) + 1]       # 오른쪽 자식 노드
                        message_count = message_sr(sender, receiver, message_count)         # 오른쪽 자식 노드에게 notification 전달
                message_count = message_sr(tree_fill_nodes[0], tree_fill_nodes[num_of_nodes - 1], message_count)    # internal 노드에 포함되지 않은 노드
                for d in range(0, detect_tree_depth - 1):                                # end-of-round upcast
                    for i in range(0, pow(2, d)):
                        receiver = tree_fill_nodes[(pow(2, d) - 1) + i]                     # 부모 노드
                        sender = tree_fill_nodes[(pow(2, d + 1) - 1) + (i * 2)]             # 왼쪽 자식 노드
                        message_count = message_sr(sender, receiver, message_count)         # 왼쪽 자식 노드의 트리거 및 코인 수 전달
                        sender = tree_fill_nodes[(pow(2, d + 1) - 1) + (i * 2) + 1]         # 오른쪽 자식 노드
                        message_count = message_sr(sender, receiver, message_count)         # 오른쪽 자식 노드의 트리거 및 코인 수 전달
                message_count = message_sr(tree_fill_nodes[num_of_nodes - 1], tree_fill_nodes[0], message_count)    # internal 노드에 포함되지 않은 노드
                w = w - trigger
                #print(f"3rd Phase: {round:2d} 라운드 끝, 발생 트리거: {trigger:6d}, 남은 트리거: {w:6d}, 현재 message complexity: {message_count:6d}")
                trigger = 0
                for c in range(0, num_of_nodes):
                    tree_fill_nodes[c].clear()
                break

maxSnd = 0
maxRcv = 0
for c in range(0, num_of_nodes):
    if (maxSnd < tree_fill_nodes[c].send_message):
        maxSnd = tree_fill_nodes[c].send_message
    if (maxRcv < tree_fill_nodes[c].receive_message):
        maxRcv = tree_fill_nodes[c].receive_message

# print(f"maxSend: {maxSnd}, maxRcv: {maxRcv}, message complexity: {message_count:6d}")
print(message_count, "\t", maxRcv, "\t", round)