import sqlite3
from flask import Flask, request, render_template, send_file, redirect, url_for

# Configurações iniciais do Flask
app = Flask(__name__)

# Conectar ao banco de dados SQLite e verificar a existência da coluna 'status'
conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''PRAGMA table_info(nomes)''')
columns = [column[1] for column in c.fetchall()]
if 'status' not in columns:
    c.execute('ALTER TABLE nomes ADD COLUMN status TEXT DEFAULT "ativo"')
    conn.commit()
conn.close()



# Rota para a página inicial com o formulário
@app.route('/')
def index():
    return render_template('index.html')

# Rota para lidar com o envio do formulário
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        try:
            # Conectar ao banco de dados SQLite
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            # Executar a consulta SQL para inserir o nome na tabela
            c.execute('INSERT INTO nomes (nome, status) VALUES (?, "ativo")', (name,))
            # Commit e fechar a conexão com o banco de dados
            conn.commit()
            conn.close()
            return 'Nome inserido com sucesso no banco de dados!'
        except Exception as e:
            return f"Erro ao inserir no banco de dados: {str(e)}"


# Rota para gerar o código QR para um nome específico
@app.route('/qrcode/<nome>')
def generate_qrcode(nome):
    try:
        # Conectar ao banco de dados SQLite
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        
        # Verificar se o nome está marcado como "inativo" no banco de dados
        c.execute('SELECT status FROM nomes WHERE nome = ? AND status = "inativo"', (nome,))
        status = c.fetchone()
        
        if status:
            # Se o status for "inativo", redirecionar para a página informando que o código QR já foi usado
            return redirect(url_for('codigo_usado'))
        else:
            # Se o status não for "inativo", atualizar o status do registro para 'inativo'
            c.execute('UPDATE nomes SET status = "inativo" WHERE nome = ?', (nome,))
            # Commit e fechar a conexão com o banco de dados
            conn.commit()
            conn.close()
            
            # Redirecionar para a página de redirecionamento
            return redirect(url_for('pagina_redirecionada'))
    except Exception as e:
        return f"Erro ao gerar o código QR: {str(e)}"

# Rota para a página de redirecionamento
@app.route('/pagina_redirecionada')
def pagina_redirecionada():
    return render_template('pagina_redirecionada.html')

# Rota para a página informando que o código QR já foi usado
@app.route('/codigo_usado')
def codigo_usado():
    return render_template('codigo_usado.html')

# Executar o aplicativo Flask
if __name__ == '__main__':
    app.run(debug=True)
