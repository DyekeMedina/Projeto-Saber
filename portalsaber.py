from flask import *  
import sqlite3

app = Flask(__name__, template_folder='template')


@app.route("/")

def index():
    return render_template("index.html");


@app.route("/registrar")

def registrar():
    return render_template("registrar.html")


@app.route("/salvar_registro", methods = ["POST","GET"])

def salvar_registro():
    msg = ""
    if request.method == "POST":
        try:
            nome = request.form["nome"]
            telefone = request.form["phone"]
            email = request.form["email"]
            senha = request.form["password"]

            with sqlite3.connect("portalsaber_bd.db") as con:
                cur = con.cursor()
                cur.execute("INSERT into tb_cadastro (nome, telefone, email, senha) values (?,?,?,?)",(nome,telefone,email,senha))
                con.commit()
                msg = "Cadastro realizado com sucesso!"
        except:
            con.rollback()
            msg = "Ops! Houve uma falha no seu cadastro. Por gentileza, tente novamente."
        finally:  
            return render_template("resultado.html",msg = msg)
            con.close()


@app.route("/entrar")

def entrar():
    return render_template("entrar.html")


@app.route("/login", methods=["POST","GET"])

def login():
    msg = ""
    if request.method == "POST":
        try:
            email = request.form["email"]
            senha = request.form["password"]

            with sqlite3.connect("portalsaber_bd.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM tb_cadastro WHERE email=?", (email,))
                registro = cur.fetchall()
                if registro[0][4] == senha:
                    msg = "Acesso liberado com sucesso!"
                    resp = flask.make_response()
                    resp.set_cookie("email", value = email)
                else:
                    msg = "Acesso negado!"
        except:
            con.rollback()
            msg = "Acesso negado! Tente novamente."
        finally:  
            return render_template("resultado.html",msg = msg)
            con.close()


@app.route("/contato")

def contato():
    return render_template("contato.html")


@app.route("/doar")

def doar():
    return render_template("doar.html")


@app.route("/novo_livro",methods = ["POST","GET"])

def novo_livro():
    msg = "msg"
    if request.method == "POST":
        try:
            nome = request.form["nome"]
            autor = request.form["autor"]
            estado = request.form["estado"]
            genero = request.form["genero"]
            status = "Disponível"
            email_doador = request.form["email_doador"]
            email_recebedor = ""
            
            con = sqlite3.connect("portalsaber_bd.db")
            cur = con.cursor()
            cur.execute("INSERT into tb_livros (nome, autor, estado, genero, status, email_doador, email_recebedor) values (?,?,?,?,?,?,?)",(nome,autor,estado,genero,status,email_doador,email_recebedor))
            con.commit()
            msg = "Livro cadastrado com sucesso!"
        except:
            con.rollback()
            msg = "Falha no cadastro do livro."
        finally:  
            return render_template("resultado.html",msg = msg)
            con.close()


@app.route("/biblioteca")

def biblioteca():
    con = sqlite3.connect("portalsaber_bd.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM tb_livros WHERE status='Disponível'")
    rows = cur.fetchall()
    
    return render_template("biblioteca.html",rows = rows)
    con.close

