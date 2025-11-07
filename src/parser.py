import pandas as pd
import numpy as np

###Loading data into dataframes

def loadFile(): #loads the file into pandas
    df = pd.read_csv('data/InjuryStats.csv')
    return df

###Cleaning data functions

def cleanData(df):
    print("\nCleaning data...")
    dropDoubleEntries(df)
    dropEmptyEntries(df)
    dropDuplicateEntries(df)

    reformatDates(df)
    combineColumns(df)
    dropAcquiredRelinquished(df)
    dropUnbalancedConsecutiveEntries(df1)
    combineEntries(df)
    dropUnbalancedEntries(df)
    addDaysOut(df)

    return

def dropDoubleEntries(df): #drop entries where theres a name in both acquired and relinquished columns
    double_entries = df['Acquired'].notnull() & df['Relinquished'].notnull()
    df.drop(df[double_entries].index, inplace=True)
    print("Dropped ", double_entries.sum(), " double entries.")
    return

def dropEmptyEntries(df): #drop entries where theres no name in either column, theres no date, or theres no team
    empty_entries = (
        (df['Acquired'].isnull() & df['Relinquished'].isnull()) |
        df['Date'].isnull() |
        df['Team'].isnull())
    df.drop(df[empty_entries].index, inplace=True)

    print("Dropped ", empty_entries.sum(), " empty entries.")
    return

def dropDuplicateEntries(df): #drop any duplicate entries (should be none but just incase)
    dropped_sum = df.duplicated().sum()
    df.drop_duplicates(inplace=True)
    
    print("Dropped ", dropped_sum, " duplicate entries")
    return

def reformatDates(df): #fix data types
    refomat_count = len(df['Date'])
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    print("Reformatted ", refomat_count, " entries.")
    return

def combineColumns(df): #combine acquired and relinquished columns, and make new player column
    #combine acquired and relinquished into one column
    df['Transaction'] = np.where(df['Acquired'].notna(), 'Acquired',
                                 np.where(df['Relinquished'].notna(), 'Relinquished', pd.NA))

    #make a new player column for players name
    df['Player'] = np.where(df['Acquired'].notna(), df['Acquired'],
                            np.where(df['Relinquished'].notna(), df['Relinquished'], pd.NA))

    #split entries with multiple players
    df['Player'] = df['Player'].str.split(' / ')
    exploded_df = df.explode('Player', ignore_index=True)
    #get rid of extra space at start of each name
    exploded_df['Player'] = exploded_df['Player'].str.strip()

    #make it inplace
    df.drop(df.index, inplace=True)
    for col in exploded_df.columns:
        df[col] = exploded_df[col]

    print("Combined 2 columns.")

def dropAcquiredRelinquished(df): #drop useless columns
    df.drop('Acquired', axis=1, inplace=True)
    df.drop('Relinquished', axis=1, inplace=True)

    print("Dropped 2 columns.")

def dropUnbalancedConsecutiveEntries(df):
    # Sort by player and date
    
    print(df.head())
    df.sort_values(['Player', 'Date'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    rows_to_drop = []
    
    # group by player and check for repeated activations/relinquishments
    for player, group in df.groupby('Player', sort=False):
        indices = group.index.tolist()
        transactions = group['Transaction'].tolist()
        
        # drop first entry if its an activation (messes with data down the line)
        if len(transactions) > 0 and transactions[0] == 'Acquired':
            rows_to_drop.append(indices[0])
        
        for i in range(len(transactions) - 1):
            current_txn = transactions[i]
            next_txn = transactions[i + 1]
            
            # two activations in a row, drop the second one
            if current_txn == 'Acquired' and next_txn == 'Acquired':
                rows_to_drop.append(indices[i + 1])
            
            # two relinquishes in a row, drop the first one
            elif current_txn == 'Relinquished' and next_txn == 'Relinquished':
                rows_to_drop.append(indices[i])
    
    # remove duplicates
    rows_to_drop = list(set(rows_to_drop))
    
    df.drop(rows_to_drop, inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    print(f"Dropped ", len(rows_to_drop), " unbalanced consecutive transactions.")
    return

def combineEntries(df): #combine entries for easier access, make dates activated/injured into same entry
    relinquished = df[df['Transaction'] == 'Relinquished'][['Player', 'Date']]
    relinquished = relinquished.rename(columns={'Date': 'Date Relinquished'})

    acquired = df[df['Transaction'] == 'Acquired'][['Player', 'Date']]
    acquired = acquired.rename(columns={'Date': 'Date Activated'})

    relinquished['count'] = relinquished.groupby('Player').cumcount()
    acquired['count'] = acquired.groupby('Player').cumcount()

    combined = pd.merge(relinquished, acquired, on=['Player', 'count'], how='left').drop(columns='count')

    df.drop(df.index, inplace=True)
    for col in combined.columns:
        df[col] = combined[col]
    
    df.dropna(axis=1, how='all', inplace=True)

def dropUnbalancedEntries(df): #drop entries that only have an activation or injury
    unbalanced = (df['Date Relinquished'].isnull() | df['Date Activated'].isnull())
    df.drop(df[unbalanced].index, inplace=True)
    return

def addDaysOut(df):
    df['Days Out'] = df['Date Activated'] - df['Date Relinquished']


###Debugging functions

def countDoubleEntries(df): #returns amount of entries that have a value in both the 'Acquired' and 'Relinquished' columns
    bad_entry = df[df['Acquired'].notnull() & df['Relinquished'].notnull()]
    bad_count = len(bad_entry)
    return bad_count

def countEmptyEntries(df): #returns amount of entries where there is no name in either acquired or relinquished, or Date or Team fields are empty
    bad_entry = df[(df['Acquired'].isnull() & df['Relinquished'].isnull()) |
                    df['Date'].isnull() |
                    df['Team'].isnull()]
    #print(bad_entry) #uncomment this to see the empty entries
    bad_count = len(bad_entry)
    return bad_count

def countDuplicateEntries(df): #returns the amount of duplicate entries
    return df.duplicated().sum()

def printBadEntries(df):
    print("\n")
    print("Amount of double entries: ", countDoubleEntries(df))
    print("Amount of empty entries: ", countEmptyEntries(df))
    print("Amount of duplicate entries: ", countDuplicateEntries(df))
    print("amount of empty values in Transaction: ", countEmptyTransaction(df))

def countEmptyTransaction(df):
    bad_entry = df[df['Transaction'].isnull()]
    bad_count = len(bad_entry)
    return bad_count

def countNegativeDays(df):
    neg_entries = df[(df['Days Out'] < pd.Timedelta(0))]
    print(neg_entries.head())
    return len(neg_entries)

df1 = loadFile()
cleanData(df1)

#df1.info()
print(df1.tail(60))