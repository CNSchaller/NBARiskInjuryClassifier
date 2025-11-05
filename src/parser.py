import pandas as pd

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


df1 = loadFile()
printBadEntries(df1)
cleanData(df1)
printBadEntries(df1)


