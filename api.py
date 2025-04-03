from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS livros(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   titulo TEXT NOT NULL,
                   categoria TEXT NOT NULL,
                   autor TEXT NOT NULL,
                   imagem_url TEXT NOT NULL
                   )""")
        print("Banco de dados criado!!")


init_db()

@app.route('/')
def homepage():
    return '<h2>API para doação de livros<h2>'

@app.route("/doar", methods=['POST'])
def doar():

    dados = request.get_json()

    titulo = dados.get("titulo")
    categoria = dados.get("categoria")
    autor = dados.get("autor")
    imagem_url = dados.get("imagem_url")

    if not all ([titulo, categoria, autor, imagem_url]):

        return jsonify({'erro':'Todos os campos são obrigatórios'}), 400

    with sqlite3.connect ('database.db') as conn:
        conn.execute(f"""INSERT INTO livros(titulo,categoria,autor,imagem_url)VALUES(?,?,?,?)""", (titulo,categoria, autor, imagem_url))
        conn.commit()

        return jsonify({'mensagem':'Livros cadastrados com sucesso'}), 201
    
@app.route('/livros', methods=['GET'])

def listar_livros():
    with sqlite3.connect('database.bd') as conn:
        livros = conn.execute("SELECT * FROM livros").fetchall()

        livros_formatados = []
        
        for livros in livros:
            dicionario_livro={
                "id": livros[0],
                "titulo": livros[1],
                "categoria": livros[2],
                "autor": livros[3],
                "imagem_url": livros[4]
            }
            livros_formatados.append(dicionario_livro)

        return jsonify(livros_formatados)


if __name__ == "__main__":
    app.run(debug=True)