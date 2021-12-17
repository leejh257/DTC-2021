import matplotlib.pyplot as plt

x = [16, 64, 256, 1024, 4096]
cr0 = [1784, 6534.8, 21774.1, 72626.1, 222397]
cr1 = [161.8, 147.9, 128.8, 116.3, 100.3]
cr2 = [38.7, 35.2, 31, 27.4, 24.6]
cr = [cr0, cr1, cr2]
pm0 = [874.9, 3025.9, 10987.8, 39342.5, 138992]
pm1 = [82.1, 78.5, 76.5, 96.1, 141.6]
pm2 = [21.1, 18.2, 16.9, 15.5, 14.1]
pm = [pm0, pm1, pm2]
ylabel0 = 'Message complexity'
ylabel1 = 'MaxRcv'
ylabel2 = 'Number of rounds'
ylabels = [ylabel0, ylabel1, ylabel2]
ylimits = [250000, 180, 40]

index = 0   # Message Complexity: 0, MaxRcv: 1, Round: 2

plt.plot(x, cr[index], 'kx--', label='CoinRand')
plt.plot(x, pm[index], 'ko-', label='Proposed algorithm')
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