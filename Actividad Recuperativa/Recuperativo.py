def toBits(bits: str) -> str:
    """transforma un str ascii en bits

    Parameters
    ----------
    bits : str
        string ascii a transformar a bits
    Returns
    -------
    str: string de bits que representan al string original
    :Authors:
        - Javier Ramos
    """
    bin_bits = bin(int.from_bytes(bits.encode(), 'big'))
    return bin_bits


def toAscii(bits: str) -> str:
    """transforma un str de bits en ascii

    Parameters
    ----------
    bits : str
        str en bits a transformar en ascii
    Returns
    -------
    str: string en ascii que corresponde al str original
    :Authors:
        - Javier Ramos
    """
    ascii_bits = int(bits, 2)
    ascii_text = ascii_bits.to_bytes(
        (ascii_bits.bit_length() + 7) // 8, 'big'
    ).decode()
    return ascii_text


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


def main():
    while True:
        text = input("Ingrese el texto a cifrar: ")
        key = input("Ingrese el texto que sera la llave: ")
        bits_text = "".join(toBits(text))
        bits_text = bits_text.split('b')[1]
        bits_key = "".join(toBits(key))
        bits_key = bits_key.split('b')[1]
        hash = xor(bits_text, bits_key)
        ascii_hashed = toAscii(hash)
        print(
            f"El resultado en ascii es: {ascii_hashed} mientras que en bits"
            f" es: {hash}"
        )
        choice = input("Deseas descifrar el texto?:(Y/N) ")
        if choice == 'Y':
            dehash = xor(hash, bits_key)
            ascii_dehashed = toAscii(dehash)
            print(f"El texto original era: {ascii_dehashed}")
            break
        else:
            continue


if __name__ == "__main__":
    main()
