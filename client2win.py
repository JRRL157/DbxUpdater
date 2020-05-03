import dropbox
import json
import bz2
import os
import zlib
from time import perf_counter
from random import randint
from os.path import isdir,isfile,join

ACCESS_KEY = 'sTDm3mz5lVAAAAAAAAAAKb9cO5NdCVWAyYpmt9k7wjiWFyrX7m4G0_yM-Un59I7r'
ROOT = '/Server'

def file_checksum(nome):
	try:
		f = open(nome,'rb');
		checksum = zlib.adler32(f.read())
		f.close();
		return checksum
	except IOError:
		return -1;

def jsonToDic(jsonFile):
	dic = {}

	with open(jsonFile) as f:
		dic = json.load(f)

	return dic

def ParaBaixar(dic):
	baixar = []
	for x in dic:
		#comparando o arquivo local com o JSON
		
		print("Checking "+x+".......",end='')
		print(file_checksum(x))
		
		if file_checksum(x) != dic[x]:
			baixar.append(x)
			print("NO!")
		else:
			print("YES!")
	return baixar

def creating_paths(path,partes):
	item = partes.pop(0)

	if len(partes) == 0:
		return

	try:
		os.mkdir(path+"/"+item)
	except OSError:
	    None;
	else:
	    None;

	creating_paths(path+"/"+item,partes)

def Dir_Creator(path):
	creating_paths('.',path.split('/')[1:])

try:
	dbx = dropbox.Dropbox(ACCESS_KEY)
	print("Conexão estabelecida com sucesso!")
except:
	print("Error ao estabelecer conexão!")

''' Arquivo de checksums .JSON '''
metadata,res = dbx.files_download(path='/Server/list.json')
while (metadata,res) == ('not_found',None):
	metadata,res = dbx.files_download(path="/Server/list.json")

#dicionário dos arquivos contendo os nomes e checksums
dic = json.loads(res.content.decode())

#Arquivos que serão baixados
baixar = ParaBaixar(dic)

#Baixando os arquivos necessários no PC
for path in baixar:	

	#Criando os diretórios necessários para salvar os arquivos
	Dir_Creator(path)

	#Caminho do dropbox
	caminho_dropbox = path + ".bz2"
	
	print("Downloading "+caminho_dropbox+".......")
	
	########################## BAIXANDO DO DROPBOX ########################

	with open(caminho_dropbox, "wb") as f:		
		metadata, res = dbx.files_download(path=ROOT+caminho_dropbox[1:])
		
		try:
			f.write(res.content)
		except:
			print("Erro ao escrever "+caminho_dropbox+"!")

	########################## BAIXANDO DO DROPBOX ########################
	
	
	print("Extracting "+caminho_dropbox+".......")

	try:
		#Abrindo o arquivo .bz2
		with bz2.BZ2File(caminho_dropbox) as zipfile:
			data = zipfile.read()		
	
		caminho_descomprimido = caminho_dropbox[:-4]	#Removendo o '.bz2' do final da string
	
		open(caminho_descomprimido,'wb').write(data)	
	except:
		print("Erro ao extrair arquivo!")

	#Deletando o arquivo zipado	
	try:
		os.remove(caminho_dropbox)
	except:
		print("Erro ao remover "+caminho_dropbox+"!")