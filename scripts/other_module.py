#!/usr/bin/python3
# code made by [You](https://github.com/@you), YYYY.

# Import config
import os
import sys
sys.path.insert(0, '../')
from config import RAW_PATH, TREAT_PATH, OUTPUT_PATH
from utils import *

import matplotlib.pyplot as pl
import matplotlib.colors as colors 
# Para legenda com linhas:
from matplotlib import lines
# Para legenda com barras:
from matplotlib.patches import Patch

from contextlib import suppress

import pandas as pd
import numpy as np

def histogram(df, column, bins, x_lim, y_lim):
    data = df[column].values
    pl.hist(data,bins=bins)
    # pl.ylim([0, y_lim])
    # pl.xlim([0, x_lim])
    return np.median(data)

def plot_deputado(df, acao):
    
    pl.figure(figsize=(15, 5))
    n_rows = 1
    n_cols = 2

    pl.subplot(n_rows, n_cols, 1)

    # Plot:    
    median = histogram(df, 'acoes', 'fd', 40, 100)
    pl.axvline(median, linestyle='--', color='k')

    # Labels
    pl.xlabel(f'# de {acao}')
    pl.ylabel('# de deputados´')

    # Coloca acredito:
    with suppress(Exception):
        pl.axvline(df.loc[(df['nome_parlamentar'] == 'TABATA AMARAL')]['acoes'].values[0], color='purple')
    with suppress(Exception):
        pl.axvline(df.loc[(df['nome_parlamentar'] == 'FELIPE RIGONI')]['acoes'].values[0], color='green')



    # Legenda
    import matplotlib.colors as colors 
    vertical_lines = [lines.Line2D([], [], color='k', linestyle='--', label='Mediana'),
    lines.Line2D([], [], color=colors.to_rgba('purple', alpha=None), linestyle='-', label='Tabata'),
    lines.Line2D([], [], color='green', linestyle='-', label='Felipe')]
    pl.legend(handles=vertical_lines, fontsize=14, loc='upper right')

    # Acumulado
    pl.subplot(n_rows, n_cols, 2)

    # Plot
    data_cumsum = (df['acoes'].sort_values(ascending=False).cumsum()
                   .reset_index(drop=True).divide(sum(df['acoes']))
                   .multiply(100))
    pl.plot(data_cumsum.index, data_cumsum)

    # Labels
    pl.xlabel('# de deputados')
    pl.ylabel(f'% do total de {acao}')

    pl.axvline(50, color='black', linestyle='--')
    with suppress(Exception):
        print('Posicao Tabata', (df.sort_values('acoes', ascending=False)
                .reset_index(drop=True).
                query("nome_parlamentar == 'TABATA AMARAL'").index.values[0]))
        pl.axvline((df.sort_values('acoes', ascending=False)
                .reset_index(drop=True)
                .query("nome_parlamentar == 'TABATA AMARAL'").index.values[0]),
               color='purple')
    with suppress(Exception):
        print('Posicao Rigoni', (df.sort_values('acoes', ascending=False)
                .reset_index(drop=True).
                query("nome_parlamentar == 'FELIPE RIGONI'").index.values[0]))
        pl.axvline((df.sort_values('acoes', ascending=False)
                .reset_index(drop=True).
                query("nome_parlamentar == 'FELIPE RIGONI'").index.values[0]),
               color='green')

    # # Legenda
    vertical_lines = [lines.Line2D([], [], color='k', linestyle='--', label=f'50 parlamentares'),
    lines.Line2D([], [], color=colors.to_rgba('purple', alpha=None), linestyle='-', label='Tabata'),
    lines.Line2D([], [], color='green', linestyle='-', label='Felipe')]
    pl.legend(handles=vertical_lines, fontsize=14, loc='lower right')

    pl.savefig(OUTPUT_PATH / f'plot_{acao}_deputados.png', bbox_inches='tight')
    
    pl.show()
    
    df.sort_values(by='acoes').to_csv(OUTPUT_PATH / f'{acao}_deputados.csv')
    

def plot_partido(df, acao, partido_bancada):
    
    pl.figure(figsize=(15, 10))
    n_rows = 1
    n_cols = 2

    pl.subplot(n_rows, n_cols, 1)

    df_partidos = df.groupby('sigla_partido').sum()[['acoes']]
    df_partidos = pd.concat([df_partidos, 
           pd.Series(index= ['Acredito'],
          data = [df.query("nome_parlamentar in ('TABATA AMARAL', 'FELIPE RIGONI')",)['acoes'].sum()], 
          name='acoes').to_frame()])
    df_partidos = df_partidos.sort_values(by='acoes')
    pl.barh(df_partidos.index, df_partidos['acoes'])
    pl.xlabel(f'# de {acao}')
    
    pl.subplot(n_rows, n_cols, 2)
    
    df_partidos = df_partidos.merge(partido_bancada, left_index=True, right_on='sigla_partido') 
    df_partidos['percapita'] = df_partidos.apply(lambda x: x['acoes'] / x['numero_parlamentares'], 1)

    pl.barh(df_partidos['sigla_partido'], 
            df_partidos['percapita'])
    pl.xlabel(f'# de {acao}')
    pl.gca().tick_params(axis='x', labelsize=14)
    
    pl.savefig(OUTPUT_PATH / f'plot_{acao}_partidos_percapita.png', bbox_inches='tight')
    
    pl.show()

    df_partidos.to_csv(OUTPUT_PATH / f'{acao}_partidos.csv')
    
def query_data(atividades, acao):

    query = """
    SELECT 
    legislatura , nome_parlamentar, sigla_partido, count(*) as acoes
    FROM `gabinete-compartilhado.analise_congresso_atividade.tramitacao_por_parlamentar_` 
    WHERE data_hora BETWEEN DATETIME('2019-02-01') AND DATETIME('2019-05-11')
    AND {}
    GROUP BY legislatura , nome_parlamentar, sigla_partido 
    """
    
    return query_gcp(query.format(atividades[acao]))
    
def build_plots(atividades, acao='relatorias', partido_bancada=None):
    
    df = query_data(atividades, acao)
    
    print('-'*15)
    print(acao)
    print('-'*15)
    
    print('Deputados')
    plot_deputado(df, acao)
    print('-'*15)
    print('Partidos')
    plot_partido(df, acao, partido_bancada)