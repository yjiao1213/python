import csv
from matplotlib import pyplot as plt
from datetime import datetime

filename = 'death_valley_2014.csv'

# 获取最高气温
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    # for index, column_header in enumerate(header_row):
    #     print(index, column_header)
    date, high, low = [], [], []
    for row in reader:
        try:
            date1 = datetime.strptime(row[0], '%Y-%m-%d')
            high1 = int(row[1])
            low1 = int(row[3])
        except ValueError:
            print(date1, 'missing data')
        else:
            date.append(date1)
            high.append(high1)
            low.append(low1)


fig = plt.figure(dpi=128, figsize=(10, 6))
plt.plot(date, high, c='red', alpha=0.5)
plt.plot(date, low, c='blue', alpha=0.5)
plt.fill_between(date, low, high, facecolor='blue', alpha=0.1)
plt.title("Daily high and low temperatures - 2014\nDeath Valley, CA", fontsize=24)
plt.xlabel('', fontsize=16)
fig.autofmt_xdate()
plt.ylabel("Temperature (F)", fontsize=16)
plt.ylim([0, 90])
plt.tick_params(axis='both', which='major', labelsize=16)
plt.show()

