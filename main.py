from flask import Flask, render_template, request, redirect, url_for
from db import getProflist, cad_Prof, cad_Escola, getEscolalist, getTurmalist, cad_Turma, getSondagemlist, cad_Sondagem, getAlunolist, cad_Aluno, getAvaliacaolist, cad_Avaliacao
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField, SelectField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key'

class TurmaForm(FlaskForm):
    serie_turma = StringField('Serie da Turma', validators=[DataRequired()])
    ano_turma = StringField('Ano da Turma', validators=[DataRequired()])
    id_professor = IntegerField('Id do Professor')
    submit = SubmitField('Cadastrar')

class SondagemForm(FlaskForm):
    materia = SelectField('Matéria', choices=["Português","Matemática"],validators=[DataRequired()])
    campo_semantico = StringField('Campo Semantico', validators=[DataRequired()])
    valores_ditados = StringField('Valores Ditados')
    data_sondagem = StringField('Data' , validators=[DataRequired()])
    submit = SubmitField('Cadastrar')

class AlunoForm(FlaskForm):
    nome_aluno = StringField('Nome do Aluno',validators=[DataRequired()])
    nome_responsavel1 = StringField('Nome do Responsavel 1', validators=[DataRequired()])
    nome_responsavel2 = StringField('Nome do Responsavel 2')
    data_nascimento = StringField('Data de Nascimento' , validators=[DataRequired()])
    telefone_contato = StringField('Telefone de Contato' , validators=[DataRequired()])
    #id_turma = IntegerField('ID da Turma')
    #criando lista dinamica
    turma_list=getTurmalist()
    lista_serie = [int(x[0]) for x in turma_list]
    print(lista_serie)
    id_turma = SelectField('ID da Turma', choices=lista_serie, coerce=int)
    submit = SubmitField('Cadastrar')

class AvaliacaoForm(FlaskForm):
    data_avaliacao = StringField('Data da Avaliação',validators=[DataRequired()])
    hipotese_escrita = SelectField('Hipótese de Escrita', choices=['Nivel 1','Nivel 2','Nivel 3', 'Nivel 4', 'Nivel 5', 'PRÉ-SILÁBICO', 'SILÁBICO SEM VALOR SONORO', 'SILÁBICO COM VALOR SONORO', 'SILÁBICO ALFABÉTICO','ALFABÉTICO'], validators=[DataRequired()])
    id_aluno = StringField('ID do Aluno')
    id_sondagem = StringField('ID da Sondagem' , validators=[DataRequired()])
    submit = SubmitField('Cadastrar')

@app.route('/')
def index():
    return render_template('index.html')


# Cadastro do Professor
@app.route('/cadastro/')
def cadastro():
    prof_list=getProflist()
    return render_template('cadastro.html', prof_list=prof_list)

@app.route('/cad_professor', methods=['POST'])
def cad_professor():
    nome_prof = request.form['nome_prof']
    email_prof = request.form['email_prof']
    telefone = request.form['telefone']
    id_escola = request.form['id_escola']
    cad_Prof(nome_prof, email_prof, telefone, id_escola)
    return redirect(url_for('cadastro'))

@app.route('/cad_escola')
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
def turma():
    turma_list=getTurmalist()
    form = TurmaForm()
    if form.validate_on_submit():
        cad_Turma(form.serie_turma.data, form.ano_turma.data, form.id_professor.data) 
        return redirect(url_for('turma'))
    return render_template('cad_turma.html', turma_list=turma_list,form=form)

#Cadastro da Sondagem
@app.route('/cad_sondagem', methods=['GET','POST'])
def cad_sondagem():
    sondagem_list=getSondagemlist()
    form = SondagemForm()
    if form.validate_on_submit():
        cad_Sondagem(form.materia.data, form.campo_semantico.data, form.valores_ditados.data, form.data_sondagem.data) 
        return redirect(url_for('cad_sondagem'))
    return render_template('cad_sondagem.html', sondagem_list=sondagem_list, form=form)

#Cadastro de Aluno
@app.route('/cad_aluno', methods=['GET','POST'])
def cad_aluno():
    aluno_list=getAlunolist()
    form = AlunoForm()
    if form.validate_on_submit():
        cad_Aluno(form.nome_aluno.data, form.nome_responsavel1.data, form.nome_responsavel2.data, form.data_nascimento.data, form.telefone_contato.data, form.id_turma.data) 
        return redirect(url_for('cad_aluno'))
    return render_template('cad_aluno.html', aluno_list=aluno_list, form=form)

#Cadastro de Avaliação
@app.route('/cad_avaliacao', methods=['GET','POST'])
def cad_avaliacao():
    avaliacao_list=getAvaliacaolist()
    form = AvaliacaoForm()
    if form.validate_on_submit():
        cad_Avaliacao(form.data_avaliacao.data, form.hipotese_escrita.data, form.id_aluno.data, form.id_sondagem.data) 
        return redirect(url_for('cad_avaliacao'))
    return render_template('cad_avaliacao.html', avaliacao_list=avaliacao_list, form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5432)
