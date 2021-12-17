import math
import random

# 실험 매개변수 선언
# num_of_nodes = pow(2, 10)       # 전체 노드 수 n (2의 제곱승으로 가정)
# num_of_triggers = pow(2, 20)    # 검출하고자 하는 트리거 개수 w
num_of_nodes = pow(2, 12)
num_of_triggers = 1000000

# 제안 기법 매개변수 계산
sqrt_tree_degree = int(math.sqrt(num_of_nodes))         # 계층 1의 노드 수 (트리 깊이는 2)
aggregation_tree_depth = int(math.log2(num_of_nodes))   # aggregation 트리 높이 L

# 제안 기법 노드 클래스 정의
class SqrtNode:
    def __init__(self, node_num):
        # 전체 노드 정보
        self.node_num = node_num    # 노드 번호 in [0, n)
        self.send_message = 0       # 보낸 메시지 수
        self.receive_message = 0    # 받은 메시지 수

        # leaf 노드 정보
        self.leaf_counter = 0       # leaf 노드 카운터

        # internal 노드 정보
        self.internal_counter = 0   # 내부 노드 카운터
    
    def send(self):
        self.send_message += 1

    def receive(self):
        self.receive_message += 1
    
    def clear(self):
        self.leaf_counter = 0       # leaf 노드 카운터
        self.internal_counter = 0   # 내부 노드 카운터

# 제안 기법 트리 클래스 정의 (리프 노드 제외, 라운드 로빈 방식으로 돌아가며 사용)
class SqrtTree:
    current_node = 0

    @classmethod
    def increase_current_node(cls):
        cls.current_node += 1
        if (cls.current_node == num_of_nodes):
                cls.current_node = 0
    
    def __init__(self):
        self.root = SqrtTree.current_node
        SqrtTree.increase_current_node()
        self.layer_1 = []
        c = 0
        while (c < sqrt_tree_degree):
            self.layer_1.append(SqrtTree.current_node)
            SqrtTree.increase_current_node()
            c += 1

# 메시지 전송 함수
def message_sr(sender, receiver, count):
    sender.send()
    receiver.receive()
    return count + 1

# 제안 기법 트리 초기화
sqrt_nodes = []                                     # 전체 노드 집합 초기화
for c in range(num_of_nodes):
    node = SqrtNode(c)                              # 노드 생성
    sqrt_nodes.append(node)                         # 전체 노드 집합에 노드 추가

# 실험 시작
w = num_of_triggers             # 검출하고자 하는 트리거 개수 w 초기화
trigger = 0                     # 현재까지 발생한 트리거의 수 trigger 초기화
round = 0                       # 라운드 초기화
message_count = 0               # 전체 메시지 수

