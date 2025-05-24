from flask import Flask, render_template, request, redirect, url_for, flash, session
from db import *
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField, SelectField, HiddenField
from wtforms.validators import DataRequired
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import psycopg2
from psycopg2.extras import RealDictCursor
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key'

class TurmaForm(FlaskForm):
    id_turma = HiddenField()
    serie_turma = StringField('Serie da Turma', validators=[DataRequired()])
    ano_turma = StringField('Ano da Turma', validators=[DataRequired()])
    id_professor = SelectField('Nome do Professor', choices=[], coerce=int)
    submit = SubmitField('Cadastrar')
    submit_alt = SubmitField('Gravar Alterações')

class SondagemForm(FlaskForm):
    id_sondagem = HiddenField()
    materia = SelectField('Matéria', choices=["Português","Matemática"],validators=[DataRequired()])
    campo_semantico = StringField('Campo Semantico', validators=[DataRequired()])
    valores_ditados = StringField('Valores Ditados')
    data_sondagem = StringField('Data' , validators=[DataRequired()])
    submit = SubmitField('Cadastrar')
    submit_alt = SubmitField('Gravar Alterações')

class AlunoForm(FlaskForm):
    id_aluno = HiddenField()
    nome_aluno = StringField('Nome do Aluno',validators=[DataRequired()])
    nome_responsavel1 = StringField('Nome do Responsavel 1', validators=[DataRequired()])
    nome_responsavel2 = StringField('Nome do Responsavel 2')
    data_nascimento = StringField('Data de Nascimento' , validators=[DataRequired()])
    telefone_contato = StringField('Telefone de Contato' , validators=[DataRequired()])
    id_turma = SelectField('Selecione o ID da Turma', choices=[], coerce=int)
    submit = SubmitField('Cadastrar')
    submit_alt = SubmitField('Gravar Alterações')

class AvaliacaoForm(FlaskForm):
    id_avaliacao = HiddenField()
    data_avaliacao = StringField('Data da Avaliação',validators=[DataRequired()])
    hipotese_escrita = SelectField('Hipótese de Escrita', choices=['Nivel 1','Nivel 2','Nivel 3', 'Nivel 4', 'Nivel 5', 'PRÉ-SILÁBICO', 'SILÁBICO SEM VALOR SONORO', 'SILÁBICO COM VALOR SONORO', 'SILÁBICO ALFABÉTICO','ALFABÉTICO'], validators=[DataRequired()])
    id_aluno = SelectField('Selecione o Aluno', choices=[], coerce=int)
    id_sondagem = SelectField('Escolha uma Sondagem' , choices=[], coerce=int)
    submit = SubmitField('Cadastrar')
    submit_alt = SubmitField('Gravar Alterações')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/relatorios')
@login_required
def relatorios():
    return render_template('relatorios.html')

# Cadastro do Professor
@app.route('/cadastro/')
@login_required
def cadastro():
    prof_list=getProflist()
    escola_list=getEscolalist()    
    return render_template('cadastro.html', prof_list=prof_list, escola_list=escola_list)

@app.route('/cad_professor', methods=['POST'])
def cad_professor():
    nome_prof = request.form['nome_prof']
    email_prof = request.form['email_prof']
    telefone = request.form['telefone']
    id_escola = request.form.get('id_escola')
    cad_Prof(nome_prof, email_prof, telefone, id_escola)
    return redirect(url_for('cadastro'))

@app.route('/cad_escola')
@login_required
def escola():
    escola_list=getEscolalist()
    return render_template('cad_escola.html',escola_list=escola_list)

# Cadastro da Escola
@app.route('/cad_escola', methods=['POST'])
def cad_escola():
    nome_escola = request.form['nome_escola']
    endereco = request.form['endereco']
    cidade = request.form['cidade']
    estado = request.form['estado']
    cad_Escola(nome_escola, endereco, cidade, estado)   
    return redirect(url_for('cad_escola'))

# Cadastro da Turma
@app.route('/cad_turma', methods=['GET','POST'])
@login_required
def turma():
    turma_list=getTurmalist()
    form = TurmaForm()
    #alteracao para incluir lista dinaminca de professores
    prof_list=getProflist()
    form.id_professor.choices =[(prof[0], prof[1]) for prof in prof_list]
    
    if form.validate_on_submit():
        cad_Turma(form.serie_turma.data, form.ano_turma.data, form.id_professor.data) 
        return redirect(url_for('turma'))
    return render_template('cad_turma.html', turma_list=turma_list,form=form)

#Cadastro da Sondagem
@app.route('/cad_sondagem', methods=['GET','POST'])
@login_required
def cad_sondagem():
    sondagem_list=getSondagemlist()
    form = SondagemForm()
    if form.validate_on_submit():
        cad_Sondagem(form.materia.data, form.campo_semantico.data, form.valores_ditados.data, form.data_sondagem.data) 
        return redirect(url_for('cad_sondagem'))
    return render_template('cad_sondagem.html', sondagem_list=sondagem_list, form=form)

