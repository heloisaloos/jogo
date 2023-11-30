from config import *

# Rota funcionando
@app.route("/salvar", methods=["post"])
def salvar():

    try:
        file = request.files["files"]
        caminho = os.path.join(pastaimagem, 'background.jpg')
        file.save(caminho)
        resposta = jsonify({"resultado":"ok", "detalhes": "Imagem salva"})

    except Exception as erro:
        resposta = jsonify({"resposta": "Erro! ", "detalhes": str(erro)})

    return resposta