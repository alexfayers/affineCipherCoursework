import math


####################################################
#
#   Math stuff
#
####################################################


def inverse_mod(a, maxNo):  # find inverse modulo of a number
    for b in range(1, maxNo, 2):  # don't process even numbers
        if ((a * b) % maxNo) == 1:
            return b
    raise ValueError(str(a)+" has no inverse mod"+str(maxNo))


def coprime(a, b):  # check if a and b are coprime using math module
    return math.gcd(a, b) == 1


def coprime_gen(n):  # find coprimes of a number 'n'
    if n < 0:  # don't check if number is too small
        return []
    else:
        coprimesTemp = []
        for toCheck in range(1, n, 2):  # don't check even numbers
            if coprime(toCheck, n):
                coprimesTemp.append(toCheck)
        return coprimesTemp


####################################################
#
#   Input stuff
#
####################################################


def get_inputs(keyspace, coprimes):
    getInput = True
    while getInput:
        print("Encrypt (e) or decrypt (d)?")
        encrypt_decrypt = input("Option: ")

        if encrypt_decrypt.lower() == 'e':
            encrypt_decrypt = 'encrypt'
            getInput = False

        elif encrypt_decrypt.lower() == 'd':
            encrypt_decrypt = 'decrypt'
            getInput = False

        else:
            print("'"+str(encrypt_decrypt)+"' is an invalid option!")

    getInput = True
    while getInput:
        a = input("First key (a) (must be coprime with "+str(len(keyspace))+"): ")

        try:
            a = int(a)

            if a not in coprimes:
                print("Please enter an integer that is coprime with " + str(len(keyspace)))
                print("E.g: " + str(coprimes))
            else:
                getInput = False
        except ValueError:
            print("Invalid number! Please enter an integer")

    getInput = True
    while getInput:
        b = input("Second key (b): ")

        try:
            b = int(b)
            getInput = False
        except ValueError:
            print("Invalid number! Please enter an integer")

    message = input("Message to "+str(encrypt_decrypt)+": ")

    return a, b, encrypt_decrypt, message


####################################################
#
#   Encryption and decryption stuff
#
####################################################


def encrypt_decrypt_single(inputChar, a, b, keyspace, encrypt):  # str, int, int, str, str
    if inputChar == ' ':  # check for spaces
        return ' '

    try:
        x = keyspace.index(inputChar)
    except ValueError:  # if current char is unrecognised, remove it (as per spec)
        return ''

    # ensure char is lowercase

    if encrypt == 'encrypt':
        output_x = (a * x + b) % len(keyspace)

    elif encrypt == 'decrypt':
        inverse_a = inverse_mod(a, len(keyspace))
        output_x = (inverse_a * (x - b)) % len(keyspace)

    else:
        raise SyntaxError("Error in encrypt/decrypt variable. Check spelling?")

    outputChar = keyspace[output_x]

    # make encrypted char uppercase?

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
    keyspace = "abcdefghijklmnopqrstuvwxyz"

    coprimes = coprime_gen(len(keyspace))

    inputs = get_inputs(keyspace,coprimes)
    keys = inputs[:2]  # keys are first 2 numbers

    encrypt_decrypt = inputs[2]

    message = inputs[3]

    if keys[0] not in coprimes:
        raise ValueError("Error! "+str(keys[0]+" is not coprime with " + str(len(keyspace))))

    print(
        encrypt_decrypt_string(message, keys[0], keys[1], keyspace, encrypt_decrypt)
    )


main()