#Cadastro de Aluno
@app.route('/cad_aluno', methods=['GET','POST'])
@login_required
def cad_aluno():
    aluno_list=getAlunolist()
    form = AlunoForm()
    #alteracao para incluir lista dinamica das turmas pelo nome
    turma_list=getTurmalist()
    form.id_turma.choices = [(turma[0], turma[1]) for turma in turma_list]
    
    if form.validate_on_submit():
        cad_Aluno(form.nome_aluno.data, form.nome_responsavel1.data, form.nome_responsavel2.data, form.data_nascimento.data, form.telefone_contato.data, form.id_turma.data) 
        return redirect(url_for('cad_aluno'))
    return render_template('cad_aluno.html', aluno_list=aluno_list, form=form)

#Cadastro de Avaliação
@app.route('/cad_avaliacao', methods=['GET','POST'])
@login_required
def cad_avaliacao():
    avaliacao_list=getAvaliacaolist()
    form = AvaliacaoForm()
    #alteracao para incluir lista dinamica do nome do Aluno e Sondagem
    aluno_list=getAlunolist()
    sondagem_list=getSondagemlist()
    form.id_aluno.choices = [(aluno[0], aluno[1]) for aluno in aluno_list]
    form.id_sondagem.choices =[(sondagem[0], sondagem[1]+' / '+sondagem[2]+' / '+sondagem[3]+' / '+sondagem[4]) for sondagem in sondagem_list]

    if form.validate_on_submit():
        cad_Avaliacao(form.data_avaliacao.data, form.hipotese_escrita.data, form.id_aluno.data, form.id_sondagem.data) 
        return redirect(url_for('cad_avaliacao'))
    return render_template('cad_avaliacao.html', avaliacao_list=avaliacao_list, form=form)

#Alterando dados de cadastro da escola
@app.route('/update_escola', methods=['POST','GET'])
def update_escola():
    if request.method == 'POST' :
        id_escola = request.form['id_escola']
        nome_escola = request.form['nome_escola']
        endereco = request.form['endereco']
        cidade = request.form['cidade']
        estado = request.form['estado']
        alt_Escola(id_escola, nome_escola, endereco, cidade, estado)   
        return redirect(url_for('cad_escola'))

#rota para deletar registros da tabela escola
@app.route('/del_escola/<string:id_escola>', methods=['GET'])
def delete_escola(id_escola):  
        del_Escola(id_escola)
        return redirect(url_for('cad_escola'))


#Alterando dados de cadastro do Professor
@app.route('/update_prof', methods=['POST','GET'])
def update_prof():  
    if request.method == 'POST' :
        id_professor = request.form['id_professor']
        nome_prof = request.form['nome_prof']
        email_prof = request.form['email_prof']
        telefone = request.form['telefone']
        id_escola = request.form.get('id_escola')
        #print(id_professor, nome_prof, email_prof, telefone, id_escola)
        alt_Prof(id_professor, nome_prof, email_prof, telefone, id_escola)   
        return redirect(url_for('cadastro'))

#rota para deletar registros da tabela professor
@app.route('/del_prof/<string:id_professor>', methods=['GET'])
def delete_prof(id_professor):  
        del_Prof(id_professor)
        return redirect(url_for('cadastro'))


# Alterando dados de cadastro da Turma
@app.route('/alt_turma', methods=['GET','POST'])
def alt_turma():
    turma_list=getTurmalist()
    form = TurmaForm()
    #alteracao para incluir lista dinaminca de professores
    prof_list=getProflist()
    form.id_professor.choices =[(prof[0], prof[1]) for prof in prof_list]

    if form.validate_on_submit():
        alt_Turma(form.id_turma.data, form.serie_turma.data, form.ano_turma.data, form.id_professor.data) 
        return redirect(url_for('turma'))
    return render_template('cad_turma.html', turma_list=turma_list,form=form)

#rota para deletar registros da tabela turma
@app.route('/del_turma/<string:id_turma>', methods=['GET'])
def del_turma(id_turma):  
        del_Turma(id_turma)
        return redirect(url_for('turma'))


## Alterando dados de cadastro de Alunos
@app.route('/alt_aluno', methods=['GET','POST'])
def alt_aluno():
    aluno_list=getAlunolist()
    form = AlunoForm()
    #alteracao para incluir lista dinamica das turmas pelo nome
    turma_list=getTurmalist()
    form.id_turma.choices = [(turma[0], turma[1]) for turma in turma_list]

    if form.validate_on_submit():
        alt_Aluno(form.id_aluno.data, form.nome_aluno.data, form.nome_responsavel1.data, form.nome_responsavel2.data, form.data_nascimento.data, form.telefone_contato.data, form.id_turma.data) 
        return redirect(url_for('cad_aluno'))
    return render_template('cad_aluno.html', aluno_list=aluno_list, form=form)

