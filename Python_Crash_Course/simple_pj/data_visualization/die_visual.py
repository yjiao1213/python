import pygal
from die import Die

# die_1 = Die()
#
# # 掷几次骰子，并将结果存储在一个列表中
# results = []
# for roll_num in range(1000):
#     result = die_1.roll()
#     results.append(result)
#
# #分析结果
# frequencies = []
#
# for value in range(1, die_1.num_sides + 1):
#     frequencies.append(results.count(value))
# print(frequencies)
#
# # 使用pygal可视化
# hist = pygal.Bar()
#
# hist.title = "Results of rolling one D6 1000 times."
# hist.x_labels = ['1', '2', '3', '4', '5', '6']
# hist.x_title = "Result"
# hist.y_title = "Frequency of Result"
#
# hist.add('D6', frequencies)
# hist.render_to_file('die_visual.svg')

die_1 = Die()
die_2 = Die()

# 掷骰子多次，并将结果存储到一个列表中
result = []
for _ in range(1000):
    add_value = die_1.roll() + die_2.roll()
    result.append(add_value)

# 结果分析
frequencies = []
max_result = die_1.num_sides + die_2.num_sides
for value in range(2, max_result+1):
    frequency = result.count(value)
    frequencies.append(frequency)

# 可视化结果
hist = pygal.Bar()
hist.title = "Results of rolling two D6 dice 1000 times."
hist.x_labels = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
hist.x_title = "Result"
hist.y_title = "Frequency of Result"
hist.add('D6 + D6', frequencies)
hist.render_to_file('dice_visual.svg')
