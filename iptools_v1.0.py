#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import argparse
from netaddr import *
from tabulate import tabulate
import socket
import struct

def cidr(prefix):
    return socket.inet_ntoa(struct.pack(">I", (0xffffffff << (32 - prefix)) & 0xffffffff))

def cabeceras(opcion):
	cabecera1=['IP','Version', 'Mascara', 'Tipo']
	cabecera2=['IP','Version', 'Mascara', 'Tipo', 'Clase']
	cabecera3=['HOST #', 'DIRECCION IP', 'USABLE?']
	cabecera4=['SUBRED #', 'ID DE RED', 'DIR BROADCAST']
	if opcion == 1:
		return cabecera1
	elif opcion == 2:
		return cabecera2
	elif opcion == 3:
		return cabecera3
	elif opcion == 4:
		return cabecera4

def obtenerClaseIP(ip):
	direccionip = ip.split('.')
	primerOcteto = int(direccionip[0])
	if(primerOcteto >= 1 and primerOcteto <=127):
		return 'A'
	elif(primerOcteto >=128 and primerOcteto <=191):
		return 'B'
	elif(primerOcteto >= 192 and primerOcteto <= 223):
		return 'C'
	else:
		return 'Unknown'
def aproximarMascara(claseIP):
	if (claseIP == 'A'):
		return '255.0.0.0'
	elif(claseIP == 'B'):
		return '255.255.0.0'
	elif(claseIP=='C'):
		return '255.255.255.0'
	else:
		return 'Unknown'
def obtenerTipoIP(ip):
	if(ip.is_private()):
		return 'Privada'
	elif(ip.is_loopback()):
		return 'LoopBack'
	elif(ip.is_multicast()):
		return 'Multicast'
	elif(ip.is_reserved()):
		return 'Reservada'
	elif(ip.is_unicast() and not ip.is_private()):
		return 'Publica'
	else:
		return 'Unknown'
def subnetNetwork(subredes, CIDR):
	print "\nSubredes Totales >> %d \nSubredes Usables >> %d" % (len(subredes), len(subredes)-2)
	print "Mascara de subred personalizada >> " + str(cidr(CIDR))
	count2 = 1
	for subred in subredes:
		dir_list=[]
		count1 = 1
		print "\n"
		print (tabulate([[count2, str(subred.network), str(subred.broadcast)]], cabeceras(4), tablefmt="pipe", numalign="center", stralign="center"))
		for ip in IPNetwork(subred):
			listatemporal=[]
			listatemporal.append(count1)
			listatemporal.append(ip)
			if count1 == 1:
				listatemporal.append('NO')
			else:
				listatemporal.append('SI')
			count1 +=1
			dir_list.append(listatemporal)
		dir_list[count1-2][2]='NO'
		print (tabulate(dir_list, cabeceras(3), tablefmt="grid", numalign="center", stralign="center"))
		count2 += 1
