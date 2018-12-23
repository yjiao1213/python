import pygal
from die import Die

die_1 = Die()
die_2 = Die(10)

# 掷骰子多次，并将结果存储到一个列表中
result = []
for _ in range(50000):
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
hist.title = "Results of rolling D6 and D10 dice 50000 times."
hist.x_labels = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
hist.x_title = "Result"
hist.y_title = "Frequency of Result"
hist.add('D6 + D10', frequencies)
hist.render_to_file('d6d10_visual.svg')