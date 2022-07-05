import base64
import binascii
import textwrap
import time

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

    print(f"bin: {base64} ")

    return


def zaHashu(x):
    bits = toBits(x)
    seed = createSeed(bits)
    hashBits = bestHash(bits, seed)
    hash = toBase64(hashBits)
    return hash


def main():
    print(
        """
    1.Add a Student
    2.Delete a Student
    3.Look Up Student Record
    4.Exit/Quit
    """
    )
    x = input("Ingrese la operacion que desea Realizar: ")


if __name__ == "__main__":
    main()
