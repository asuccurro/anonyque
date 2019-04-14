import json, csv
import matplotlib.pyplot as plt
import pandas as pd

results = {}
with open('../votazioni4p0/final_valid.csv') as ifl:
    csvr = csv.reader(ifl, delimiter=',')
    l=0
    for row in csvr:
        if l < 1:
            mykeys = row
            for k in mykeys:
                results[k] = []
        else:
            for i,k in enumerate(mykeys):
                results[k] = results[k]+row[i].replace(', ',',').split(',')
        l+=1

for k in mykeys:
    print(pd.Series(results[k]).value_counts())
    pd.Series(results[k]).value_counts().plot('barh', rot=45, fontsize=6)
    plt.title(k)
    plt.xlabel("Voti")
    plt.savefig(f"../votazioni4p0/final_valid_{k}.png")
    

with open('../votazioni4p0/final_valid.json', 'w') as ofl:
    json.dump(results, ofl)
