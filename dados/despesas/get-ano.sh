# Baixa dados de uso de cotas parlamentares de um ano específico e unzipa:

# Parâmetros:
ano=$1

# Baixa:
wget http://www.camara.leg.br/cotas/Ano-$ano.csv.zip
# Descomprime:
unzip Ano-$ano.csv.zip
rm -f Ano-$ano.csv.zip
