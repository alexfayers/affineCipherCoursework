####################################################
#
#   Imports
#
####################################################


import math


####################################################
#
#   Math
#
####################################################


def inverse_mod(a, maxNo):  # find inverse modulo of a number
    for b in range(1, maxNo, 2):  # don't process even numbers as they cant be coprime
        if ((a * b) % maxNo) == 1:
            return b
    raise ValueError(str(a)+" has no inverse mod "+str(maxNo))


def coprime(a, b):  # check if a and b are coprime using math module
    return math.gcd(a, b) == 1


def coprime_gen(n):  # find coprimes of a number 'n'
    if n < 0:  # don't check if number is too small
        return []
    else:
        coprimesTemp = []
        for toCheck in range(1, n, 2):  # don't check even numbers as they cant be coprime
            if coprime(toCheck, n):  # if current number is coprime with n
                coprimesTemp.append(toCheck)  # add number to returned array
        return coprimesTemp


####################################################
#
#   Encryption and decryption
#
####################################################


def encrypt_decrypt_single(inputChar, a, b, keyspace, encrypt):  # str, int, int, str, str
    if inputChar == ' ':  # check for spaces and leave them in the message
        return ' '

    try:
        x = keyspace.index(inputChar)  # convert char to corresponding number
    except ValueError:  # if current char is unrecognised (not in keyspace), remove it (as per spec)
        return ''

    if encrypt == 'encrypt':
        output_x = (a * x + b) % len(keyspace)  # actual encryption algorithm

    elif encrypt == 'decrypt':
        inverse_a = inverse_mod(a, len(keyspace))
        output_x = (inverse_a * (x - b)) % len(keyspace)  # actual decryption algorithm

    else:
        raise SyntaxError("Error in encrypt/decrypt variable. Check spelling?")

    outputChar = keyspace[output_x]
    return outputChar


def encrypt_decrypt_string(plainText, a, b, keyspace, encrypt):
    encryptedText = ""

    for character in plainText:
        encryptedText += encrypt_decrypt_single(character, a, b, keyspace, encrypt)

    return encryptedText


####################################################
#
#   Main
#
####################################################


def main():
    encryptedMessage = "UYLCCZPFFWUYTGDHZ"
    encryptedMessage = "PAJJYXPANA"  # HELLOTHERE (a=5,b=6)
    encryptedMessageLen = len(encryptedMessage)
    keyspace = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    coprimes = coprime_gen(len(keyspace))

    with open("englishwords.txt") as word_file:
        for a in coprimes:
            print("next a", a)
            for b in range(1, len(keyspace) - 2):

                decrypted = encrypt_decrypt_string(encryptedMessage, a, b, keyspace, 'decrypt')

                word_file.seek(0)
                for word in word_file:
                    word = word.upper().strip()
                    if word in decrypted and len(word) >= 3:
                        print(word, "found in ", decrypted)




main()

