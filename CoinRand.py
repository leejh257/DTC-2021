import math
import random

# 실험 매개변수 선언
# num_of_nodes = pow(2, 10)       # 전체 노드 개수 n (2의 제곱승으로 가정)
# num_of_triggers = pow(2, 20)    # 검출하고자 하는 트리거 개수 w
num_of_nodes = pow(2, 12)
num_of_triggers = 1000000

# CoinRand 매개변수 계산
coin_rand_tree_depth = int(math.log2(num_of_nodes)) # CoinRand 트리 높이 L

# CoinRand 노드 클래스 정의
class CoinRandNode:
    def __init__(self, node_num):
        # 전체 노드 정보
        self.node_num = node_num    # 노드 번호 in [0, n)
        self.send_message = 0       # 보낸 메시지 수
        self.receive_message = 0    # 받은 메시지 수

        # leaf 노드 정보
        self.leaf_counter = 0       # leaf 노드 카운터

        # internal 노드 정보
        self.layer = None           # internal 노드 layer in [0, L), 0이 루트 노드
        self.layer_index = None     # 해당 layer에서의 노드 순서 in [0, 2^layer)
        self.coin_received = False  # 코인 수신 여부
    
    def send(self):
        self.send_message += 1

    def receive(self):
        self.receive_message += 1
    
    def clear(self):
        self.leaf_counter = 0       # leaf 노드 카운터
        self.coin_received = False  # 코인 수신 여부

# 메시지 전송 함수
def message_sr(sender, receiver, count):
    sender.send()
    receiver.receive()
    return count + 1

# CoinRand 트리 초기화
coin_rand_nodes = []                                # 전체 노드 집합 초기화
for c in range(num_of_nodes):
    node = CoinRandNode(c)                          # 노드 생성
    node.layer = int(math.log2(c+1))                # 노드 layer 계산
    node.layer_index = c - (pow(2, node.layer) - 1) # 해당 layer에서의 노드 순서 계산
    coin_rand_nodes.append(node)                    # 전체 노드 집합에 노드 추가

# 실험 시작
w = num_of_triggers             # 검출하고자 하는 트리거 개수 w 초기화
trigger = 0                     # 현재까지 발생한 트리거의 수 trigger 초기화
round = 0                       # 라운드 초기화
message_count = 0               # 전체 메시지 수

# First Phase (w >= n일 때)
while (w >= num_of_nodes):
    round += 1                                                  # 새로운 라운드 시작
    leaf_threshold = math.ceil(w / (4 * num_of_nodes))          # 리프 노드 threshold 값 계산
    while (True):
        trigger += 1                                            # 트리거 발생
        trigger_node_index = random.randrange(0, num_of_nodes)  # 트리거 발생 노드 결정
        coin_rand_nodes[trigger_node_index].leaf_counter += 1   # 해당 리프 노드 카운터 값 증가
        if (coin_rand_nodes[trigger_node_index].leaf_counter == leaf_threshold):            # 리프 노드 카운터 값이 threshold에 이르면
            coin_rand_nodes[trigger_node_index].leaf_counter = 0                            # 리프 노드 카운터 초기화
            sender = coin_rand_nodes[trigger_node_index]
            for d in range(coin_rand_tree_depth - 1, -1, -1):                               # 트리를 리프 노드부터 루트 노드로 순회
                coin_node_index = random.randrange(0, pow(2, d))                            # 코인 추가 노드 결정
                receiver = coin_rand_nodes[(pow(2, d) - 1) + coin_node_index]
                message_count = message_sr(sender, receiver, message_count)                 # 코인 메시지 전달
                if not coin_rand_nodes[(pow(2, d) - 1) + coin_node_index].coin_received:    # 코인을 전달할 노드에 이미 코인이 있는지 확인
                    coin_rand_nodes[(pow(2, d) - 1) + coin_node_index].coin_received = True # 코인이 없을 경우 코인 추가
                    break
                sender = coin_rand_nodes[(pow(2, d) - 1) + coin_node_index]                 # 코인이 있을 경우 상위 layer로 코인 메시지 전송
            if (coin_rand_nodes[0].coin_received):                                          # end-of-round 프로시저 시작 조건
                for d in range(0, coin_rand_tree_depth - 1):                                # end-of-round notification broadcast
                    for i in range(0, pow(2, d)):
                        sender = coin_rand_nodes[(pow(2, d) - 1) + i]                       # 부모 노드
                        receiver = coin_rand_nodes[(pow(2, d + 1) - 1) + (i * 2)]           # 왼쪽 자식 노드
                        message_count = message_sr(sender, receiver, message_count)         # 왼쪽 자식 노드에게 notification 전달
                        receiver = coin_rand_nodes[(pow(2, d + 1) - 1) + (i * 2) + 1]       # 오른쪽 자식 노드
                        message_count = message_sr(sender, receiver, message_count)         # 오른쪽 자식 노드에게 notification 전달
                message_count = message_sr(coin_rand_nodes[0], coin_rand_nodes[num_of_nodes - 1], message_count)    # internal 노드에 포함되지 않은 노드
                for d in range(0, coin_rand_tree_depth - 1):                                # end-of-round upcast
                    for i in range(0, pow(2, d)):
                        receiver = coin_rand_nodes[(pow(2, d) - 1) + i]                     # 부모 노드
                        sender = coin_rand_nodes[(pow(2, d + 1) - 1) + (i * 2)]             # 왼쪽 자식 노드
                        message_count = message_sr(sender, receiver, message_count)         # 왼쪽 자식 노드의 트리거 및 코인 수 전달
                        sender = coin_rand_nodes[(pow(2, d + 1) - 1) + (i * 2) + 1]         # 오른쪽 자식 노드
                        message_count = message_sr(sender, receiver, message_count)         # 오른쪽 자식 노드의 트리거 및 코인 수 전달
                message_count = message_sr(coin_rand_nodes[num_of_nodes - 1], coin_rand_nodes[0], message_count)    # internal 노드에 포함되지 않은 노드
                w = w - trigger
                # print(f"1st Phase: {round:2d} 라운드 끝, 발생 트리거: {trigger:6d}, 남은 트리거: {w:6d}, 현재 message complexity: {message_count:6d}")
                trigger = 0
                for c in range(0, num_of_nodes):
                    coin_rand_nodes[c].clear()
                break

