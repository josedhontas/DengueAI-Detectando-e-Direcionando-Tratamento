from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from opencage.geocoder import OpenCageGeocode
from Algoritmos.predicaoSintomas import dataAcess

app = Flask(__name__)
CORS(app)

key = 'c098a7b3be6c4b4f9f14160c422559d5'
geocoder = OpenCageGeocode(key)

@app.route('/receber_data', methods=['POST'])
def receber_dados():
    try:
        dados_recebidos = request.json
        print(dados_recebidos)  # Imprimir os dados recebidos
        # Verificar se todos os campos necessários estão presentes nos dados recebidos
        campos_obrigatorios = ['nome', 'sobrenome', 'idade', 'endereco', 'numero', 'bairro', 'cidade', 'estado']
        for campo in campos_obrigatorios:
            if campo not in dados_recebidos:
                print(f'O campo obrigatório {campo} está ausente')
                return jsonify({'error': f'O campo obrigatório {campo} está ausente'}), 400

        dados_transformados = {
            "nome": f"{dados_recebidos.get('nome', '')} {dados_recebidos.get('sobrenome', '')}",
            "febre": int(dados_recebidos.get('febre', 0)),
            "dor_cabeca": int(dados_recebidos.get('dor_de_cabeca', 0)),
            "dor_articulacoes": int(dados_recebidos.get('dor_nas_articulacoes', 0)),
            "sangramento": int(dados_recebidos.get('sangramento', 0)),
            "idade": int(dados_recebidos.get('idade', 0))
        }
        print (dados_transformados)
        endereco_completo = f"{dados_recebidos.get('endereco', '')}, {dados_recebidos.get('numero', '')}, {dados_recebidos.get('bairro', '')}, {dados_recebidos.get('cidade', '')}, {dados_recebidos.get('estado', '')}, Brasil"
    
        resultados = geocoder.geocode(endereco_completo)

        if resultados:
            latitude = resultados[0]['geometry']['lat']
            longitude = resultados[0]['geometry']['lng']

            # Adicionar latitude, longitude e idade aos dados transformados
            dados_transformados["latitude"] = latitude
            dados_transformados["longitude"] = longitude

            print(dados_transformados)  # Imprimir os dados transformados
            resultado_previsao = dataAcess(dados_transformados)

            return jsonify({'resultado_previsao': resultado_previsao})
        else:
            print("Endereço não encontrado.")
            return jsonify({"error": "Endereço não encontrado"}), 404

    except Exception as e:
        print(f"Erro ao processar solicitação: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500
    
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index_consulta')
def index_consulta():
    return render_template('pages/index_consulta.html')

@app.route('/index_painel')
def index_painel():
    return render_template('pages/index_painel.html')

@app.route('/index_hospitais')
def index_hospitais():
    return render_template('pages/index_hospitais.html')


@app.route('/index_contaminacao')
def index_contaminacao():
    return render_template('pages/index_contaminacao.html')


@app.route('/index_unidades')
def index_unidades():
    return render_template('pages/index_unidades.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)



