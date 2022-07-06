import hashlib
import re
import textwrap
import time
from math import log
from timeit import default_timer as timer
from typing import Callable

base64Alph = [
    'A',
    'B',
    'C',
    'D',
    'E',
    'F',
    'G',
    'H',
    'I',
    'J',
    'K',
    'L',
    'M',
    'N',
    'O',
    'P',
    'Q',
    'R',
    'S',
    'T',
    'U',
    'V',
    'W',
    'X',
    'Y',
    'Z',
    'a',
    'b',
    'c',
    'd',
    'e',
    'f',
    'g',
    'h',
    'i',
    'j',
    'k',
    'l',
    'm',
    'n',
    'o',
    'p',
    'q',
    'r',
    's',
    't',
    'u',
    'v',
    'w',
    'x',
    'y',
    'z',
    '0',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    '+',
    '/',
]


def measure_time(funcion: Callable) -> Callable:
    """Mide el tiempo de ejecucion

    Parameters
    ----------
    funcion : function
        funcion a la cual se le mide el tiempo
    Returns
    -------
    function: resultado de la funcion
    :Authors:
        - Javier Ramos
    """

    def measure_func(*args, **kwargs):
        inicio = timer()
        c = funcion(*args, **kwargs)
        print(
            '============================================================================'
        )
        print(f"\u2193 Tiempo de Ejecucion: {float(timer() - inicio)}")
        return c

    return measure_func


def toBits(bits: list) -> list:
    """Dada una lista de caracteres ASCII, Retorna su version en bits

    Parameters
    ----------
    list : list
        Lista de caracteres ASCII
    Returns
    -------
    list: lista de bits correspondiente a los caracteres ASCII
    :Authors:
        - Javier Ramos
    """
    bit_list = []
    arreglo_de_bytes = bytearray(bits, "utf8")
    for b in arreglo_de_bytes:
        bit_list.append(bin(b).split('b')[1])
    return bit_list


def createSeed(bitList: list) -> str:
    """Crea la semilla a usar en za Hash, usando el tiempo
            y el primer elemento de la lista que recibe.

    Parameters
    ----------
    bitList : list
        Binarios de 7 bits que representan characteres en ASCII.
    Returns
    -------
    str: Retorna la semilla inicial de largo 56 bits.
    :Authors:
        - Javier Ramos
    """
    timeseed = int(time.time() / 100)
    seedbits = bin(timeseed).split('b')[1]
    seed = seedbits + bitList[0] + seedbits + "0"
    return seed


def xor(base: str, key: str) -> str:
    """calcula el XOR entre 2 streams de bits

    Parameters
    ----------
    base : str
        steam de bit al cual se le aplica el XOR
    key : str
        llave para aplicar el XOR
    Returns
    -------
    str: Retorna un string del XOR resultante
    :Authors:
        - Javier Ramos
    """
    xorList = [(ord(a) ^ ord(b)) for a, b in zip(base, key)]
    return "".join(map(str, xorList))


def bestHash(bitList: list, seed: str) -> str:
    """Calcula el hash de una lista de bits dada,
            asegurandose que el resultado sea de 330 bits.

    Parameters
    ----------
    bitList : list
        bloques binarios de los caracteres del string a hashear
    seed : str
        la semilla en binario
    Returns
    -------
    str: retorna un string de 330 caracteres en binario
    :Authors:
        - Javier Ramos
    """
    hashedBits = ""
    count = 0
    seedSplit = textwrap.wrap(seed, 7)
    for char in bitList:
        a = xor(char, seedSplit[count])
        hashedBits += a + char
        count = count + 1 if count < 7 else 0
    lenght = len(hashedBits)
    if lenght < 330:
        hashedList = textwrap.wrap(hashedBits, 7)
        hashedList = list(
            map(
                lambda x: (x + x[0] * (7 - len(x))) if len(x) < 7 else x,
                hashedList,
            )
        )
        return bestHash(
            hashedList,
            xor(hashedBits, seed),
        )

    else:
        # print(f" {hashedBits} seed: {seed} len: {len(hashedBits)}")
        return splitBits(hashedBits)


def splitBits(bits: str) -> str:
    """recibe un binario de mas de 330 bits de largo y
        retorna el resultado de un xor entre 2 mitades del
        binario recibido. finalBits es de 330 bits exactos.

    Parameters
    ----------
    bits : str
       string binario de largo mayor a 330.
    Returns
    -------
    str: string binario de largo 330 bits.
    :Authors:
        - Javier Ramos
    """
    firstBits = bits[:330]
    lastBits = bits[-330:]
    finalBits = xor(firstBits, lastBits)
    return finalBits


