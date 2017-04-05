# IPTools

Programa en Python para calculos con direcciones IP (subnetting).

### Funciones


1. Obtiene información de una IP. E.g. Su mascara por defecto, clase, privada o publica, loopback, etc.
2. Subnetea la IP a partir de mascara de subred personalizada.
3. Subnetea la IP a partir del número de hosts requeridos
4. Subnetea la IP a partir del número de subredes requeridas.
5. Convierte una máscara de red de notacion de "números y puntos" a CIDR.


### Usage

```
usage: iptools_v1.0.py [-h] --dir-ip DIRECCION_IP [--info] [--subnet]
                       [--cidr CIDR] [--nhost HOSTREQUERIDOS]
                       [--nsubredes SUBREDESREQUERIDAS] [--tocidr]
                       [--out ARCHIVO]

IPv4 Tools v1.0

optional arguments:
  -h, --help            show this help message and exit
  --info, -f            Muestra información sobre la IP
  --tocidr              Convierte una mascara de red de notacion de números y
                        puntos a CIDR
  --out ARCHIVO, -o ARCHIVO
                        Genera la salida en el archivo de texto indicado

REQUERIDO:
  --dir-ip DIRECCION_IP, -i DIRECCION_IP
                        IP en formato de numeros y puntos (numbers and dots)
                        e.g --dir-ip 1.1.1.1 Puedes indicar la mascara con
                        notacion CIDR e.g. -i 1.1.1.1/8

opciones para subnetting:
  --subnet, -s          Indica que se hará un subnetting de le IP dada. Si la
                        IP no tiene su prefijo CIDR (/24 ..) se aproximará de
                        acuerdo a su clase.
  --cidr CIDR, -c CIDR  Indica el nuevo prefijo (máscara personalizada) con
                        el que se hará el subnetting. Indicar en notacion
                        CIDR. E.g. --subnet --cidr 28 ó -s -c 28
  --nhost HOSTREQUERIDOS, -t HOSTREQUERIDOS
                        Display Help
  --nsubredes SUBREDESREQUERIDAS, -r SUBREDESREQUERIDAS
                        Display Help

```
### Algunos ejemplos

![imagen 1](https://github.com/todmephis/calculadora_ip_subnet/blob/master/caps/cap1.png)
![imagen 2](https://github.com/todmephis/calculadora_ip_subnet/blob/master/caps/cap2.png)
![imagen 3](https://github.com/todmephis/calculadora_ip_subnet/blob/master/caps/cap3.png)
![imagen 4](https://github.com/todmephis/calculadora_ip_subnet/blob/master/caps/cap4.png)
![imagen 5](https://github.com/todmephis/calculadora_ip_subnet/blob/master/caps/cap5.png)

### ¿Preguntas?

Puedes hacerme llegar cualquiér opinión o duda que tengas. Dejaré mi contacto :)

## Autor

**Iván Sánchez**

*Contacto*

[Twitter](https://twitter.com/todmephis) 
[Telegram](http://telegram.me/todmephis)
[Facebook](https://www.facebook.com/0xSCRIPTKIDDIE1)



## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details

by todmephis