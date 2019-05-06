#!/usr/bin/python3
# code made by [You](https://github.com/@you), YYYY.
import pandas as pd
import numpy as np


import other_module as om

def query_gcp(query):
    
    return pd.read_gbq(query, 
              project_id='gabinete-compartilhado',
              dialect='standard', 
              private_key='../notebooks/gabinete-compartilhado.json')

### Auxiliary functions ###

def Bold(text):
    """
    Takes a string and returns it bold.
    """
    return '\033[1m'+text+'\033[0m'


def unique(series):
    """
    Takes a pandas series as input and print all unique values, separated by comma.
    """
    u = series.unique()
    print(Bold(str(len(u)))+':'+',  '.join(sorted(u.astype(str))))

    
def map_unique(v):
    """
    Takes a pandas database and prints the unique values of all columns and their numbers.
    If the number of unique values is greater than maxItems, only print out a sample.  
    """
    for c in v.columns.values:
        maxItems = 20
        u = v[c].unique()
        n = len(u)
        isStr = isinstance(u[0],basestring)
        print('')
        print(Bold(c+': ')+str(n)+' unique values.')
        if n<=maxItems:
            if isStr:
                print(',  '.join(np.sort(u)))
            else:
                print(',  '.join(np.sort(u).astype('unicode')))
        else:
            if isStr:
                print(Bold('(sample) ')+',  '.join(np.sort(np.random.choice(u,size=maxItems,replace=False))))
            else:
                print(Bold('(sample) ')+',  '.join(np.sort(np.random.choice(u,size=maxItems,replace=False)).astype('unicode')))


def check_missing(v):
    """
    Takes a pandas dataframe and prints out the columns that have missing values.
    """
    colNames = v.columns.values
    print(Bold('Colunas com valores faltantes:'))
    Ntotal = len(v)
    Nmiss  = np.array([float(len(v.loc[v[c].isnull()])) for c in colNames])
    df = pd.DataFrame(np.transpose([colNames,[v[c].isnull().any() for c in colNames], Nmiss, np.round(Nmiss/Ntotal*100,2)]),
                     columns=['coluna','missing','N','%'])
    print(df.loc[df['missing']==True][['coluna','N','%']])


def freq(series, value):
    """
    Takes a pandas series and a value and returns the fraction of the series that presents a certain value.
    """
    Ntotal = len(series)
    Nsel   = float(len(series.loc[series==value]))
    return Nsel/Ntotal

if __name__ == '__main__':
    
    # This is executed you run via terminal

    print('I\'m in terminal! - example.py')