# First Phase (w >= 2n일 때)
while (w >= num_of_nodes * 2):
    round += 1                                                  # 새로운 라운드 시작
    leaf_threshold = math.floor(w / (2 * num_of_nodes))         # 리프 노드 threshold 값 계산
    internal_threshold = math.floor(sqrt_tree_degree / 2)       # 내부 노드 threshold 값 계산
    sqrt_tree = SqrtTree()
    while (True):
        trigger += 1                                            # 트리거 발생
        trigger_node_index = random.randrange(0, num_of_nodes)  # 트리거 발생 노드 결정
        sqrt_nodes[trigger_node_index].leaf_counter += 1        # 해당 리프 노드 카운터 값 증가
        if (sqrt_nodes[trigger_node_index].leaf_counter == leaf_threshold):                 # 리프 노드 카운터 값이 threshold에 이르면
            sqrt_nodes[trigger_node_index].leaf_counter = 0                                 # 리프 노드 카운터 초기화
            sender = sqrt_nodes[trigger_node_index]
            sqrt_index = random.randrange(0, sqrt_tree_degree)                              # 코인 추가 노드 결정
            receiver = sqrt_nodes[sqrt_tree.layer_1[sqrt_index]]                            # 코인 추가 내부 노드
            message_count = message_sr(sender, receiver, message_count)                     # 코인 메시지 전달
            sqrt_nodes[sqrt_tree.layer_1[sqrt_index]].internal_counter += 1                 # 해당 내부 노드 카운터 값 증가
            if (sqrt_nodes[sqrt_tree.layer_1[sqrt_index]].internal_counter == internal_threshold):  # 내부 노드 카운터 값이 threshold에 이르면
                sqrt_nodes[sqrt_tree.layer_1[sqrt_index]].internal_counter = 0                      # 내부 노드 카운터 초기화
                sender = sqrt_nodes[sqrt_tree.layer_1[sqrt_index]]
                receiver = sqrt_nodes[sqrt_tree.root]
                message_count = message_sr(sender, receiver, message_count)                         # 내부 노드에서 루트 노드로 코인 메시지 전달
                sqrt_nodes[sqrt_tree.root].internal_counter += 1                                    # 루트 노드 카운터 값 증가
                if (sqrt_nodes[sqrt_tree.root].internal_counter == sqrt_tree_degree):               # end-of-round 프로시저 시작 조건
                    for d in range(0, aggregation_tree_depth - 1):                                  # end-of-round notification broadcast
                        for i in range(0, pow(2, d)):
                            sender = sqrt_nodes[(pow(2, d) - 1) + i]                                # 부모 노드
                            receiver = sqrt_nodes[(pow(2, d + 1) - 1) + (i * 2)]                    # 왼쪽 자식 노드
                            message_count = message_sr(sender, receiver, message_count)             # 왼쪽 자식 노드에게 notification 전달
                            receiver = sqrt_nodes[(pow(2, d + 1) - 1) + (i * 2) + 1]                # 오른쪽 자식 노드
                            message_count = message_sr(sender, receiver, message_count)             # 오른쪽 자식 노드에게 notification 전달
                    message_count = message_sr(sqrt_nodes[0], sqrt_nodes[num_of_nodes - 1], message_count)  # aggregation tree에 포함되지 않은 노드
                    for d in range(0, aggregation_tree_depth - 1):                                  # end-of-round upcast
                        for i in range(0, pow(2, d)):
                            receiver = sqrt_nodes[(pow(2, d) - 1) + i]                              # 부모 노드
                            sender = sqrt_nodes[(pow(2, d + 1) - 1) + (i * 2)]                      # 왼쪽 자식 노드
                            message_count = message_sr(sender, receiver, message_count)             # 왼쪽 자식 노드의 트리거 및 코인 수 전달
                            sender = sqrt_nodes[(pow(2, d + 1) - 1) + (i * 2) + 1]                  # 오른쪽 자식 노드
                            message_count = message_sr(sender, receiver, message_count)             # 오른쪽 자식 노드의 트리거 및 코인 수 전달
                    message_count = message_sr(sqrt_nodes[num_of_nodes - 1], sqrt_nodes[0], message_count)  # aggregation tree에 포함되지 않은 노드
                    w = w - trigger
                    # print(f"1st Phase: {round:2d} 라운드 끝, 발생 트리거: {trigger:6d}, 남은 트리거: {w:6d}, 현재 message complexity: {message_count:6d}")
                    trigger = 0
                    for c in range(0, num_of_nodes):
                        sqrt_nodes[c].clear()
                    break

