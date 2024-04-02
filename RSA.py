import random

#function to pick prime number
def pick_prime():
    prime = False
    while prime == False:
        n = random.randint(3, 100000)
        if n % 2 == 0:
            n += 1

        prime = miller_rabin(n, k = 5)

    return n

#primality test function (rand odd int n and k rounds)
def miller_rabin(n, k):
    
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