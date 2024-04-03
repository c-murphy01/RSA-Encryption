#to generate random numbers to find primes
import random

#function to pick prime number
def pick_prime():
    #initialise
    prime = False
    #loop until prime is found
    while prime == False:
        num = random.randint(3, 1000)
        #ensure number is odd
        if num % 2 == 0:
            num += 1

        #check for primality, 5 rounds by default
        prime = miller_rabin(num, k = 5)

    #return prime number when found
    return num

#primality test function (rand odd int n and k rounds)
def miller_rabin(n, k):
    
    #handle case of n = 3
    if n == 3:
        return True
    
    #need to find n-1 in the form (2^s) * d, where s is a positive integer and d is an odd positive integer
    s, d = 0, n - 1 #set initial values
    #divide d by 2 (floor division) until it is odd and count iterations with s
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(k): #even if n seems to be prime with a certain base a, we need to check others to be sure
        a = random.randint(2, n-2)
        #initial test for primality
        x = mod_exp(a, d, n)  #compute a^d % n
        if x == 1 or x == n - 1: #if either of these is true, n passes the base test and might be prime
            continue
            #
        for _ in range(s - 1):
            x = mod_exp(x, 2, n)  #square x and mod n
            if x == n - 1:
                break  #n passes; high probability of being prime
        
        else: #n fails the test; it is composite
            return False
    
    return True

#function to calculate base^exp % mod
def mod_exp(base, exp, mod):
    #set result to 1
    result = 1
    #modulo base to make sure all operations are done within the modular space of mod
    base = base % mod
    #keep looping until exp becomes zero
    while exp > 0:
        #check if current exponent is odd
        if exp % 2 == 1:
            #if so, multiply current result by base and modulo to keep result in modular space (multiply part of square and multiply)
            result = (result * base) % mod
        #right shift by 1 (divide by 2 and round down)
        exp = exp >> 1
        #square and modulo (square part of square and multiply)
        base = (base * base) % mod
    return result

#fucntion to choose a suitable value e
def choose_e(phi):
    #find a number that fits gcd(φ(n), e) = 1; 1 < e < φ(n)
    for i in range(2, phi):
        if gcd(i, phi) == 1:
            return i
    
    return None

#function to find greatest common denominator of two numbers
def gcd(a, b):
    #loop until b = 0
    while b != 0:
        #each iteration decrease the size of each number until a modulo 0 is left, then return a
        temp = b
        b = a % b
        a = temp
        
    return a

#extended greatest common denominator to find that and the bezout coefficients, such that ax+by=gcd(a,b)
def extended_gcd(a, b):
    if a == 0: #base case if a = 0
        return b, 0, 1
    
    #otherwise recursively call the function to get smaller values
    gcd, x1, y1 = extended_gcd(b % a, a)
    
    #calculate the bezout coefficients
    x = y1 - (b // a) * x1
    y = x1

    return gcd, x, y

#calculate the modular inverse of a number, e, w.r.t. another number, phi_n
def mod_inv(e, phi_n):
    g, x, y = extended_gcd(e, phi_n)
    if g != 1:
        print('Modular inverse does not exist!')
    else:
        #return the modular inverse
        return x % phi_n 

#generate the private and public encryption keys
def generate_keys():
    #generate two prime numbers that are not equal
    p = pick_prime()
    q = p
    while q == p:
        q = pick_prime()

    #calculate n and φ(n)
    n = p*q
    phi = (p-1)*(q-1)

    #choose a suitable e so that 1 < e < φ(n), and gcd(φ(n), e) = 1;
    e = choose_e(phi)

    #calculate d, where d ≡ e^−1 (mod φ(n))
    d = mod_inv(e, phi)

    #generate keys
    PR = {'d': d, 'n': n}  #private
    PU = {'e': e, 'n': n}  #public

    return PR, PU

#encrypt message
def encrypt(message, public_key):
    #extract exponent, e, and modulus, n from key
    e, n = public_key['e'], public_key['n']
    #encrypt the message using modular exponentiation
    cipher = mod_exp(message, e, n)
    return cipher

#decrypt cipher
def decrypt(cipher, private_key):
    #extract the exponent, d, and the modulus, n, from key
    d, n = private_key['d'], private_key['n']
    #decrypt the message using modular exponentiation
    message = mod_exp(cipher, d, n)
    return message