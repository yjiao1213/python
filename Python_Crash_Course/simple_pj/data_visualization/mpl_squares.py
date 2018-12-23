import matplotlib.pyplot as plt
import math

input_values = [1, 2, 3, 4, 5]
squares = [1, 4, 9, 16, 25]
#
# plt.plot(input_values, squares, linewidth=5)
# # 设置图表标题，并给坐标轴加上标签
# plt.title("Square Numbers", fontsize=24)
# plt.xlabel("Value", fontsize=14)
# plt.ylabel("Square of Value", fontsize=14)
# # 设置刻度标记的大小
# plt.tick_params(axis='both', labelsize=14)
# plt.show()


x_values = list(range(1,1000))
y_values = [x**2 for x in x_values ]

x_valuesss = list(range(1, 5000))
y_valuesss = [math.pow(x, 3) for x in x_valuesss]
plt.scatter(x_valuesss[0:4999], y_valuesss[0:4999], c=y_valuesss[0:4999], cmap=plt.cm.Blues, edgecolor='none', s = 10)
# 设置图表标题并给坐标轴加上标签
plt.title("Square Numbers", fontsize=24)
plt.xlabel("Value", fontsize=14)
plt.ylabel("Square of Value", fontsize=14)
# 设置刻度标记的大小
plt.tick_params(axis='both', which='major', labelsize=14)
# 设置每个坐标轴的取值范围
#plt.axis([0, 6, 0, 200])
#plt.savefig('squares_plot.png', bbox_inches='tight')
plt.show()
