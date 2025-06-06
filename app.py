from flask import Flask, render_template, request, redirect, session, send_from_directory, jsonify
from mysql.connector import Error
from flask_cors import CORS
import google.generativeai as genai
from config import *
from db_functions import *
import os
from dotenv import load_dotenv
import json
import requests


acentoagudo = ["heróis, anéis, edifício, lápide, papéis, sóis, áreas, médios, néctar, memória, pérgola, régias, mágicos, frágeis, cálcio, júri, fértil, pólis, pálido, lúdico, fé, séries, fábula, sérios, mídias, príncipe, colégio, réu, pódio, álbum, ícones, médicas, nível, júbilo, régua, químico, crédito, código, série, síntese, vitória, prédio, místico, séquito, século, cárie, plágio"]

acentocircunflexo = ["pêsames, cômodo, ômega, gênese, lêmures, cúpulas, mênstruos, elétrons, pôneis, bêbados, sêmen, âmago, côncavo, ônix, âmbar, cômico, bônus, pêndulos, êxitos, cômputo, vôlei, têmpora, têxtil, fênix, elétrico, cânhamo, pênsil, êxito, ângulo, fenômeno, gêmeo, êxodo, ônus, fôlego, cúpula, exército, cândido, sólido, lícito, vácuo"]

acentotil = ["mamões, limões, feijões, botões, leões, aviões, balões, portão, irmão, tubarão, fogões, peões, corações, ladrão, violão, botão, dragão, alemão, sabão, galão, bênção, pães, não, alçapão, corujão, campeão, arranhão, quinhão, trovão, trovões, caixão, leãozinho, ancião, charlatão, cãozinho"]

semacento = ["porta, cadeira, mochila, sapato, vaso, planta, tigela, animal, rua, pedra, livro, tela, sino, mesa, papel, caneta, garfo, faca, prato, colher, panela, copo, balde, carro, disco, violino, gato, cachorro, rato, urso, peixe, sol, lua, estrela, planeta, mar, rio, lago, montanha, floresta, chuva, vento, tempestade, nuvem, terra, fogo, gelo, neve, areia, rocha, caverna, gruta, poço, fonte, trilha, ponte, estrada, cidade, vila, bairro, parque, mercado, loja, hospital, igreja, templo, casa, barraca, cabana, castelo, povo, sombra, segredo, perfume, retrato, farol, barco, aldeia, barragem, moinho, geleira, estreito, cacto, trilho, lenha, capim, bambu, trevo, toco, tronco, galho, folha, florada, sementeira, regato, charco, pasto, sitio, curral, colina, encosta, baixada, bosque, mato, selva, savana, manguezal, brejo, abismo, penhasco, escarpa,  vertente, cascata, cachoeira, corredeira, delta, duna, lagoa, enseada, fiorde, ilhota, atalho, picada, vereda, esplanada, pomar, vinhedo, plantio, lavoura, rocado,  milharal,  jabuti, lambari, surubim, cascudo, pacu"]

load_dotenv()

app = Flask(__name__)
app.secret_key = 'oi'
CORS(app)

genai.configure(api_key=os.getenv("apikey"))  

model = genai.GenerativeModel("gemini-1.5-flash", generation_config={"temperature": 1.2})



@app.route('/', methods=['GET', 'POST'])
def login():
    

    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        if not email or not senha:
            erro = "Os campos precisam estar preenchidos!"
            return render_template('login.html', msg_erro=erro)
        
        if email == MASTER_EMAIL and senha == MASTER_PASSWORD:
            session['adm'] = True
            return redirect('/adm')

        try:
            conexao, cursor = conectar_db()
            comandoSQL = 'SELECT * FROM aluno WHERE email = %s AND senha = %s'
            cursor.execute(comandoSQL, (email, senha))
            aluno = cursor.fetchone()

            if aluno:
                if aluno['status'] == 'inativo':
                    return render_template('login.html', msgerro='Aluno desativado! Procure o administrador!')
                session['idAluno'] = aluno['idAluno']
                session['nomeAluno'] = aluno['nomeAluno']
                return redirect('/aluno')  

            # Se não for aluno, tenta como professor
            comandoSQL = 'SELECT * FROM professores WHERE email = %s AND senha = %s'
            cursor.execute(comandoSQL, (email, senha))
            professor = cursor.fetchone()

            if professor:
                session['idProfessor'] = professor['idProfessor']
                session['nomeProfessor'] = professor['nomeProfessor']
                return redirect('/professor')  

            return render_template('login.html', msgerro='E-mail e/ou senha estão errados!')

        except Error as erro:
            return f"ERRO! Erro de Banco de Dados: {erro}"
        except Exception as erro:
            return f"ERRO! Outros erros: {erro}"
        finally:
            encerrar_db(cursor, conexao)

        
@app.route('/aluno', methods=['GET'])
def aluno():
    if not session:
        return redirect('/login')
        
    if 'adm' in session:
        return redirect('/adm')

@app.route('/professor', methods=['GET'])
def professor():
    if not session:
        return redirect('/login')
    
    if not session['adm']:
        return redirect('/login')