def toBase64(hashedBits: str) -> str:
    """recibe una cadena de bits y los transforma a base64,
        utiliza como apoyo la lista base64Alph.
        Por implementacion no se agregan = si faltan bloques

    Parameters
    ----------
    hashedBits : str
        cadena binaria resultante de bestHash
    Returns
    -------
    str: retorna un string en base64
    :Authors:
        - Javier Ramos
    """
    hashSplit = textwrap.wrap(hashedBits, 6)
    base64 = ""
    for i in hashSplit:
        bin_int = int(i, 2)
        base64 += base64Alph[bin_int]
    return base64


@measure_time
def zaHashu(x: str) -> str:
    """Se encarga de llamar las funciones necesarias para
        obtener un hash "za hash"

    Parameters
    ----------
    x : str
        string a hashear
    Returns
    -------
    str: string hasheado en za hash
    :Authors:
        - Javier Ramos
    """
    bits = toBits(x)
    seed = createSeed(bits)
    hashBits = bestHash(bits, seed)
    hash = toBase64(hashBits)
    return hash


@measure_time
def md5(word: str) -> str:
    """calcula el hash md5 de un string dado

    Parameters
    ----------
    word : str
        string a hashear
    Returns
    -------
    str: string hasheado en md5
    :Authors:
        - Javier Ramos
    """
    hash = hashlib.md5(word.encode())
    return hash.hexdigest()


@measure_time
def sha256(word: str) -> str:
    """calcula el hash sha256 de un string dado

    Parameters
    ----------
    word : str
        string a hashear
    Returns
    -------
    str: string hasheado en sha256
    :Authors:
        - Javier Ramos
    """
    hash = hashlib.sha256(word.encode())
    return hash.hexdigest()


@measure_time
def sha1(word: str) -> str:
    """Calcula el hash sha1 de un string dado

    Parameters
    ----------
    word : str
        string a hashear
    Returns
    -------
    str: string hasheado en sha1
    :Authors:
        - Javier Ramos
    """
    hash = hashlib.sha1(word.encode())
    return hash.hexdigest()


def getBase(word: str) -> int:
    """dado un string, calcula la base en la que esta.
        (se considero solo los caracteres ASCII imprimibles hasta el 125)

    Parameters
    ----------
    word : str
        string en alguna base
    Returns
    -------
    int: entero que representa la base
    :Authors:
        - Javier Ramos
    """
    base = 0
    baseAscii = re.compile(r"[\x21-\x2f]|[\x3a-\x40]|[\x5b-\x60]|[\x7b-\x7e]")
    if re.search("[a-z]", word):
        base += 26
    if re.search("[A-Z]", word):
        base += 26
    if re.search("[0-9]", word):
        base += 10
    if baseAscii.search(word):
        base += 32
    return base


def entropy(word: str) -> float:
    """Dado un string, se encarga de calcular su base y el largo,
        para luego determinar la entropia del texto ingresado

    Parameters
    ----------
    word : str
        string al cual se le calculara la entropia (clave)
    Returns
    -------
    float: numero de bits de entropia.
    :Authors:
        - Javier Ramos
    """
    base = getBase(word)
    Llargo = len(word)
    Wbase = base
    Hentropia = Llargo * log(Wbase, 2)
    return Hentropia


def calculateEntropy(word: str):
    if word:
        option = input(
            f'Se detecto que hasheo --> {word}, desea utilizarla? (Y/N)'
        )
        while True:
            if option == 'Y':
                print(
                    """============================================================================
                    Calculando Entropia\n============================================================================"""
                )
                entropia = entropy(word)
                print(f"La entropia del hash es: {entropia}")
                break
            elif option == 'N':
                calculo = input(
                    """Porfavor Ingresa la palabra a la cual le deseas
                    calcular la entropia: """
                )
                print(
                    """============================================================================
                    Calculando Entropia\n ============================================================================"""
                )
                entropia = entropy(calculo)
                print(f"La entropia del hash es: {entropia}")
                break
    else:
        calculo = input(
            """Porfavor Ingresa la palabra a la cual le deseas calcular la entropia: """
        )
        print(
            """============================================================================\n
            Calculando Entropia\n============================================================================"""
        )
        entropia = entropy(calculo)
        print(f"La entropia de la clave es: {entropia}")
    return


