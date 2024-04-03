from RSA import generate_keys, encrypt, decrypt, sign, check_sign

#generate keys
private, public = generate_keys()

#plaintext message, must be smaller than n
message = 123
#encrpt the message
cipher = encrypt(message, public)

#decrypt the ciphertext
plaintext = decrypt(cipher, private)

#check that the decrypted message matches the original
assert plaintext == message, "Decryption failed!"

print("Encryption and Decryption were successful!")

#generate new keys
private, public = generate_keys()

message = 321

#sign the message with the private key
signature = sign(message, private)

#check the signature with the public key
verified_message = check_sign(signature, public)

#check that the verified message matches the original
assert verified_message == message, "Signature verification failed!"

print("Signature and Verification successful!")