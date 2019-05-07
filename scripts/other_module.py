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
    
    pl.figure(figsize=(10, 5))
    n_rows = 1
    n_cols = 2

    pl.subplot(n_rows, n_cols, 1)

    # Plot:    
    median = histogram(df, 'acoes', 'fd', 40, 100)
    pl.gca().tick_params(labelsize=14)

    # Labels
    pl.xlabel(f'# de {acao}', fontsize=14)
    pl.ylabel('# de deputados´', fontsize=14)

    # Coloca acredito:
    pl.axvline(median, linestyle='--', color='k')
    vertical_lines = [lines.Line2D([], [], color='k', linestyle='--', label='Mediana')]
    
    with suppress(Exception):
        pl.axvline(df.loc[(df['nome_parlamentar'] == 'TABATA AMARAL')]['acoes'].values[0], color='purple')
        vertical_lines.append(lines.Line2D([], [], color=colors.to_rgba('purple', alpha=None), linestyle='-',
                                           label='Tabata'))
    with suppress(Exception):
        pl.axvline(df.loc[(df['nome_parlamentar'] == 'FELIPE RIGONI')]['acoes'].values[0], color='green')
        vertical_lines.append(lines.Line2D([], [], color='green', linestyle='-', label='Felipe'))


    # Plota Legenda
    pl.legend(handles=vertical_lines, fontsize=14, loc='upper right')

    # Gráfico Acumulado #
    pl.subplot(n_rows, n_cols, 2)

    ## Plot
    data_cumsum = (df['acoes'].sort_values(ascending=False).cumsum()
                   .reset_index(drop=True).divide(sum(df['acoes']))
                   .multiply(100))
    pl.plot(data_cumsum.index, data_cumsum)
    pl.gca().tick_params(labelsize=14)
    pl.ylim([0, 100])

    ## Labels
    pl.xlabel('# de deputados', fontsize=14)
    pl.ylabel(f'% do total de {acao}', fontsize=14)

    pl.axhline(50, color='black', linestyle='--')
    vertical_lines = []
    
    with suppress(Exception):
        print('Posicao Tabata', (df.sort_values('acoes', ascending=False)
                .reset_index(drop=True).
                query("nome_parlamentar == 'TABATA AMARAL'").index.values[0]))
        pl.axvline((df.sort_values('acoes', ascending=False)
                .reset_index(drop=True)
                .query("nome_parlamentar == 'TABATA AMARAL'").index.values[0]),
               color='purple')
        vertical_lines.append(lines.Line2D([], [], color=colors.to_rgba('purple', alpha=None), linestyle='-', label='Tabata'))   
    
    with suppress(Exception):
        print('Posicao Rigoni', (df.sort_values('acoes', ascending=False)
                .reset_index(drop=True).
                query("nome_parlamentar == 'FELIPE RIGONI'").index.values[0]))
        pl.axvline((df.sort_values('acoes', ascending=False)
                .reset_index(drop=True).
                query("nome_parlamentar == 'FELIPE RIGONI'").index.values[0]),
               color='green')
        vertical_lines.append(lines.Line2D([], [], color='green', linestyle='-', label='Felipe'))

    ## Legenda
    pl.legend(handles=vertical_lines, fontsize=14, loc='lower right')
     
    ## Plot e Salva Figura e Arquivo
    pl.tight_layout()
    
    pl.savefig(OUTPUT_PATH / f'atividade/fig/plot_{acao}_deputados.png', bbox_inches='tight')
    df.sort_values(by='acoes').to_csv(OUTPUT_PATH / f'atividade/data/{acao}_deputados.csv')
    pl.show()
    
    
    

def plot_partido(df, acao, partido_bancada):
    
    pl.figure(figsize=(10, 10))
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
    pl.xlabel(f'# de {acao}', fontsize=14)
    
    pl.subplot(n_rows, n_cols, 2)
    
    df_partidos = df_partidos.merge(partido_bancada, left_index=True, right_on='sigla_partido') 
    df_partidos['percapita'] = df_partidos.apply(lambda x: x['acoes'] / x['numero_parlamentares'], 1)

    pl.barh(df_partidos['sigla_partido'], 
            df_partidos['percapita'])
    pl.xlabel(f'{acao} per capita', fontsize=14)
    pl.gca().tick_params(axis='x', labelsize=14)
    pl.gca().tick_params(axis='y', labelleft=False)

    
    pl.tight_layout()
        
    pl.savefig(OUTPUT_PATH / f'atividade/fig/plot_{acao}_partidos_percapita.png', bbox_inches='tight')
    df_partidos.to_csv(OUTPUT_PATH / f'atividade/data/{acao}_partidos.csv')
    pl.show()

    
    
def query_data(atividades, acao, tipo_atividade):

    queries = {}
    
    queries['tramitacao'] = """
    SELECT 
    legislatura , nome_parlamentar, sigla_partido, count(*) as acoes
    FROM `gabinete-compartilhado.analise_congresso_atividade.tramitacao_por_parlamentar_` 
    WHERE data_hora BETWEEN DATETIME('2019-02-01') AND DATETIME('2019-05-11')
    AND {}
    GROUP BY legislatura , nome_parlamentar, sigla_partido 
    """
    
    queries['autores'] = """
    SELECT 
    56 as legislatura, UPPER(nome_autor) as nome_parlamentar, sigla_partido_autor as sigla_partido, count(*) as acoes
    FROM `gabinete-compartilhado.congresso.camara_proposicoes_autores_` 
    WHERE sigla_tipo = '{}'
    AND data_apresentacao BETWEEN DATETIME('2019-02-01') AND DATETIME('2019-05-11')
    AND sigla_partido_autor != ''
    GROUP BY nome_autor, sigla_partido_autor
    """
    
    return query_gcp(queries[tipo_atividade].format(atividades[acao]))
    
def build_plots(atividades, 
                acao='relatorias',
                partido_bancada=None, 
                tipo_atividade='tramitacao'
               ):
    
    df = query_data(atividades, acao, tipo_atividade)
    
    print('-'*15)
    print(acao)
    print('-'*15)
    
    print('Deputados')
    plot_deputado(df, acao)
    print('-'*15)
    print('Partidos')
    plot_partido(df, acao, partido_bancada)