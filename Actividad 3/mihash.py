import hashlib
import textwrap
import time
from math import log

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
        inicio = time.time()
        c = funcion(*args, **kwargs)
        print(time.time() - inicio)
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


def entropy(word: str):
    L = len(word)
    W = 64
    H = L * log(W, 2)
    return H


def calculateEntropy(word: str):
    if word:
        option = input(
            f'Se detecto que hasheo --> {word}, desea utilizarla? (Y/N)'
        )
        while True:
            if option == 'Y':
                print(
                    """======================================================
                                    Calculando Entropia
                    ======================================================"""
                )
                entropia = entropy(word)
                print(f"La entropia del hash es: {entropia}")
                break
            if option == 'N':
                calculo = input(
                    """Porfavor Ingresa la palabra a la cual le deseas
                    calcular la entropia: """
                )
                print(
                    """======================================================
                                Calculando Entropia
                    ======================================================"""
                )
                entropia = entropy(calculo)
                print(f"La entropia del hash es: {entropia}")
                break
    else:
        calculo = input(
            """Porfavor Ingresa la palabra a la cual le deseas calcular la entropia: """
        )
        print(
            """======================================================
                            Calculando Entropia
            ======================================================"""
        )
        entropia = entropy(calculo)
        print(f"La entropia del hash es: {entropia}")
    return


def main():
    hash = ""
    word = ""
    while True:
        print(
            """
        1.Calcular Hash de Una palabra.
        2.Calcular Hash desde el archivo rockyou.txt
        3.Calcular Hash desde un archivo propio.
        4.Calcular Entropia Za Hashu.
        5.Comparar Entropia.
        9.Salir
        """
        )
        x = input("Ingrese la operacion que desea Realizar: ")

        if x == '1':
            word = input("Ingrese la palabra que desea hashear: ")
            hash = zaHashu(word)
            print(f"El hash de --> {word} <-- es: {hash}")

        if x == '2':
            print("Leyendo archivo rockyou.txt")
            test = input(
                """
                    Prueba 1: 1 entrada de texto.
                    Prueba 2: 10 entrada de texto.
                    Prueba 3: 20 entrada de texto.
                    Prueba 4: 50 entrada de texto.
            Que prueba desea realizar? (Ingrese Numero de la Prueba):   """
            )
            with open('rockyou.txt') as file:
                for i in range():
                    line = file.readline()

        if x == '3':
            print("Por favor ingresa el nombre del archivo a leer")

        if x == '4':
            if word:
                calculateEntropy(word)
            else:
                calculateEntropy(word)

        if x == '5':
            print("comparando")

        if x == '9':
            print("Adios")
            break
        else:
            print("Por favor ingresa una opcion valida")
            continue

    return


if __name__ == "__main__":
    main()