# Second Phase (w < n일 때)
while (w > 0):
    for c in range(1, coin_rand_tree_depth):                                # k 계산: (L - k) layer의 트리 사용 예정
        if (num_of_nodes / pow(2, c) <= w < num_of_nodes / pow(2, c - 1)):
            k = c
            break
    round += 1                                                  # 새로운 라운드 시작
    leaf_threshold = 1                                          # 2nd Phase의 리프 노드 threshold 값은 1
    while (True):
        trigger += 1                                            # 트리거 발생
        trigger_node_index = random.randrange(0, num_of_nodes)  # 트리거 발생 노드 결정
        coin_rand_nodes[trigger_node_index].leaf_counter += 1   # 해당 리프 노드 카운터 값 증가
        if (coin_rand_nodes[trigger_node_index].leaf_counter == leaf_threshold):            # 리프 노드 카운터 값이 threshold에 이르면
            coin_rand_nodes[trigger_node_index].leaf_counter = 0                            # 리프 노드 카운터 초기화
            sender = coin_rand_nodes[trigger_node_index]
            for d in range(coin_rand_tree_depth - 1 - k, -1, -1):                           # 트리를 (L - k) layer의 노드부터 루트 노드로 순회
                coin_node_index = random.randrange(0, pow(2, d))                            # 코인 추가 노드 결정
                receiver = coin_rand_nodes[(pow(2, d) - 1) + coin_node_index]
                message_count = message_sr(sender, receiver, message_count)                 # 코인 메시지 전달
                if not coin_rand_nodes[(pow(2, d) - 1) + coin_node_index].coin_received:    # 코인을 전달할 노드에 이미 코인이 있는지 확인
                    coin_rand_nodes[(pow(2, d) - 1) + coin_node_index].coin_received = True # 코인이 없을 경우 코인 추가
                    break
                sender = coin_rand_nodes[(pow(2, d) - 1) + coin_node_index]                 # 코인이 있을 경우 상위 layer로 코인 메시지 전송
            if (coin_rand_nodes[0].coin_received):                                          # end-of-round 프로시저 시작 조건
                for d in range(0, coin_rand_tree_depth - 1 - k):                            # end-of-round notification broadcast (코인 수만 확인하면 됨)
                    for i in range(0, pow(2, d)):
                        sender = coin_rand_nodes[(pow(2, d) - 1) + i]                       # 부모 노드
                        receiver = coin_rand_nodes[(pow(2, d + 1) - 1) + (i * 2)]           # 왼쪽 자식 노드
                        message_count = message_sr(sender, receiver, message_count)         # 왼쪽 자식 노드에게 notification 전달
                        receiver = coin_rand_nodes[(pow(2, d + 1) - 1) + (i * 2) + 1]       # 오른쪽 자식 노드
                        message_count = message_sr(sender, receiver, message_count)         # 오른쪽 자식 노드에게 notification 전달
                for d in range(0, coin_rand_tree_depth - 1 - k):                            # end-of-round upcast (코인 수만 확인하면 됨)
                    for i in range(0, pow(2, d)):
                        receiver = coin_rand_nodes[(pow(2, d) - 1) + i]                     # 부모 노드
                        sender = coin_rand_nodes[(pow(2, d + 1) - 1) + (i * 2)]             # 왼쪽 자식 노드
                        message_count = message_sr(sender, receiver, message_count)         # 왼쪽 자식 노드의 코인 수 전달
                        sender = coin_rand_nodes[(pow(2, d + 1) - 1) + (i * 2) + 1]         # 오른쪽 자식 노드
                        message_count = message_sr(sender, receiver, message_count)         # 오른쪽 자식 노드의 코인 수 전달
                w = w - trigger
                # print(f"2nd Phase: {round:2d} 라운드 끝, 발생 트리거: {trigger:6d}, 남은 트리거: {w:6d}, 현재 message complexity: {message_count:6d}, 현재 k 값: {k:2d}")
                trigger = 0
                for c in range(0, num_of_nodes):
                    coin_rand_nodes[c].clear()
                break

maxSnd = 0
maxRcv = 0
for c in range(0, num_of_nodes):
    if (maxSnd < coin_rand_nodes[c].send_message):
        maxSnd = coin_rand_nodes[c].send_message
    if (maxRcv < coin_rand_nodes[c].receive_message):
        maxRcv = coin_rand_nodes[c].receive_message

# print(f"maxSend: {maxSnd}, maxRcv: {maxRcv}, message complexity: {message_count:6d}")
print(message_count, "\t", maxRcv, "\t", round)