from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Defina sua própria chave secreta

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Dados de exemplo para autenticação
users = {'admin@asdf.com': {'password': 'admin123'}}


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
            return redirect(url_for('index'))
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
    return render_template('upload.html')


@app.route('/uploadprocessing', methods=['POST'])
@login_required
def uploadprocessing():
    if 'fileInput' in request.files:
        file = request.files['fileInput']
        # Aqui você pode processar o arquivo, salvar em um local, etc.
        # Exemplo de salvamento do arquivo no diretório atual:
        file.save('files_upload/'+file.filename)
        return render_template('upload.html', message='Arquivo enviado com sucesso!')
    else:
        return render_template('upload.html', message='Nenhum arquivo selecionado.')

    
@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot-password.html')

if __name__ == '__main__':
    app.run(debug=True)