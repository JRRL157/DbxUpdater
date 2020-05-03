import os
import zlib
from os.path import isdir,isfile,join
import bz2
import json

def file_checksum(nome):
	try:
		f = open(nome,'rb');
		checksum = zlib.adler32(f.read())
		f.close();
		return checksum
	except IOError:
		return -1;

#Entra na pasta e cria os checksums dos arquivos e seus respectivos arquivos zipados
def folder(pasta,root):
	ArquivosEPastas = [f for f in (os.listdir(pasta)) if ((f not in pasta) and (root not in f) and ('.py' not in f))]

	try:
		os.mkdir(root+"/"+pasta)
	except OSError:
	    None;
	else:
	    None;

	#pegará o hash dos arquivos e criará os seus respectivos arquivos bzip2
	for name in ArquivosEPastas:
		if not isfile(pasta+"/"+name):
			folder(pasta+"/"+name,root)
			continue

		print(pasta+"/"+name)

		if pasta == '.':
			hash = file_checksum(name)
			HashFiles[name] = hash
		else:
			hash = file_checksum(pasta+'/'+name)
			HashFiles[pasta+'/'+name] = hash		

		if pasta != '.':
			z = bz2.BZ2File(root+"/"+pasta+"/"+name+".bz2",'wb')
			f = open(pasta+'/'+name,'rb')
		else:
			z = bz2.BZ2File(root+"/"+name+".bz2",'wb')
			f = open(name,'rb')

		try:
			z.write(f.read());
		finally:
			z.close();

		f.close()


root = input("Digite o nome do diretório raiz dos arquivos que serão enviados ao cliente, Ex.: Server: ")

#guardará os hash de todos os arquivos que serão baixados
HashFiles = {};

#Criando o diretório raiz onde ficarão os arquivos de download
try:
	os.mkdir(root)
except OSError:
	None;
else:
	None;

#Verificando todos os arquivos e pastas do diretório atual
folder('.',root)

#criando o arquivo json
f = open(root+"/list.json","w")
f.close()

#Adicionando nomes e hashes ao arquivo JSON
j = root+"/list.json"

if j:
	with open(j,'a') as f:
		json.dump(HashFiles,f)
