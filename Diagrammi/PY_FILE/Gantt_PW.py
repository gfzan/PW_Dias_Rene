import matplotlib.pyplot as plt
fig, gnt = plt.subplots()
gnt.set_ylim(0, 50)
gnt.set_xlim(0, 160)
gnt.set_xlabel('seconds since start')
gnt.set_ylabel('Processor')
gnt.set_yticks([15, 25, 35])
gnt.set_yticklabels(['1', '2', '3'])
gnt.grid(True)
gnt.broken_barh([(40, 50)], (30, 9), facecolors =('tab:orange'))
gnt.broken_barh([(110, 10), (150, 10)], (10, 9),
                facecolors ='tab:blue')

gnt.broken_barh([(10, 50), (100, 20), (130, 10)], (20, 9),
                facecolors =('tab:red'))

plt.savefig("gantt1.png") 