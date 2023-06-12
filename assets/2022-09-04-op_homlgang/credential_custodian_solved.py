#!/usr/bin/env python3

'''
2010-05-04: Here is the password manager you wanted; Start using it TODDAY!
2010-05-03: Implemented OWN generate_password function. Probably secure.
2010-05-02: Started development. Stole most of the code from hackexchange.
'''

import sys
import string
import random
import time
import base64

def generate_password(t, length=50):
    '''Return an UNPREDICTALBE password of given length'''

    random.seed(t)
    characters =  string.digits + string.ascii_letters
    password = ''

    for i in range(length):
        offset = random.randrange(0, len(characters))
        password += characters[offset]

    return password

def xor(secret, key):
    '''Encrypt or decrypt secret blob using XOR cipher'''

    return bytes([a ^ b for a, b in zip(secret, key)])

def show_secret(password):
    '''Decrypt base64 encoded secret from the bottom of this file'''

    secret = ''
    with open(sys.argv[0], 'r', encoding='utf8') as file:
        secret = file.readlines()[-1]

    secret = base64.b64decode(secret[1:])
    secret = xor(secret, password)
    return secret.decode()

def save_secret(password, secret):
    '''Encrypt and store base64 encoded secret in this file with # prefix'''

    secret = xor(secret, password)
    secret = base64.b64encode(secret)
    secret = '#' + str(secret.decode()) + '\n'

    all_content = ''
    with open(sys.argv[0], 'r', encoding='utf8') as file:
        all_content = file.readlines()

    all_content[-1] = secret

    with open(sys.argv[0], 'w', encoding='utf8') as file:
        file.writelines(all_content)

def usage():
    '''Print script usage and exit'''

    sys.exit(f'Usage: {sys.argv[0]} COMMAND [password] [secret]\
\n\tgenerate : creates password\
\n\tshow [password]: prints secret\
\n\tsave [password] [secret]: stores secret\
    ')

def main():
    '''Entry point. Handles script arguments and calls relevant function'''

    if len(sys.argv) < 2 or len(sys.argv) > 4:
        usage()

    if sys.argv[1] == 'generate':
        for t in range(1272848461,1273104061):
        	message = show_secret(generate_password(t).encode())
        	if message.isprintable():
        		print(message)
        		if len(message.split()) > 5:
        			likely = message
        print(likely)

    if sys.argv[1] == 'show':
        if len(sys.argv) == 3:
            password = sys.argv[2].encode()
            print(show_secret(password))
        else:
            usage()

    if sys.argv[1] == 'save':
        if len(sys.argv) == 4:
            password = sys.argv[2].encode()
            secret = sys.argv[3].encode()
            save_secret(password, secret)
        else:
            usage()


if __name__ == '__main__':
    main()


#OTskUhcDAWQuBy50AQgJExRVHh1uFgomAm4VEwoQLDAfFkQSHxkDB1AKcAYIAmM9MBw=
