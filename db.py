import psycopg2, os

def getProflist():
  conn = psycopg2.connect(os.environ['DATABASE_URL'])
  cur = conn.cursor()
  cur.execute("SELECT * FROM professor")
  prof_list = cur.fetchall()
  cur.close
  conn.close
  return prof_list

def cad_Prof(nome_prof, email_prof, telefone, id_escola):
  conn = psycopg2.connect(os.environ['DATABASE_URL'])
  cur = conn.cursor()
  cur.execute("INSERT INTO professor (nome_prof, email_prof, telefone, id_escola) VALUES( %s, %s , %s, %s);" ,(nome_prof, email_prof, telefone, id_escola))
  conn.commit()
  cur.close
  conn.close
  
def getEscolalist():
  conn = psycopg2.connect(os.environ['DATABASE_URL'])
  cur = conn.cursor()
  cur.execute("SELECT * FROM escola")
  prof_list = cur.fetchall()
  cur.close
  conn.close
  return prof_list

def cad_Escola(nome_escola, endereco, cidade, estado):
  conn = psycopg2.connect(os.environ['DATABASE_URL'])
  cur = conn.cursor()
  cur.execute("INSERT INTO escola (nome_escola, endereco, cidade, estado) VALUES(\'%s\', \'%s\' , \'%s\', \'%s\' );" % (nome_escola, endereco, cidade, estado))
  conn.commit()
  cur.close
  conn.close

def getTurmalist():
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    cur.execute("SELECT * FROM turma")
    turma_list = cur.fetchall()
    cur.close
    conn.close
    return turma_list

  
def cad_Turma(serie_turma, ano_turma, id_professor):
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    cur.execute("INSERT INTO turma (serie_turma, ano_turma, id_professor) VALUES(\'%s\', \'%s\' , \'%s\');" % (serie_turma, ano_turma, id_professor))
    conn.commit()
    cur.close
    conn.close

def getSondagemlist():
  conn = psycopg2.connect(os.environ['DATABASE_URL'])
  cur = conn.cursor()
  cur.execute("SELECT * FROM sondagem")
  sondagem_list = cur.fetchall()
  cur.close
  conn.close
  return sondagem_list

def cad_Sondagem(materia, campo_semantico, valores, data_sondagem):
  conn = psycopg2.connect(os.environ['DATABASE_URL'])
  cur = conn.cursor()
  cur.execute("INSERT INTO sondagem (materia, campo_semantico, valores_ditados, data_sondagem) VALUES(\'%s\', \'%s\' , \'%s\' , \'%s\');" % (materia, campo_semantico, valores, data_sondagem))
  conn.commit()
  cur.close
  conn.close


def getAlunolist():
  conn = psycopg2.connect(os.environ['DATABASE_URL'])
  cur = conn.cursor()
  cur.execute("SELECT * FROM aluno")
  aluno_list = cur.fetchall()
  cur.close
  conn.close
  return aluno_list

def cad_Aluno(nome_aluno, nome_responsavel1, nome_responsavel2, data_nascimento, telefone_conato, id_turma):
  conn = psycopg2.connect(os.environ['DATABASE_URL'])
  cur = conn.cursor()
  cur.execute("INSERT INTO aluno (nome_aluno, nome_responsavel1, nome_responsavel2, data_nascimento, telefone_contato, id_turma) VALUES(\'%s\', \'%s\' , \'%s\' , \'%s\' , \'%s\' , \'%s\');" % (nome_aluno, nome_responsavel1, nome_responsavel2, data_nascimento, telefone_conato, id_turma))
  conn.commit()
  cur.close
  conn.close

def getAvaliacaolist():
  conn = psycopg2.connect(os.environ['DATABASE_URL'])
  cur = conn.cursor()
  cur.execute("SELECT * FROM avaliacao")
  avaliacao_list = cur.fetchall()
  cur.close
  conn.close
  return avaliacao_list

def cad_Avaliacao(data_avaliacao, hipotese_escrita, id_aluno, id_sondagem):
  conn = psycopg2.connect(os.environ['DATABASE_URL'])
  cur = conn.cursor()
  cur.execute("INSERT INTO avaliacao (data_avaliacao, hipotese_escrita, id_aluno, id_sondagem) VALUES(\'%s\', \'%s\' , \'%s\' , \'%s\');" % (data_avaliacao, hipotese_escrita, id_aluno, id_sondagem))
  conn.commit()
  cur.close
  conn.close
#('INSERT INTO public."TaskList"(task_name, due_date) values(\'%s\', \'%s\');' % (name, date))