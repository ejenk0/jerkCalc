from numpy import average, polyfit
import pandas
import os
from sympy import *

dirs = os.listdir("Data/Videos")

try:
    dirs.remove(".DS_Store")
except ValueError:
    pass

df = pandas.DataFrame(columns=["Trial", "Jerk", "Error"])

for dir in sorted(dirs, key=lambda x: int(x[:-2])):
    jerks = []
    for f in filter(lambda x: x[-4:] == ".csv", os.listdir("Data/Videos/" + dir)):
        data = pandas.read_csv("Data/Videos/" + dir + "/" + f)
        x = data["VideoAnalysis: Time (s)"]
        y = data["VideoAnalysis: X Velocity (m/s)"]
        fit = polyfit(x, y, 2)
        jerk = 2 * fit[0]
        jerks.append(jerk)
    avgjerk = round(average(jerks), 2)
    error = round((max(jerks) - min(jerks)) / 2, 2)
    df = df.append({"Trial": dir, "Jerk": avgjerk, "Error": error}, ignore_index=True)

print(df)

df.to_excel("jerk.xlsx")