@app.route('/cadastraraluno', methods=['POST', 'GET'])
def cadastraraluno():
    
    #if not session:
        #return redirect('/login')
    
    if request.method == 'GET':
        return render_template('cadastrar_aluno.html')
    
    #tratando os dados do form
    if request.method == 'POST':
        nomeAluno = request.form['nomeAluno']
        cpfAluno = limpar_input(request.form['cpfAluno'])
        emailAluno = request.form['emailAluno']
        senhaAluno = request.form['senhaAluno']

        #Verificar
        if not nomeAluno or not cpfAluno  or not emailAluno or not senhaAluno:
            return render_template('cadastrar_aluno.html', msg_erro="Todos os campos são obrigatórios!")
        
        try:
            conexao, cursor = conectar_db()
            comandoSQL = 'INSERT INTO Aluno (nomeAluno, cpfAluno, emailAluno ,senhaAluno) VALUES (%s,%s,%s,%s)'
            cursor.execute(comandoSQL, (nomeAluno, cpfAluno, emailAluno, senhaAluno))
            conexao.commit() #envia os dados para o BD
            return redirect('/adm')
        except Error as erro:
            if erro.errno == 1062:
                return render_template('cadastrar_aluno.html', msg_erro="Já existe um aluno com esse Email!")
            else:
                return f"Erro de BD: {erro}"
        except Exception as erro:
            return f"Erro de BackEnd: {erro}"
        finally:
            encerrar_db(cursor, conexao)

    
    #if not session['adm']:
        #return redirect('/login')

@app.route('/editaraluno/<int:idAluno>', methods=['POST', 'GET'])
def editaraluno(idAluno):
    if not session:
        return redirect('/login')
    
    if not session['adm']:
        return redirect('/login')
    
    if request.method == 'GET':
        try:
            conexao, cursor = conectar_db()
            comandoSQL = 'SELECT * FROM Aluno WHERE idAluno = %s'
            cursor.execute(comandoSQL, (idAluno,))
            aluno = cursor.fetchone()
            return render_template('editar_aluno.html', aluno=aluno)
        except Error as erro:
            return f"Erro de BD: {erro}"
        except Exception as erro:
            return f"Erro de BackEnd: {erro}"
        finally:
            encerrar_db(cursor, conexao)

            #tratando os dados do form
    if request.method == 'POST':
        nomeAluno = request.form['nomeAluno']
        cpfAluno = limpar_input(request.form['cpfAluno'])
        emailAluno = request.form['emailAluno']
        senhaAluno = request.form['senhaAluno']

        #Verificar
        if not nomeAluno or not cpfAluno or not emailAluno or not senhaAluno:
            return render_template('editar_aluno.html', msg_erro="Todos os campos são obrigatórios!")
        
        try:
            conexao, cursor = conectar_db()
            comandoSQL = '''
            UPDATE aluno
            SET nomeAluno = %s, cpf = %s, email = %s, senha = %s WHERE idAluno = %s;
            '''
            cursor.execute(comandoSQL, (nomeAluno, cpfAluno, emailAluno, senhaAluno, idAluno))
            conexao.commit() #envia os dados para o BD
            return redirect('/adm')
        except Error as erro:
            if erro.errno == 1062:
                return render_template('editar_aluno.html', msg_erro="Já existe um aluno com esse Email!")
            else:
                return f"Erro de BD: {erro}"
        except Exception as erro:
            return f"Erro de BackEnd: {erro}"
        finally:
            encerrar_db(cursor, conexao)
    if not session['adm']:
        return redirect('/login')
    
@app.route('/adm')
def adm():
    
    if not session:
        return redirect('/login')
    
    if not 'adm' in session:
        return redirect('/')
  
    try:
        conexao, cursor = conectar_db()
        comandoSQL = 'SELECT * FROM Aluno WHERE status = "ativo"'
        cursor.execute(comandoSQL)
        alunos_ativos = cursor.fetchall()

        comandoSQL = 'SELECT * FROM Aluno WHERE status = "inativo"'
        cursor.execute(comandoSQL)
        alunos_inativos = cursor.fetchall()

        return render_template('adm.html', alunos_ativos=alunos_ativos, alunos_inativos=alunos_inativos)
    except Error as erro:
        return f"ERRO! Erro de Banco de Dados: {erro}"
    except Exception as erro:
        return f"ERRO! Outros erros: {erro}"
    finally:
        encerrar_db(cursor, conexao)



def feedbackaluno():
    prompt = """
    Você é um assistente de ortografia para o jogo OrtoFix.

    O aluno recebe uma lista de palavras e deve escolher o tipo de acento correto para cada uma:

    Agudo (´)

    Circunflexo (^)

    Til (~)

    Sem acento

    Para cada palavra, avalie a resposta do aluno em relação ao gabarito correto.

    Para cada item, siga este formato de feedback:

    Se o aluno acertou, diga "Correto!", explique rapidamente a regra de acentuação da palavra.

    Se o aluno errou, diga "Incorreto.", informe qual seria o acento correto e explique a regra de acentuação de forma simples.

    Exemplo de entrada:
    Palavra: "herois" | Resposta do aluno: "agudo" | Resposta correta: "agudo"

    Exemplo de saída:

    "Correto! 'Heróis' leva acento agudo no 'i' porque é uma palavra oxítona terminada em 'i(s)'."

    Outro exemplo de entrada:
    Palavra: "porta" | Resposta do aluno: "agudo" | Resposta correta: "sem acento"

    Exemplo de saída:

    "Incorreto. 'Porta' não leva acento porque é uma palavra paroxítona terminada em 'a', que não recebe acento."

    Use sempre explicações curtas, educativas e motivadoras.


    Gere um feedback individual para cada palavra.


    """
    
    response = model.generate_content(prompt)
    texto = response.text.strip()



@app.route("/ortofix", methods=["GET", "POST"])
def ortofix():
    palavras = feedbackaluno()
    return render_template('ortofix.html', palavras=palavras)


if __name__=='__main__':
    app.run(debug=True)
