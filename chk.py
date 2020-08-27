#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" controlla i file .h"""
import os
import sys
import string
import subprocess

def extgetcmd(comando):
	""" run a program and get the results.
	:param comando: the command line that will be launched
	:return: output of the command line
	"""
	if os.name == "nt":
		comando = comando.replace("'", "\"")

	arr = []
	p = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	for line in p.stdout.readlines():
		try:
			arr.append(line.strip().decode('ascii'))
		except:
			try:
				arr.append(line.strip().decode('utf-8'))
			except:
				arr.append(line.strip().decode('ascii', 'ignore'))
		p.wait()
		#retval = p.wait()

	return "\n".join(arr)

	
def readfile(fn):
	global lavoro
	# sdir = "D:\\auton\+uscita"
	sdir = "./" #"D:\\prog"
	contatore = 1
	nomefile = os.path.join(sdir, fn)
	if not nomefile[-2:] == ".h":
		nomefile += ".h"
	
	#se non c'e' chiudo
	if not os.path.exists(nomefile):
		print(nomefile + " non esiste")
		sys.exit()
	print("####################")
	beginning = False
	lavoro = "xxxx"
	commento = ""
	f = open(nomefile)
	line = f.readline()
	while line:
		contatore += 1
		if line.strip().isdigit():
			print(line)
		if line.startswith("TOOL CALL "):
			arr = line.split(" ")
			print("----------------------------------")
			print("Utensile " + arr[2] + " velocita' " + arr[4])
		elif line.startswith("M8"):
			print("Refrigerante attivo")
		elif line.startswith("M08"):
			print("Refrigerante attivo")
		elif line.startswith("M9"):
			print("  Refrigerante chiuso")
		elif line.startswith("M3"):
			if line.startswith("M30"):
				print("  Fine programma")
			elif line.startswith("M35"):
				print("  Convogliatore spento")
			elif line.startswith("M36"):
				print("  Convogliatore acceso")
		elif line.startswith("M77"):
			print("  Spengimento macchina")
		
		if line.find(" M13") > 0:
			print("Refrigerante attivo")
		
		if line.startswith(";"):
			if beginning == False:
				beginning = True
				commento = line
			else:
				commento += line[1:]
		else:
			if beginning == True:
				print(processcommento(commento))
				beginning = False
				commento = ""
		line = f.readline()
	f.close()
	print("Totale linee: " + str(contatore))
	
def processcommento(comm):
	res = ""
	comm = comm[comm.find("\n") + 1:]
	comm = comm.lower().replace("\r\n", "")
	comm = comm.lower().replace("\n", "")
	comm = comm.replace(",", " ")
	arr = comm.split()
	
	if arr:
		if "roughing" in arr:
			res = "\nLavorazione = SGROSSATURA"
		if "zmill" in arr:
			res = "\nLavorazione = FRESATURA ZMILL"	
		if "pmill" in arr:
			res = "\nLavorazione = PIANI PMILL"
		for s in sorted(arr):
			if s.startswith("f"):
				if s[1:].isdigit():
					res += "\nAvanzamento: " + s[1:]
			if s.startswith("zmin-") or \
				s.startswith("zmin+") or \
				s.startswith("zmax-") or \
				s.startswith("zmax+"):
					res += "\n" + s.upper()
			if s.startswith("svr"):
				res += "\nSVR " + s


	return res

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Devi scrivere chk.py nomedelfile.")
		sys.exit()
	else:
		spath=os.path.abspath(os.path.dirname(__file__))

		arg1 = sys.argv[1]
		readfile(arg1)

	for i in range(1, len(sys.argv)):
		t = sys.argv[i]
		if t == "--build":
			if i < len(sys.argv) - 1:
				arg = sys.argv[i + 1]
				if os.path.exists(arg):
					readfile(arg)
			else:
				pass
