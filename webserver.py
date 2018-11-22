from flask import Flask, Response, request, render_template
import requests
import os.path
from aps_1 import *

def diretorio():
	return os.path.abspath(os.path.dirname(__file__))

def get_file(filename):
	try:
		src = os.path.join(diretorio(), filename)
		return open(src).read()

	except IOError as e:
		return str(e)
		
app = Flask(__name__)

server_addr = 'https://http://127.0.0.1:5000/'


@app.route("/", methods=['GET'])
def indice():
	
	conteudo = get_file('home.html')
	return Response(conteudo, mimetype="text/html")

@app.route("/Tarefa/", methods=['POST', 'GET'])
def tarefas():
	if request.method == 'POST':
		try:
			dado = request.get_json()
			valor = dado.split(":")[1]
			cria_tarefa(valor)
			return "Tarefa/POST"
		except:
			print("POST ERROR")

		else:
			try:
				lista = []

				for chave, valor in dicionario_tarefas.items():
					lista.append(valor)

				print(lista)
				return "Tarefa/GET"

			except:
				return "Tarefa/GET ERROR"

@app.route("/Tarefa/<int:id_>",methods=['GET', 'PUT', 'DELETE'])
def atualiza(id_):
	if request.method == 'GET':
		print(dicionario_tarefas[str(id_)])
		return "Tarefa/id/GET"

	elif request.method == 'PUT':
		valor = str(request.get_data())
		valor = valor.split("=")[1]
		dicionario_tarefas[str(id_)] = valor
		return "Tarefa/id/PUT"

	elif request.method == 'DELETE':
		del dicionario_tarefas[str(id_)]
		return "Tarefa/id/DELETE"

@app.route("/healthcheck/")
def healthcheck():
	return "200"

if __name__ == '__main__':
    app.run(debug=True)