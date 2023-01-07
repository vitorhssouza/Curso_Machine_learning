# Contruindo a api --> Flask
from flask import Flask, request

# Biblioteca para carregar meu modelo
import joblib

# Importando biblioteca para criar conexao com banco de dados
import sqlite3

# Lib para datas
from datetime import datetime

# Instanciando o aplicativo
Aplicativo = Flask(__name__)

# Carregando nosso modelo 
modelo = joblib.load('Modelo_Floresta_Aleatorio_v100.pkl')


# Função para recerber nossa api
@Aplicativo.route('/api_preditivo/<area>;<rooms>;<bathroom>;<parking_spaces>;<floor>;<animal>;<furniture>;<hoa>;<property_tax>', methods=['GET'])
def funcao_01(area, rooms, bathroom, parking_spaces, floor, animal, furniture, hoa, property_tax):

    # Data inicio
    data_inicio = datetime.now()

    # Recebendo os parametro para analise da previsão 
    lista = [
        float(area), float(rooms), float(bathroom), float(parking_spaces),
        float(floor), float(animal), float(furniture), float(hoa), float(property_tax)
    ]

    try:
        previsao = modelo.predict([lista])

        # Inserir o valor da previsão na lista
        lista.append(str(previsao))

        # Concatenando a lista
        inputs = ''
        for valor in lista:
            inputs = inputs + ';' + str(valor)

        # termino do processo 
        data_fim = datetime.now()
        processamento = data_fim - data_inicio

        # Criando conexão com banco de dados
        db = sqlite3.connect('Banco_dados_API.db')
        cursor = db.cursor()


        # query de inserção no db
        query_inserindo_dados = f'''
            INSERT INTO Log_API(inputs, inicio, fim, processamento)
            VALUES("{inputs}", "{data_inicio}", "{data_fim}", "{processamento}")
        '''

        # Executando a query
        cursor.execute(query_inserindo_dados)

        # Salvando os insert no banco
        db.commit()

        # Fechando conexão com banco de dados
        cursor.close()

        return {'Valor_aluguel': str(previsao)}

    except:
        return {'Atenção': 'Deu algum error'}


    


if __name__ == '__main__':
    Aplicativo.run(debug=True)

