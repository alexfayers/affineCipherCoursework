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
    encryptedMessage = input("Please enter the cipher-text to crack: ")
    # encryptedMessage = "PAJJYXPANA"  # HELLOTHERE (a=5, b=6)
    # "UYLCCZPFFWUYTGDHZ"  # PRETTYGOODPRIVACY (a=15, b=3)

    encryptedMessageLen = len(encryptedMessage)
    keyspace = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    coprimes = coprime_gen(len(keyspace))

    bestOverallKeys = [[]]
    bestOverallWords = ['']

    with open("1000.txt") as word_file:
        for a in coprimes:
            print("Checking an A value of " + str(a) + "...")

            for b in range(1, len(keyspace)-1):
                addedToWords = False
                decrypted = encrypt_decrypt_string(encryptedMessage, a, b, keyspace, 'decrypt')

                word_file.seek(0)
                for word in word_file:

                    word = word.upper().strip()

                    # these if's don't use 'and' statements to save on processing time
                    if len(word) >= len(bestOverallWords[0]):  # if current word is longer than the best
                        if word in decrypted:  # decrypted.startswith(word):
                            if len(word) > len(bestOverallWords[0]):
                                addedToWords = True
                                bestOverallWords = [word]
                                bestOverallKeys = [[a, b]]
                                print("Found longer word! New overall best length is " + str(len(word)))
                                print("(Word found: " + str(word) + ")")
                                print("(Decrypted text: "+str(decrypted)+")")

                            elif len(word) == len(bestOverallWords[0]):
                                addedToWords = True
                                bestOverallWords.append(word)
                                bestOverallKeys.append([a, b])

            if not addedToWords:
                print("No valid english words found with this A value.")

        print("Longest words overall are:")
        print(bestOverallWords)
        print("With keys:")
        print(bestOverallKeys)
        print()
        print("Therefore possible decrypted messages are:")

        for pair in range(len(bestOverallKeys)):
            print(encrypt_decrypt_string(encryptedMessage, bestOverallKeys[pair][0], bestOverallKeys[pair][1],
                                         keyspace, 'decrypt')
                  )
        input("Press enter to exit...")          

main()