#rota para deletar registros da tabela aluno
@app.route('/del_aluno/<string:id_aluno>', methods=['GET'])
def del_aluno(id_aluno):  
        del_Aluno(id_aluno)
        return redirect(url_for('cad_aluno'))

# Alterando dados de cadastro da Sondagem
@app.route('/alt_sondagem', methods=['GET','POST'])
def alt_sondagem():
    sondagem_list=getSondagemlist()
    form = SondagemForm()
    if form.validate_on_submit():
        alt_Sondagem(form.id_sondagem.data, form.materia.data, form.campo_semantico.data, form.valores_ditados.data, form.data_sondagem.data) 
        return redirect(url_for('cad_sondagem'))
    return render_template('cad_sondagem.html', sondagem_list=sondagem_list, form=form)

#rota para deletar registros da tabela Sondagem
@app.route('/del_sondagem/<string:id_sondagem>', methods=['GET'])
def del_sondagem(id_sondagem):  
        del_Sondagem(id_sondagem)
        return redirect(url_for('cad_sondagem'))

# Alterando dados de cadastro da Avaliacao
@app.route('/alt_avaliacao', methods=['GET','POST'])
def alt_avaliacao():
    avaliacao_list=getAvaliacaolist()
    form = AvaliacaoForm()
    #alteracao para incluir lista dinamica do nome do Aluno e Sondagem
    aluno_list=getAlunolist()
    sondagem_list=getSondagemlist()
    #form.id_aluno.choices = [(aluno[0], aluno[1]) for aluno in aluno_list]
    #form.id_sondagem.choices =[(sondagem[0], sondagem[1]+' / '+sondagem[2]+' / '+sondagem[3]+' / '+sondagem[4]) for sondagem in sondagem_list]

    
    if form.validate_on_submit():
        alt_Avaliacao(form.id_avaliacao.data, form.data_avaliacao.data, form.hipotese_escrita.data, form.id_aluno.data, form.id_sondagem.data) 
        return redirect(url_for('cad_avaliacao'))
    return render_template('cad_avaliacao.html', avaliacao_list=avaliacao_list, form=form)

#rota para deletar registros da tabela Avaliacao
@app.route('/del_avaliacao/<string:id_avaliacao>', methods=['GET'])
def del_avaliacao(id_avaliacao):  
        del_Avaliacao(id_avaliacao)
        return redirect(url_for('cad_avaliacao'))












# Funcionalidade de Login

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'info'

# limpar mensagens flash
def clear_flash_messages():
    """Limpa todas as mensagens flash existentes"""
    session.pop('_flashes', None)

def flash_message(message, category='info'):
    """Adiciona uma mensagem flash após limpar as anteriores"""
    clear_flash_messages()
    flash(message, category)


class Usuario(UserMixin):
    def __init__(self, id_user, email):
        self.id = id_user
        self.email = email

    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(id_user):
    """Carrega o usuário pelo ID"""
    

    try:
        conn = psycopg2.connect(os.environ['DATABASE_URL'])
        cur = conn.cursor()
        #cursor = conn.cursor(cursor_factory=RealDictCursor)
        query = "SELECT id_user, senha FROM login WHERE id_user = %s"
        cur.execute(query, (id_user,))
        user_data = cur.fetchone()
        
        if user_data:
            #print('userdata:',user_data)
            return Usuario(user_data[0], user_data[1])
        return None

    except psycopg2.Error as e:
        print(f"Erro ao carregar usuário: {e}")
        return None

    finally:
        cur.close()
        conn.close()




# rota para tela de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = (request.form['senha'])
        #print('email , senha formulatio:', email,senha)
        
        #user = User.query.filter_by(email=email).first()
        conn = psycopg2.connect(os.environ['DATABASE_URL'])
        cur = conn.cursor()
        #cursor = conn.cursor(cursor_factory=RealDictCursor)
        query = "SELECT id_user, senha FROM login WHERE email = %s"
        cur.execute(query, (email,))
        user_data = cur.fetchone()
        #print('user data:', user_data)

        if not user_data:
            flash_message('Email ou senha incorretos.', 'info')
            return render_template('login.html')
            
        if not email or not senha:
            flash_message('Email e senha são obrigatórios.', 'info')
            return render_template('login.html')

        if user_data[1] == senha:
            user = Usuario(user_data[0], email)
            #if current_user.is_authenticated: 
                #print('esta autenticado')
            login_user(user)
            
            next_page = request.args.get('next')
            flash_message(f'Login realizado com sucesso! Bem-vindo, {user.email}', 'success')
            return redirect(next_page) if next_page else redirect(url_for('sobre'))
            

        else:
            flash_message('Email ou senha incorretos.', 'info')
            return render_template('login.html')

    return render_template('login.html')


# Rota Logout
@app.route('/logout')
@login_required
def logout():
    """Logout do usuário"""
    logout_user()
    #flash_message('Você foi desconectado com sucesso.', 'info')
    session.pop('_flashes', None)
    return redirect(url_for('index'))







if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5432)
