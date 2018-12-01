from flask import Flask, Response, request, render_template, jsonify
import requests
import os.path

dicionario_tarefas = {}
indice = 1

class Tarefa(object):
	"""docstring for Tarefa"""
	def __init__(self, atributo_1, atributo_2):
		
		self.atributo_1 = atributo_1
		self.atributo_2 = atributo_2

	def muda_atributo_1(self, novo_atributo_1):
		
		self.atributo_1 = novo_atributo_1

	def muda_atributo_2(self, novo_atributo_2):

		self.atributo_2 = novo_atributo_2

	def serialize(self):
		return {'atributo_1': self.atributo_1, 'atributo_2': self.atributo_2}

	
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
	print(request.method)
	if request.method == 'POST':
		
		dado = request.json

		try:
			dado = request.json
			print(dado)
			valor = Tarefa(dado["a1"], dado["a2"])

			print(len(dicionario_tarefas))

			if len(dicionario_tarefas) == 0:
				indice = 1
			else:
				indice = len(dicionario_tarefas) + 1


			print(dicionario_tarefas)
			print(valor)

			dicionario_tarefas[str(indice)] = valor

			print(dicionario_tarefas)

			return jsonify(dado), 200
		except:
			print("POST ERROR")

	elif request.method == 'GET':
		print("A")
		print(dicionario_tarefas)
		#return {'tarefas': [marshal(task, task_fields) for task in dicionario_tarefas]}, 200
		return jsonify(dicionario_tarefas=[v.serialize() for k,v in dicionario_tarefas.items()]), 200
		#return jsonify({ 'tarefas' : dicionario_tarefas }), 200
		#return jsonify([marshal(e, tarefas_tipos) for e in dicionario_tarefas]), 200

@app.route("/Tarefa/<int:id_>",methods=['GET', 'PUT', 'DELETE'])
def atualiza(id_):
	if request.method == 'GET':
		print(dicionario_tarefas[str(id_)])
		return "Tarefa/id/GET"

	elif request.method == 'PUT':
		valor = str(request.get_data())
		print(valor)
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
    app.run(debug=True, host="0.0.0.0")