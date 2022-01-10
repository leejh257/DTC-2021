import matplotlib.pyplot as plt

x = [16, 64, 256, 1024, 4096]                               # Number of Nodes
cr0_10000 = [975.7, 3113.8, 9216.8, 21229.8, 45051.7]       # CoinRand Message Complexity (W = 10,000)
cr1_10000 = [90, 76.8, 65.4, 52.1, 48]                      # CoinRand MaxRcv (W = 10,000)
cr2_10000 = [22.5, 19.2, 17.2, 13.6, 12.5]                  # CoinRand Round (W = 10,000)
cr0_100000 = [1374.6, 4775, 15538.9, 44825.5, 138872.6]     # CoinRand Message Complexity (W = 100,000)
cr1_100000 = [125.2, 111.3, 97.2, 82.6, 72.4]               # CoinRand MaxRcv (W = 100,000)
cr2_100000 = [30.8, 26.1, 23.3, 20, 18.6]                   # CoinRand Round (W = 100,000)
cr0_1000000 = [1784, 6534.8, 21774.1, 72626.1, 222397]      # CoinRand Message Complexity (W = 1,000,000)
cr1_1000000 = [161.8, 147.9, 128.8, 116.3, 100.3]           # CoinRand MaxRcv (W = 1,000,000)
cr2_1000000 = [38.7, 35.2, 31, 27.4, 24.6]                  # CoinRand Round (W = 1,000,000)
cr_10000 = [cr0_10000, cr1_10000, cr2_10000]                # CoinRand (W = 10,000)
cr_100000 = [cr0_100000, cr1_100000, cr2_100000]            # CoinRand (W = 100,000)
cr_1000000 = [cr0_1000000, cr1_1000000, cr2_1000000]        # CoinRand (W = 1,000,000)
cr = [cr_10000, cr_100000, cr_1000000]                      # CoinRand
tf0_10000 = [740.2, 2748.2, 8617.2, 26814, 81243]           # TreeFill Message Complexity (W = 10,000)
tf1_10000 = [71.7, 77.6, 92.3, 118.6, 154.7]                # TreeFill MaxRcv (W = 10,000)
tf2_10000 = [9.2, 7.3, 5.3, 4, 3]                           # TreeFill Round (W = 10,000)
tf0_100000 = [989.6, 3575.6, 12901.2, 43326.4, 163159.2]    # TreeFill Message Complexity (W = 100,000)
tf1_100000 = [95.6, 100.4, 127.7, 183.3, 312.7]             # TreeFill MaxRcv (W = 100,000)
tf2_100000 = [12.1, 9.5, 8, 6.5, 6]                         # TreeFill Round (W = 100,000)
tf0_1000000 = [1252.6, 5051.8, 17181.6, 60757, 205928]      # TreeFill Message Complexity (W = 1,000,000)
tf1_1000000 = [118.5, 138.6, 166, 251.6, 381.5]             # TreeFill MaxRcv (W = 1,000,000)
tf2_1000000 = [15.5, 13.4, 10.7, 9.1, 7.6]                  # TreeFill Round (W = 1,000,000)
tf_10000 = [tf0_10000, tf1_10000, tf2_10000]                # TreeFill (W = 10,000)
tf_100000 = [tf0_100000, tf1_100000, tf2_100000]            # TreeFill (W = 100,000)
tf_1000000 = [tf0_1000000, tf1_1000000, tf2_1000000]        # TreeFill (W = 1,000,000)
tf = [tf_10000, tf_100000, tf_1000000]                      # TreeFill
pa0_10000 = [578.7, 1807, 6346.7, 22425.2, 57873.2]         # Proposed Algorithm Message Complexity (W = 10,000)
pa1_10000 = [56.1, 52.2, 53.6, 79.1, 124.3]                 # Proposed Algorithm MaxRcv (W = 10,000)
pa2_10000 = [14.2, 11.3, 10.3, 9.4, 6.8]                    # Proposed Algorithm Round (W = 10,000)
pa0_100000 = [729.2, 2617.5, 8509.8, 29416.1, 105199]       # Proposed Algorithm Message Complexity (W = 100,000)
pa1_100000 = [70.2, 66.9, 58.4, 85.7, 131.6]                # Proposed Algorithm MaxRcv (W = 100,000)
pa2_100000 = [17.7, 16, 13.4, 11.9, 11.1]                   # Proposed Algorithm Round (W = 100,000)
pa0_1000000 = [874.9, 3025.9, 10987.8, 39342.5, 138992]     # Proposed Algorithm Message Complexity (W = 1,000,000)
pa1_1000000 = [82.1, 78.5, 76.5, 96.1, 141.6]               # Proposed Algorithm MaxRcv (W = 1,000,000)
pa2_1000000 = [21.1, 18.2, 16.9, 15.5, 14.1]                # Proposed Algorithm Round (W = 1,000,000)
pa_10000 = [pa0_10000, pa1_10000, pa2_10000]                # Proposed Algorithm (W = 10,000)
pa_100000 = [pa0_100000, pa1_100000, pa2_100000]            # Proposed Algorithm (W = 100,000)
pa_1000000 = [pa0_1000000, pa1_1000000, pa2_1000000]        # Proposed Algorithm (W = 1,000,000)
pa = [pa_10000, pa_100000, pa_1000000]                      # Proposed Algorithm

ylabel0 = 'Message complexity'
ylabel1 = 'MaxRcv'
ylabel2 = 'Number of rounds'
ylabels = [ylabel0, ylabel1, ylabel2]
ylimits = [[90000, 160, 24], [180000, 320, 32], [250000, 400, 40]]

#index = 0  # Message Complexity: 0, MaxRcv: 1, Round: 2
#index = 1  # Message Complexity: 0, MaxRcv: 1, Round: 2
index = 2   # Message Complexity: 0, MaxRcv: 1, Round: 2

#num_of_nodes_index = 0     # 10,000: 0, 100,000: 1, 1,000,000: 2
#num_of_nodes_index = 1     # 10,000: 0, 100,000: 1, 1,000,000: 2
num_of_nodes_index = 2      # 10,000: 0, 100,000: 1, 1,000,000: 2

plt.plot(x, cr[num_of_nodes_index][index], 'kx:', label='CoinRand')
plt.plot(x, tf[num_of_nodes_index][index], 'k+--', label='TreeFill')
plt.plot(x, pa[num_of_nodes_index][index], 'ko-', label='Proposed algorithm')
plt.xscale('symlog')
plt.yscale('linear')
plt.xlabel('Number of nodes')
plt.ylabel(ylabels[index])
plt.xlim([8, 8192])
plt.ylim([0, ylimits[num_of_nodes_index][index]])
plt.legend(loc='best')
plt.grid(True)
plt.xticks(x, labels=x)
plt.show()