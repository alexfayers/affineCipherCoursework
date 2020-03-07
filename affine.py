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

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:  # otherwise
        gcd, x, y = extended_gcd(b % a, a)

    return gcd, y - (b // a) * x, x


def inverse_mod(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def coprime_gen(n):  # find coprimes of a number 'n'
    if n < 0:  # don't check if number is too small
        return []
    else:
        coprimesTemp = []
        for toCheck in range(1, n, 2):  # don't check even numbers as they cant be coprime
            if math.gcd(toCheck, n) == 1:  # if current number is coprime with n
                coprimesTemp.append(toCheck)  # add number to returned array
        return coprimesTemp


####################################################
#
#   Inputs
#
####################################################


def get_inputs(keyspace, coprimes):

    # Ask user if they want to encrypt or decrypt, and validate the response
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

    # Ask the user to enter the first key and validate the response
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

    # Ask the user to enter the second key and validate the response
    getInput = True
    while getInput:
        b = input("Second key (b): ")

        try:
            b = int(b)

            if b not in coprimes:
                print("Please enter an integer that is coprime with " + str(len(keyspace)))
                print("E.g: " + str(coprimes))
            else:
                getInput = False
        except ValueError:
            print("Invalid number! Please enter an integer")

    # Ask the user to enter the message to encrypt/decrypt (no need to validate here as all
    # unrecognised characters are removed
    message = input("Message to "+str(encrypt_decrypt)+": ")
    message = message.upper()

    return a, b, encrypt_decrypt, message


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
    keyspace = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    coprimes = coprime_gen(len(keyspace))

    inputs = get_inputs(keyspace, coprimes)
    keys = inputs[:2]  # keys are first 2 numbers

    encrypt_decrypt = inputs[2]

    message = inputs[3]

    if keys[0] not in coprimes:
        raise ValueError("Error! "+str(keys[0]+" is not coprime with " + str(len(keyspace))))

    outmessage = encrypt_decrypt_string(message, keys[0], keys[1], keyspace, encrypt_decrypt)

    print("\nYour "+str(encrypt_decrypt)+"ed message is:")
    print(outmessage)

    input("Press enter to exit...")


main()
