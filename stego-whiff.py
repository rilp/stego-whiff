import os
import argparse
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

PNG_HEADER = b'\x89PNG\r\n\x1a\n'
PNG_HEADER_LENGTH = len(PNG_HEADER)
IEND = b'IEND\xaeB\x60\x82'
IEND_LENGTH = len(IEND)

def print_and_exit(msg):
    print(msg)
    exit(1)

def hide_message(filename, pos_iend, secrect_msg):
    with open(filename,"r+b") as file:
        file.read(pos_iend + IEND_LENGTH)
        file.write(secrect_msg)
        file.truncate(pos_iend + IEND_LENGTH + len(secrect_msg))
        print('\nThe message has been hidden correctly in "{}"\n'.format(filename))
        print('{\__/}')
        print('( o_o)')
        print('( >  ) Want a taco?\n')

def find_message(filename, pos_iend):
    with open(filename,"rb") as file:
        file.read(pos_iend + IEND_LENGTH)
        msg = file.read().decode('UTF-8')
        return msg

def cypher_message(msg, password):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=PNG_HEADER+IEND,
        iterations=390000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(bytes(password,'UTF-8')))
    f = Fernet(key)
    secret_msg = f.encrypt(bytes(msg,'UTF-8'))
    return secret_msg

def uncypher_message(secret_msg, password):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=PNG_HEADER+IEND,
        iterations=390000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(bytes(password,'UTF-8')))
    f = Fernet(key)
    msg = f.decrypt(bytes(secret_msg,'UTF-8'))
    if msg:
        print("Jackpot!")
        print(msg.decode()+"\n")
    else:
        print("I couldn't find a hidden message. Try with LSB or maybe is just a PNG scam.")

def main():
    # Define and parse the input arguments
    parser = argparse.ArgumentParser(description="Hide or find a text message in a PNG file. In order to find the message it should be appended after the IEND PNG chunk. The same idea is to hide the message.")
    parserGroup = parser.add_mutually_exclusive_group()
    parserGroup.add_argument("-find",help="Find the hidden message",action="store_true")
    parserGroup.add_argument("-hide",help="Add a hidden message",metavar="Message")
    parser.add_argument("-passwd",help="Password used to code or decode the message",metavar="Password")
    parser.add_argument("file",help="a PNG file")
    args = parser.parse_args(['-find','-passwd','secure password','../cool.png'])

    # Check that at least one option (-find or -hide) is choosen
    if args.hide == None and args.find == False:
        print_and_exit('You need to choose at least one of the following options: -find or -hide')

    filename = args.file
    # Check whether the file exists
    if not os.path.isfile(filename):
        print_and_exit('File "{}" not found'.format(filename))

    with open(filename,"rb") as file:
        #Check whether file is a PNG
        if file.read(PNG_HEADER_LENGTH) != PNG_HEADER:
            print_and_exit('"{}" is not a PNG'.format(filename))
        str = PNG_HEADER + file.read()
        pos = str.find(b'IEND')
    
    if args.hide and args.passwd:
        msg = cypher_message(args.hide, args.passwd)
        hide_message(filename, pos, msg)
    elif args.hide:
        hide_message(filename, pos, bytes(args.hide,'UTF-8'))
    elif args.find and args.passwd:
        msg = find_message(filename,pos)
        uncypher_message(msg,args.passwd)
    elif args.find:
        find_message(filename,pos)

if __name__ == "__main__":
    main()

