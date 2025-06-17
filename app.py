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
import random


acento_correto = {
    # Agudo
    "eletrico": "agudo",
    "herois": "agudo",
    "aneis": "agudo",
    "lapide": "agudo",
    "papeis": "agudo",
    "sois": "agudo",
    "areas": "agudo",
    "medios": "agudo",
    "nectar": "agudo",
    "memoria": "agudo",
    "pergola": "agudo",
    "regias": "agudo",
    "magicos": "agudo",
    "frageis": "agudo",
    "calcio": "agudo",
    "juri": "agudo",
    "fertil": "agudo",
    "polis": "agudo",
    "palido": "agudo",
    "ludico": "agudo",
    "fe": "agudo",
    "series": "agudo",
    "fabula": "agudo",
    "serios": "agudo",
    "midias": "agudo",
    "principe": "agudo",
    "colegio": "agudo",
    "reu": "agudo",
    "podio": "agudo",
    "album": "agudo",
    "icones": "agudo",
    "medicas": "agudo",
    "nivel": "agudo",
    "jubilo": "agudo",
    "regua": "agudo",
    "credito": "agudo",
    "serie": "agudo",
    "sintese": "agudo",
    "vitoria": "agudo",
    "predio": "agudo",
    "sequito": "agudo",
    "seculo": "agudo",
    "carie": "agudo",
    "plagio": "agudo",
    "pesames": "agudo",
    # Circunflexo
    "edificio": "agudo",
    "quimico": "agudo",
    "codigo": "agudo",
    "mistico": "agudo",
    "cafe": "agudo",
    "sofa": "agudo",
    "arvore": "agudo",
    "lapis": "agudo",
    "eletrons": "agudo",
    "relogio": "agudo",
    "exercito": "agudo",
    "genio": "agudo",
    "cupulas": "agudo",
    "epoca": "agudo",
    "sabado": "agudo",
    "perimetro": "agudo",
    "apice": "agudo",
    "latex": "agudo",
    "torax": "agudo",
    "cortex": "agudo",
    "vortex": "agudo",
    "circulo": "agudo",
    "taxis": "agudo",
    "juiz": "agudo",
    "bari": "agudo",
    "cerebro": "agudo",
    "exito": "circunflexo",
    "exodo": "circunflexo",
    "onus": "circunflexo",
    "angulo": "circunflexo",
    "fenix": "circunflexo",
    "fenomeno": "circunflexo",
    "tremulo": "circunflexo",
    "bebado": "circunflexo",
    "orgao": "circunflexo",
    "cromico": "circunflexo",
    "vovo": "circunflexo",
    "torax": "circunflexo",
    "tibio": "circunflexo",
    "obvio": "circunflexo",
    "subito": "circunflexo",
    "tenue": "circunflexo",
    "traves": "circunflexo",
    "custodio": "circunflexo",
    "comodo": "circunflexo",
    "omega": "circunflexo",
    "genese": "circunflexo",
    "lemures": "circunflexo",
    "poneis": "circunflexo",
    "bebados": "circunflexo",
    "semen": "circunflexo",
    "concavo": "circunflexo",
    "onix": "circunflexo",
    "ambar": "circunflexo",
    "comico": "circunflexo",
    "bonus": "circunflexo",
    "pendulos": "circunflexo",
    "computo": "circunflexo",
    "volei": "circunflexo",
    "tempora": "circunflexo",
    "textil": "circunflexo",
    "fenix": "circunflexo",
    "canhamo": "circunflexo",
    "pensil": "circunflexo",
    "angulo": "circunflexo",
    "fenomeno": "circunflexo",
    "gemeo": "circunflexo",
    "exodo": "circunflexo",
    "onus": "circunflexo",
    "folego": "circunflexo",
    "candido": "circunflexo",
    # Til
    "mamoes": "til",
    "limoes": "til",
    "feijoes": "til",
    "botoes": "til",
    "leoes": "til",
    "avioes": "til",
    "baloes": "til",
    "portao": "til",
    "irmao": "til",
    "tubarao": "til",
    "fogoes": "til",
    "peoes": "til",
    "coracoes": "til",
    "ladrao": "til",
    "violao": "til",
    "botao": "til",
    "dragao": "til",
    "alemao": "til",
    "sabao": "til",
    "galao": "til",
    "bençao": "til",
    "paes": "til",
    "nao": "til",
    "alçapao": "til",
    "corujao": "til",
    "campeao": "til",
    "arranhao": "til",
    "quinhao": "til",
    "trovao": "til",
    "trovoes": "til",
    "caixao": "til",
    "leaozinho": "til",
    "anciao": "til",
    "charlatao": "til",
    "caozinho": "til",
    "camarao": "til",
    "pavao": "til",
    "pao": "til",
    "mao": "til",
    "chao": "til",
    "grao": "til",
    "sabao": "til",
    "timao": "til",
    "simao": "til",
    "talao": "til",
    "torao": "til",
    "corao": "til",
    "mamao": "til",
    "furao": "til",
    "tubarao": "til",
    # Sem acento
    "porta": "sem acento",
    "cadeira": "sem acento",
    "mochila": "sem acento",
    "sapato": "sem acento",
    "vaso": "sem acento",
    "planta": "sem acento",
    "tigela": "sem acento",
    "animal": "sem acento",
    "rua": "sem acento",
    "pedra": "sem acento",
    "livro": "sem acento",
    "tela": "sem acento",
    "sino": "sem acento",
    "mesa": "sem acento",
    "papel": "sem acento",
    "caneta": "sem acento",
    "garfo": "sem acento",
    "faca": "sem acento",
    "prato": "sem acento",
    "colher": "sem acento",
    "panela": "sem acento",
    "copo": "sem acento",
    "balde": "sem acento",
    "carro": "sem acento",
    "disco": "sem acento",
    "violino": "sem acento",
    "gato": "sem acento",
    "cachorro": "sem acento",
    "terra": "sem acento",
    "fogo": "sem acento",
    "gelo": "sem acento",
    "neve": "sem acento",
    "areia": "sem acento",
    "rocha": "sem acento",
    "caverna": "sem acento",
    "gruta": "sem acento",
    "poco": "sem acento",
    "fonte": "sem acento",
    "trilha": "sem acento",
    "ponte": "sem acento",
    "estrada": "sem acento",
    "cidade": "sem acento",
    "vila": "sem acento",
    "bairro": "sem acento",
    "parque": "sem acento",
    "mercado": "sem acento",
    "loja": "sem acento",
    "hospital": "sem acento",
    "igreja": "sem acento",
    "templo": "sem acento",
    "casa": "sem acento",
    "barraca": "sem acento",
    "cabana": "sem acento",
    "castelo": "sem acento",
    "povo": "sem acento",
    "sombra": "sem acento",
    "segredo": "sem acento",
    "perfume": "sem acento",
    "retrato": "sem acento",
    "farol": "sem acento",
    "barco": "sem acento",
    "aldeia": "sem acento",
    "barragem": "sem acento",
    "moinho": "sem acento",
    "geleira": "sem acento",
    "estreito": "sem acento",
    "cacto": "sem acento",
    "trilho": "sem acento",
    "lenha": "sem acento",
    "capim": "sem acento",
    "bambu": "sem acento",
    "trevo": "sem acento",
    "bosque": "sem acento",
}



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
    todas_palavras = list(acento_correto.keys())
    feedback = None
    if request.method == "GET":
        palavras = random.sample(todas_palavras, 4)
        return render_template('ortofix.html', palavras=palavras, feedback=feedback)

    acao = request.form.get("acao")
    if acao == "novas":
        palavras = random.sample(todas_palavras, 4)
        feedback = None
        return render_template('ortofix.html', palavras=palavras, feedback=feedback)
    else:
        palavras = []
        for i in range(4):
            palavra = request.form.get(f'palavra_{i}')
            if palavra:
                palavras.append(palavra)
        
        respostas_usuario = []
        for i, palavra in enumerate(palavras):
            resposta = request.form.get(f"acento_{i}")
            respostas_usuario.append({
                "palavra": palavra,
                "resposta_usuario": resposta,
                "acento_correto": acento_correto[palavra]
            })
        prompt = """Você é um assistente de ortografia.
        Para cada palavra abaixo, forneça o feedback seguindo exatamente esta estrutura, sem adicionar comentários ou exemplos extras:
        - Palavra: [palavra]
        - Sua resposta: [resposta do aluno]
        - Resposta correta: [resposta correta]
        - Resultado: [Correto! ou Incorreto.]
        - Explicação: [Explique de forma breve e educativa a regra de acentuação ou o motivo da resposta estar correta ou incorreta.]"""
        for item in respostas_usuario:
            prompt += f"Palavra: {item['palavra']} | Resposta do aluno: {item['resposta_usuario']} | Resposta correta: {item['acento_correto']}\n"
        import google.generativeai as genai
        model = genai.GenerativeModel("gemini-1.5-flash") 
        response = model.generate_content(prompt)
        feedback = response.text
        return render_template('ortofix.html', palavras=palavras, feedback=feedback)
if __name__=='__main__':
    app.run(debug=True)
