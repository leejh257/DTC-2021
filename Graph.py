import matplotlib.pyplot as plt

x = [16, 64, 256, 1024, 4096]                   # Number of Nodes
cr0 = [1784, 6534.8, 21774.1, 72626.1, 222397]  # CoinRand Message Complexity
cr1 = [161.8, 147.9, 128.8, 116.3, 100.3]       # CoinRand MaxRcv
cr2 = [38.7, 35.2, 31, 27.4, 24.6]              # CoinRand Round
cr = [cr0, cr1, cr2]                            # CoinRand
tf0 = [1252.6, 5051.8, 17181.6, 60757, 205928]  # TreeFill Message Complexity
tf1 = [118.5, 138.6, 166, 251.6, 381.5]         # TreeFill MaxRcv
tf2 = [15.5, 13.4, 10.7, 9.1, 7.6]              # TreeFill Round
tf = [tf0, tf1, tf2]                            # TreeFill
pa0 = [874.9, 3025.9, 10987.8, 39342.5, 138992] # Proposed Algorithm Message Complexity
pa1 = [82.1, 78.5, 76.5, 96.1, 141.6]           # Proposed Algorithm MaxRcv
pa2 = [21.1, 18.2, 16.9, 15.5, 14.1]            # Proposed Algorithm Round
pa = [pa0, pa1, pa2]                            # Proposed Algorithm
ylabel0 = 'Message complexity'
ylabel1 = 'MaxRcv'
ylabel2 = 'Number of rounds'
ylabels = [ylabel0, ylabel1, ylabel2]
ylimits = [250000, 400, 40]

index = 0   # Message Complexity: 0, MaxRcv: 1, Round: 2
#index = 1  # Message Complexity: 0, MaxRcv: 1, Round: 2
#index = 2  # Message Complexity: 0, MaxRcv: 1, Round: 2

plt.plot(x, cr[index], 'kx:', label='CoinRand')
plt.plot(x, tf[index], 'k+--', label='TreeFill')
plt.plot(x, pa[index], 'ko-', label='Proposed algorithm')
plt.xscale('symlog')
plt.yscale('linear')
plt.xlabel('Number of nodes')
plt.ylabel(ylabels[index])
plt.xlim([8, 8192])
plt.ylim([0, ylimits[index]])
plt.legend(loc='best')
plt.grid(True)
plt.xticks(x, labels=x)
plt.show()