# Second Phase (2k <= w < 2n일 때)
while (w >= sqrt_tree_degree * 2):
    round += 1                                                  # 새로운 라운드 시작
    leaf_threshold = 1                                          # 2nd Phase의 리프 노드 threshold 값은 1
    internal_threshold = math.floor(w / (sqrt_tree_degree * 2)) # 내부 노드 threshold 값 계산
    sqrt_tree = SqrtTree()
    while (True):
        trigger += 1                                            # 트리거 발생
        trigger_node_index = random.randrange(0, num_of_nodes)  # 트리거 발생 노드 결정
        sqrt_nodes[trigger_node_index].leaf_counter += 1        # 해당 리프 노드 카운터 값 증가
        if (sqrt_nodes[trigger_node_index].leaf_counter == leaf_threshold):                 # 리프 노드 카운터 값이 threshold에 이르면
            sqrt_nodes[trigger_node_index].leaf_counter = 0                                 # 리프 노드 카운터 초기화
            sender = sqrt_nodes[trigger_node_index]
            sqrt_index = random.randrange(0, sqrt_tree_degree)                              # 코인 추가 노드 결정
            receiver = sqrt_nodes[sqrt_tree.layer_1[sqrt_index]]                            # 코인 추가 내부 노드
            message_count = message_sr(sender, receiver, message_count)                     # 코인 메시지 전달
            sqrt_nodes[sqrt_tree.layer_1[sqrt_index]].internal_counter += 1                 # 해당 내부 노드 카운터 값 증가
            if (sqrt_nodes[sqrt_tree.layer_1[sqrt_index]].internal_counter == internal_threshold):  # 내부 노드 카운터 값이 threshold에 이르면
                sqrt_nodes[sqrt_tree.layer_1[sqrt_index]].internal_counter = 0                      # 내부 노드 카운터 초기화
                sender = sqrt_nodes[sqrt_tree.layer_1[sqrt_index]]
                receiver = sqrt_nodes[sqrt_tree.root]
                message_count = message_sr(sender, receiver, message_count)                         # 내부 노드에서 루트 노드로 코인 메시지 전달
                sqrt_nodes[sqrt_tree.root].internal_counter += 1                                    # 루트 노드 카운터 값 증가
                if (sqrt_nodes[sqrt_tree.root].internal_counter == sqrt_tree_degree):               # end-of-round 프로시저 시작 조건
                    for d in range(0, aggregation_tree_depth - 1):                                  # end-of-round notification broadcast
                        for i in range(0, pow(2, d)):
                            sender = sqrt_nodes[(pow(2, d) - 1) + i]                                # 부모 노드
                            receiver = sqrt_nodes[(pow(2, d + 1) - 1) + (i * 2)]                    # 왼쪽 자식 노드
                            message_count = message_sr(sender, receiver, message_count)             # 왼쪽 자식 노드에게 notification 전달
                            receiver = sqrt_nodes[(pow(2, d + 1) - 1) + (i * 2) + 1]                # 오른쪽 자식 노드
                            message_count = message_sr(sender, receiver, message_count)             # 오른쪽 자식 노드에게 notification 전달
                    message_count = message_sr(sqrt_nodes[0], sqrt_nodes[num_of_nodes - 1], message_count)  # aggregation tree에 포함되지 않은 노드
                    for d in range(0, aggregation_tree_depth - 1):                                  # end-of-round upcast
                        for i in range(0, pow(2, d)):
                            receiver = sqrt_nodes[(pow(2, d) - 1) + i]                              # 부모 노드
                            sender = sqrt_nodes[(pow(2, d + 1) - 1) + (i * 2)]                      # 왼쪽 자식 노드
                            message_count = message_sr(sender, receiver, message_count)             # 왼쪽 자식 노드의 트리거 및 코인 수 전달
                            sender = sqrt_nodes[(pow(2, d + 1) - 1) + (i * 2) + 1]                  # 오른쪽 자식 노드
                            message_count = message_sr(sender, receiver, message_count)             # 오른쪽 자식 노드의 트리거 및 코인 수 전달
                    message_count = message_sr(sqrt_nodes[num_of_nodes - 1], sqrt_nodes[0], message_count)  # aggregation tree에 포함되지 않은 노드
                    w = w - trigger
                    # print(f"2nd Phase: {round:2d} 라운드 끝, 발생 트리거: {trigger:6d}, 남은 트리거: {w:6d}, 현재 message complexity: {message_count:6d}")
                    trigger = 0
                    for c in range(0, num_of_nodes):
                        sqrt_nodes[c].clear()
                    break

# Third Phase (w < 2k일 때)
round += 1                                                  # 새로운 라운드 시작
sqrt_tree = SqrtTree()
while (w > 0):
    trigger += 1                                            # 트리거 발생
    trigger_node_index = random.randrange(0, num_of_nodes)  # 트리거 발생 노드 결정
    sender = sqrt_nodes[trigger_node_index]
    receiver = sqrt_nodes[sqrt_tree.root]
    message_count = message_sr(sender, receiver, message_count) # 트리거 메시지 루트에게 직접 전달
    w -= 1
# print(f"3rd Phase: {round:2d} 라운드 끝, 발생 트리거: {trigger:6d}, 남은 트리거: {w:6d}, 현재 message complexity: {message_count:6d}")

maxSnd = 0
maxRcv = 0
for c in range(0, num_of_nodes):
    if (maxSnd < sqrt_nodes[c].send_message):
        maxSnd = sqrt_nodes[c].send_message
    if (maxRcv < sqrt_nodes[c].receive_message):
        maxRcv = sqrt_nodes[c].receive_message

# print(f"maxSend: {maxSnd}, maxRcv: {maxRcv}, message complexity: {message_count:6d}")
print(message_count, "\t", maxRcv, "\t", round)