import hashlib
import re
import textwrap
import time
from math import log
from timeit import default_timer as timer
from weakref import WeakKeyDictionary

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


def mide_tiempo(funcion):
    def funcion_medida(*args, **kwargs):
        inicio = timer()
        c = funcion(*args, **kwargs)
        print(
            '============================================================================'
        )
        print(f"\u2193 Tiempo de Ejecucion: {float(timer() - inicio)}")
        return c

    return funcion_medida


def toBits(bits: list) -> list:
    """Funcion que dado una lista de caracteres ASCII, Retorna su version en bits

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
    timeseed = int(time.time() / 100)
    seedbits = bin(timeseed).split('b')[1]
    seed = seedbits + bitList[0] + seedbits + "0"
    return seed


def xor(base: str, key: str):
    xorList = [(ord(a) ^ ord(b)) for a, b in zip(base, key)]
    return "".join(map(str, xorList))


def bestHash(bitList: list, seed: str) -> str:
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


def splitBits(bits: str):
    firstBits = bits[:330]
    lastBits = bits[-330:]
    finalBits = xor(firstBits, lastBits)
    return finalBits


def toBase64(hashedBits: str) -> str:
    hashSplit = textwrap.wrap(hashedBits, 6)
    base64 = ""
    for i in hashSplit:
        bin_int = int(i, 2)
        base64 += base64Alph[bin_int]
    return base64


@mide_tiempo
def zaHashu(x: str):
    bits = toBits(x)
    seed = createSeed(bits)
    hashBits = bestHash(bits, seed)
    hash = toBase64(hashBits)
    return hash


@mide_tiempo
def md5(word: str):
    hash = hashlib.md5(word.encode())
    return hash.hexdigest()


@mide_tiempo
def sha256(word: str):
    hash = hashlib.sha256(word.encode())
    return hash.hexdigest()


@mide_tiempo
def sha1(word: str):
    hash = hashlib.sha1(word.encode())
    return hash.hexdigest()


def getBase(word: str):
    base = 0
    baseAscii = re.compile("[\x21-\x2f]|[\x3a-\x40]|[\x5b-\x60]|[\x7b-\x7e]")
    if re.search("[a-z]", word):
        base += 26
    if re.search("[A-Z]", word):
        base += 26
    if re.search("[0-9]", word):
        base += 10
    if baseAscii.search(word):
        base += 32
    return base


def entropy(word: str):
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
