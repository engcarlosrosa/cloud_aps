dicionario_tarefas = {}
chave_primaria = len(dicionario_tarefas)

def cria_tarefa(tarefa):
	
	global dicionario_tarefas
	global chave_primaria

	dicionario_tarefas[str(chave_primaria)] = tarefa
	chave_primaria +=1

class Tarefas(object):
	"""docstring for Tarefas"""
	def __init__(self, atributo_1, atributo_2):
		
		self.atributo_1 = atributo_1
		self.atributo_2 = atributo_2

	def muda_atributo_1(self, novo_atributo_1):
		
		self.atributo_1 = novo_atributo_1

	def muda_atributo_2(self, novo_atributo_2):

		self.atributo_2 = novo_atributo_2
		