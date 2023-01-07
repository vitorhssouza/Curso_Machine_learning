# Contruindo a api --> Flask
from flask import Flask, request
import joblib


# Instanciando o aplicativo
Aplicativo = Flask(__name__)

# Carregando nosso modelo 
modelo = joblib.load('Modelo_Floresta_Aleatorio_v100.pkl')

# Função para recerber nossa api
@Aplicativo.route('/api_preditivo/<area>;<rooms>;<bathroom>;<parking_spaces>;<floor>;<animal>;<furniture>;<hoa>;<property_tax>', methods=['GET'])
def funcao_01(area, rooms, bathroom, parking_spaces, floor, animal, furniture, hoa, property_tax):

    # Recebendo os parametro para analise da previsão 
    lista = [
        float(area), float(rooms), float(bathroom), float(parking_spaces),
        float(floor), float(animal), float(furniture), float(hoa), float(property_tax)
    ]

    try:
        previsao = modelo.predict(lista)

        return {'Valor_aluguel': 'previsao'}

    except:
        return {'Aviso': 'Deu algum error!'}

    


if __name__ == '__main__':
    Aplicativo.run(debug=True)

