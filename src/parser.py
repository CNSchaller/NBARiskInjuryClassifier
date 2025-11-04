import pandas as pd

def loadFile():
    df = pd.read_csv('data/InjuryStats.csv')
    return df

df1 = loadFile()
print(df1.head())
