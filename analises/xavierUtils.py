import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as pl


### Auxiliary functions ###


def Bold(text):
    """
    Takes a string and returns it bold.
    """
    return '\033[1m'+text+'\033[0m'


def unique(series):
    """
    Takes a pandas series as input and print all unique values, separated by a blue bar.
    """
    u = series.unique()
    try:
        print Bold(str(len(u)))+': '+'\033[1;34m | \033[0m'.join(sorted(u.astype(str)))
    except:
        print Bold(str(len(u)))+': '+'\033[1;34m | \033[0m'.join(sorted(u))

def columns(df):
    """
    Print the number of columns and their names, separated by a blue bar.
    """
    unique(df.columns)
    
def mapUnique(df):
    """
    Takes a pandas dataframe and prints the unique values of all columns and their numbers.
    If the number of unique values is greater than maxItems, only print out a sample.  
    """
    for c in df.columns.values:
        maxItems = 20
        u = df[c].unique()
        n = len(u)
        isStr = isinstance(u[0],basestring)
        print ''
        print Bold(c+': ')+str(n)+' unique values.'
        if n<=maxItems:
            if isStr:
                print ',  '.join(np.sort(u))
            else:
                print ',  '.join(np.sort(u).astype('unicode'))
        else:
            if isStr:
                print Bold('(sample) ')+',  '.join(np.sort(np.random.choice(u,size=maxItems,replace=False)))
            else:
                print Bold('(sample) ')+',  '.join(np.sort(np.random.choice(u,size=maxItems,replace=False)).astype('unicode'))


def checkMissing(df):
    """
    Takes a pandas dataframe and prints out the columns that have missing values.
    """
    colNames = df.columns.values
    print Bold('Colunas com valores faltantes:')
    Ntotal = len(df)
    Nmiss  = np.array([float(len(df.loc[df[c].isnull()])) for c in colNames])
    df2    = pd.DataFrame(np.transpose([colNames,[df[c].isnull().any() for c in colNames], Nmiss, np.round(Nmiss/Ntotal*100,2)]),
                     columns=['coluna','missing','N','%'])
    print df2.loc[df2['missing']==True][['coluna','N','%']]


def freq(series, value):
    """
    Takes a pandas series and a value and returns the fraction of the series that presents a certain value.
    """
    Ntotal = len(series)
    Nsel   = float(len(series.loc[series==value]))
    return Nsel/Ntotal


### TEM BUG!! CORRIGIR! >> o split pode dar errado se o path tiver ../
def saveFigWdate(name):
    """
    Takes a string (a filename with extension) and save the current plot to it, 
    but adding the current date to the filename.
    """
    part = name.split('.')
    t = dt.datetime.now().strftime('%Y-%m-%d')
    filename = part[0]+'_'+t+'.'+part[1]
    pl.savefig(filename, bbox_inches='tight')


def cov2corr(cov):
    """
    Takes a covariance matrix and returns the correlation matrix.
    """
    assert(len(cov) == len(np.transpose(cov))), 'Cov. matrix must be a square matrix.'
    corr = [ [cov[i][j]/np.sqrt(cov[i][i]*cov[j][j]) for i in range(0,len(cov))] for j in range(0,len(cov))]
    return np.array(corr)


def one2oneQ(df, col1, col2):
    """
    Check if there is a one-to-one correspondence between two columns in a dataframe.
    """
    n2in1 = df.groupby(col1)[col2].nunique()
    n1in2 = df.groupby(col2)[col1].nunique()
    if len(n2in1)==np.sum(n2in1) and len(n1in2)==np.sum(n1in2):
        return True
    else:
        return False


def one2oneViolations(df, colIndex, colMultiples):
    """
    Returns the unique values in colMultiples for a fixed value in colIndex (only for when the number of unique values is >1).
    """
    return df.groupby(colIndex)[colMultiples].unique().loc[df.groupby(colIndex)[colMultiples].nunique()>1]
