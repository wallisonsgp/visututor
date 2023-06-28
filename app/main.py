from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'files_upload'
app.secret_key = 'sua_chave_secreta'  # Defina sua própria chave secreta

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Dados de exemplo para autenticação
users = {'admin@asdf.com': {'password': 'admin123'}}


def obter_estrutura_pasta(caminho):
    estrutura_pasta = []
    for raiz, pastas, arquivos in os.walk(caminho):
        # # Adiciona as pastas ao resultado
        # for pasta in pastas:
        #     estrutura_pasta.append(os.path.join(raiz, pasta))
        # Adiciona os arquivos ao resultado
        for arquivo in arquivos:
            estrutura_pasta.append(os.path.join(raiz, arquivo))
    return estrutura_pasta

# Classe de exemplo para representar um usuário
class User(UserMixin):
    def __init__(self, username):
        self.username = username
        self.password = users[username]['password']

    def get_id(self):
        return self.username


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/')
@login_required
def index():
    return render_template('dashboard.html')

@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        print(username)
        print(password)
        if username in users and password == users[username]['password']:
            user = User(username)
            login_user(user)
            return redirect(url_for('chat'))
        else:
            flash('Usuário ou senha inválidos', 'error')
    return render_template('login.html')

@app.route('/api/chat', methods=['POST'])
@login_required
def process_message():
    message = request.form.get('message')

    # Verificar se a mensagem é um arquivo de áudio
    if 'audio' in request.files:
        audio_file = request.files['audio']
        # Aqui você pode fazer o processamento necessário com o arquivo de áudio
        # por exemplo, salvá-lo em disco ou processá-lo com alguma biblioteca de processamento de áudio
        
        # Retornar uma resposta com a mensagem indicando que o áudio foi recebido
        response = "Áudio recebido com sucesso!"
    else:
        # Processar a mensagem de texto normalmente
        # Aqui você pode implementar a lógica de processamento da mensagem de texto
        # e obter a resposta adequada do chatbot
        # Por exemplo, usando um modelo de linguagem ou chamando uma API de chatbot
        
        # Retornar uma resposta padrão para a mensagem de texto
        response = "Mensagem de texto recebida"

    return jsonify({'response': response})

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/files')
@login_required
def files():
    
    return render_template('files.html')


@app.route('/upload')
@login_required
def upload():
    estrutura_pasta = obter_estrutura_pasta(app.config['UPLOAD_FOLDER'])
    return render_template('upload.html', estrutura_pasta=estrutura_pasta)

import os

@app.route('/excluirarquivo', methods=['POST'])
@login_required
def excluir_arquivo():
    nome_arquivo = request.form['nome_arquivo']
    nome_arquivo = '/Users/guimaraes/Workspace/private-projects/visututor/app/'+nome_arquivo
    caminho_arquivo = os.path.join('caminho', nome_arquivo)  # Substitua 'caminho' pelo caminho real da pasta onde os arquivos estão salvos
    
    if os.path.exists(caminho_arquivo):
        os.remove(caminho_arquivo)
        return 'Arquivo excluído com sucesso!'
    else:
        return 'Arquivo não encontrado.'


@app.route('/uploadprocessing', methods=['POST'])
@login_required
def uploadprocessing():
    estrutura_pasta = obter_estrutura_pasta(app.config['UPLOAD_FOLDER'])
    if 'fileInput' in request.files:
        file = request.files['fileInput']
        categoria = request.form['categoriaInput']

        # Verificar se o diretório da categoria já existe, caso contrário, criar
        diretorio_categoria = os.path.join(app.config['UPLOAD_FOLDER'], categoria)
        if not os.path.exists(diretorio_categoria):
            os.makedirs(diretorio_categoria)

        # Salvar o arquivo no diretório da categoria
        arquivo_path = os.path.join(diretorio_categoria, file.filename)
        file.save(arquivo_path)
        estrutura_pasta = obter_estrutura_pasta(app.config['UPLOAD_FOLDER'])
        return render_template('upload.html', message='Arquivo enviado com sucesso!', estrutura_pasta=estrutura_pasta)
    else:
        return render_template('upload.html', message='Nenhum arquivo selecionado.', estrutura_pasta=estrutura_pasta)



    
@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot-password.html')

if __name__ == '__main__':
    app.run(debug=True)