def main():
	parser=argparse.ArgumentParser(description='IPv4 Tools v1.0')
	requiredNamed = parser.add_argument_group('REQUERIDO')
	requiredNamed.add_argument('--dir-ip', '-i', dest='direccion_ip', help='IP en formato de numeros y puntos (numbers and dots) e.g --dir-ip 1.1.1.1 Puedes indicar la mascara con notacion CIDR e.g. -i 1.1.1.1/8', required=True, )
	parser.add_argument('--info', '-f',action='store_true', help='Muestra información sobre la IP')
	subnetgroup = parser.add_argument_group('opciones para subnetting')
	subnetgroup.add_argument('--subnet', '-s', action='store_true', help='Indica que se hará un subnetting de le IP dada. Si la IP no tiene su prefijo CIDR (/24 ..) se aproximará de acuerdo a su clase.')
	subnetgroup.add_argument('--cidr', '-c', dest='CIDR', type=int, help='Indica el nuevo prefijo (máscara personalizada) con el que se hará el subnetting. Indicar en notacion CIDR. E.g. --subnet --cidr 28 ó -s -c 28')
	subnetgroup.add_argument('--nhost', '-t', dest='hostrequeridos', type=int, help='Display Help')
	subnetgroup.add_argument('--nsubredes', '-r', dest='subredesrequeridas', type=int, help='Display Help')
	parser.add_argument('--tocidr', action='store_true', help='Convierte una mascara de red de notacion de números y puntos a CIDR')
	parser.add_argument('--out', '-o', dest='archivo', help='Genera la salida en el archivo de texto indicado')
	if(len(sys.argv) == 1 or len(sys.argv) == 3):
		parser.print_help()
		exit(0)
	args = parser.parse_args()
	try:
		miip = IPNetwork(args.direccion_ip)
		mimascara=miip.netmask
	except:
		print "Dirección IP inválida (%s)\n" % args.direccion_ip
		parser.print_help()
		exit (1)
	if args.archivo:
		print "Ejecutando'{}'".format(__file__)
		print "Creando archivo: %s" % args.archivo
		sys.stdout = open(args.archivo, 'w+')

	if args.info:
		if IPAddress(mimascara).netmask_bits() == 32:
			mimascara = aproximarMascara(obtenerClaseIP(args.direccion_ip))
		else:
			mimascara = miip.netmask
		tipo = obtenerTipoIP(miip)
		if (tipo=='Publica'):
			clase=obtenerClaseIP(args.direccion_ip)
			salida= [[str(miip.ip), "IPv"+str(miip.version), str(mimascara), tipo, clase]]
			print tabulate(salida, cabeceras(2), tablefmt="grid", numalign="center", stralign="center")
		else:
			salida= [[str(miip.ip), "IPv"+str(miip.version), str(mimascara), tipo]]
			print tabulate(salida, cabeceras(1), tablefmt="grid", numalign="center", stralign="center")
	if args.subnet:
		if IPAddress(mimascara).netmask_bits() == 32:
			mimascara = aproximarMascara(obtenerClaseIP(args.direccion_ip))
			miip.prefixlen = IPAddress(mimascara).netmask_bits()
		else:
			mimascara = miip.netmask
		if args.CIDR:
			if args.CIDR > 30: #or args.CIDR < mimascara#:
				print "Error: El CIDR no debe ser mayor a 30 (ingresado: %d)" % (args.CIDR)
				exit(1)
			subredes = list(miip.subnet(args.CIDR))
			subnetNetwork(subredes, args.CIDR)
		elif args.hostrequeridos:
			num = 32-IPAddress(miip.netmask).netmask_bits()
			numero_host=[]
			for x in range (num,0,-1):
				numero_host.append(2**x)
			nhost = args.hostrequeridos + 2
			for idx, value in reversed(list(enumerate(numero_host))):
				if value >= nhost:
					break
			if len(numero_host)-idx == len(numero_host):
				print "Error: Numero de host excede el espacio para subnetting."
				exit (1)
			nuevoCIDRhost = miip.prefixlen + idx
			subredes = list(miip.subnet(nuevoCIDRhost))
			subnetNetwork(subredes, nuevoCIDRhost)
		elif args.subredesrequeridas:
			num = 32-IPAddress(mimascara).netmask_bits()
			numero_subredes=[]
			for x in range(1,num+1):
				numero_subredes.append(2**x)
			nsubredes = args.subredesrequeridas + 2 
			for idx, value in enumerate(numero_subredes):
				if value >= nsubredes:
					break
			if (idx + 1 == len(numero_subredes)):
				print "Error: Numero de subredes excede el espacio para subnetting."
				exit(1)
			nuevoCIDRred = miip.prefixlen + idx + 1
			subredes = list(miip.subnet(nuevoCIDRred))
			subnetNetwork(subredes, nuevoCIDRred)
		else:
			print "Error: (" + sys.argv[3] + ") requiere opcion para subnetting."
			parser.print_help()
			exit(1)
	if args.tocidr:
		print IPAddress(miip.ip).netmask_bits()		
if (__name__ == "__main__"):
	main()