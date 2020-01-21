import math

def coprime(a,b): # check if a and b are coprime using math module
	return math.gcd(a,b) == 1

def coprimeGen(n): # find coprimes of a number 'n'

	# validate n is number

	if n < 0: # don't check if number is too small
		return []
	else:
		coprimesTemp = []
		for toCheck in range(1,n,2): # don't check even numbers
			if coprime(toCheck,n):
				coprimesTemp.append(toCheck)
		return coprimesTemp

def getInputs():
	a = 5 #int(input("Enter a: "))
	b = 8 #int(input("Enter b: "))

	return (a,b)

def encryptSingle(plainChar, a, b, keyspace, encrypt): # str, int, int, str, bool
	try:
		x = keyspace.index(plainChar)
	except:
		print("Encountered invalid char! '"+str(x)+"'")
		return '!'
	# ensure char is lowercase
	
	if encrypt:	
		encryptedX = (a*x + b) % len(keyspace)
	else:
		encryptedX = (a*x - b) % len(keyspace)
	
	encryptedChar = keyspace[encryptedX]	

	# make encrypted char uppercase?

	return encryptedChar

def encryptString(plainText, a, b, keyspace, encrypt):
	encryptedText = ""
	
	for character in plainText:
		encryptedText += encryptSingle(character, a, b, keyspace,encrypt)
	
	return encryptedText

def main():
	keyspace = "abcdefghijklmnopqrstuvwxyz"

	coprimes = coprimeGen(len(keyspace))
	
	inputs = getInputs()

	e = encryptString('affine', inputs[0], inputs[1], keyspace, True)
	
	print(e)

main()