import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

"""
Data Processing - Another Mother

This file imports the enemy data of all 3 Mother games
from CSV, combines it into a single dataframe, then
regularizes the values to scale similarly and
fills in missing/NaN values (typically for stats that
exist in one game but not the others).
This is a batch-processing step to take the bulk of
the work before the human adjustments come in to balance
the data better for TTRPG conversion.
Data processing is done without regard for the way
stat effects, damage, etc. are calculated in-game. 

Code By Caves/CC -- thanks for checking it out! <3
"""

# read csv to dataframe and drop anything with a NaN val
# dropping NaN was easier than manually removing m3 chapter headers from CSV lol
def importAsDf(filepath):
    df = pd.read_csv(filepath)
    df = df.dropna()
    df.head()
    return df

#scale each game to a range of [0,1]
#so relative values are preserved when combining
def scaleSet(df):
    dfp = df.copy()
    dfp.drop(columns='Enemy Name', inplace=True)
    scaler = MinMaxScaler()
    scaler.fit(dfp)
    s = scaler.transform(dfp)
    dfs = pd.DataFrame(s, columns=dfp.columns.tolist())
    dfs.insert(loc=0, column='Enemy Name', value=df['Enemy Name'].values)
    return dfs
            

#fill holes in data with standard fill/interpolation
#while this is technically successful, it is currently
#unused due to the unique shape of the combined dataframe
#(for example, if a column was NaN for the span of an 
# entire game, it would fill with the lowest value in
# the next game). Not useful or helpful.
def fillerUp(df):
    dfout = df.interpolate()
    dfout.bfill(inplace=True)
    return dfout

#fill holes in data with linear regression
#TODO: stop it. get some help
def fillerUpRegression(df):
    return df
    

#create pandas dataframes for the 3 enemy datasets
cd = os.getcwd()
m1d = cd + "/Enemies M1.csv"
ebd = cd + "/Enemies EB.csv"
m3d = cd + "/Enemies M3.csv"
m1 = importAsDf(m1d)
eb = importAsDf(ebd)
m3 = importAsDf(m3d)

#regularize values for each game
m1s = scaleSet(m1)
ebs = scaleSet(eb)
m3s = scaleSet(m3)

#create a combination dataframe
all = pd.concat([m1s,ebs,m3s], ignore_index=True, keys=["m1","eb","m3"])

all_filled = fillerUp(all)
print(all_filled)