def main():
    hash = ""
    word = ""
    pruebas = {'1': 1, '2': 10, '3': 20, '4': 50}
    while True:
        print(
            """============================================================================\n
        1.Calcular Hash de Una palabra.
        2.Calcular Hash desde archivo propio.
        3.Calcular Hash desde archivo rockyou.txt
        4.Calcular Entropia Za Hashu.
        5.Comparar Entropia y Ejecucion (MD5/SHA1/SHA256).
        9.Salir\n\n============================================================================"""
        )
        x = input("Ingrese la operacion que desea Realizar: ")

        if x == '1':
            word = input("Ingrese la palabra que desea hashear: ")
            hash = zaHashu(word)
            print(
                '============================================================================'
            )
            print(f"El hash de --> {word} es: {hash}")
            print(
                '============================================================================'
            )

        elif x == '2':
            name = input("Por favor ingresa el nombre del archivo a leer: ")
            with open(name) as file:
                lines = file.readlines()
                for i in lines:
                    line = i.strip()
                    hash = zaHashu(line)
                    print(
                        f"============================================================================\n{line}\nHash:"
                        f" {hash}\n============================================================================"
                    )
            file.close()

        elif x == '3':
            print(
                '============================================================================'
            )
            test = input(
                """
            Prueba 1: 1 entrada de texto.
            Prueba 2: 10 entrada de texto.
            Prueba 3: 20 entrada de texto.
            Prueba 4: 50 entrada de texto.

============================================================================
Que prueba desea realizar? (Ingrese Numero de la Prueba):"""
            )
            print("Leyendo archivo rockyou.txt")
            if test in pruebas.keys():
                print('owo')
                with open('rockyou.txt') as file:
                    for i in range(pruebas[test]):
                        line = file.readline()
                        hash = zaHashu(line)
                        print(
                            f"""============================================================================ 
    Palabra {i+1}: {line} 
    Hash: {hash}"""
                        )
                file.close()
            else:
                print('unu')

        elif x == '4':
            if word:
                calculateEntropy(word)
            else:
                calculateEntropy(word)

        elif x == '5':
            if word:
                option = input(
                    f'Se detecto que hasheo --> {word}, desea utilizarla?'
                    ' (Y/N)'
                )
                while True:
                    if option == 'Y':
                        print(
                            """============================================================================
                            Calculando Tiempo de Ejecucion\n============================================================================"""
                        )
                        entropia = entropy(word)
                        print(f"La entropia de {word} es: {entropia}")
                        myhash = zaHashu(word)
                        print(f"el hash generado por za hash es: {myhash}")
                        hashmd5 = md5(word)
                        print(f"el hash generado por md5 es: {hashmd5}")
                        hashsha1 = sha1(word)
                        print(f"el hash generado por sha1 es: {hashsha1}")
                        hashsha256 = sha256(word)
                        print(f"el hash generado por sha256 es: {hashsha256}")
                        break
                    elif option == 'N':
                        word = input(
                            """Porfavor Ingresa la palabra con la que deseas realizar la comparacion: """
                        )
                        print(
                            """============================================================================
                            Calculando Tiempo de Ejecucion\n============================================================================"""
                        )
                        entropia = entropy(word)
                        print(f"La entropia de {word} es: {entropia}")
                        myhash = zaHashu(word)
                        print(f"el hash generado por za hash es: {myhash}")
                        hashmd5 = md5(word)
                        print(f"el hash generado por md5 es: {hashmd5}")
                        hashsha1 = sha1(word)
                        print(f"el hash generado por sha1 es: {hashsha1}")
                        hashsha256 = sha256(word)
                        print(f"el hash generado por sha256 es: {hashsha256}")
                        break
            else:
                word = input(
                    """Porfavor Ingresa la palabra con la que deseas realizar la comparacion: """
                )
                print(
                    """============================================================================
                    Calculando Tiempo de Ejecucion\n============================================================================"""
                )
                entropia = entropy(word)
                print(f"La entropia de {word} es: {entropia}")
                myhash = zaHashu(word)
                print(f"el hash generado por za hash es: {myhash}")
                hashmd5 = md5(word)
                print(f"el hash generado por md5 es: {hashmd5}")
                hashsha1 = sha1(word)
                print(f"el hash generado por sha1 es: {hashsha1}")
                hashsha256 = sha256(word)
                print(f"el hash generado por sha256 es: {hashsha256}")

        elif x == '9':
            print("Adios")
            break
        else:
            print("Por favor ingresa una opcion valida")
            continue

    return


if __name__ == "__main__":
    main()
