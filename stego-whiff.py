import os
import argparse

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
        msg = bytes(secrect_msg,'UTF-8')
        file.write(msg)
        file.truncate(pos_iend + IEND_LENGTH + len(msg))
        print('\nThe message has been hidden correctly in "{}"\n'.format(filename))
        print('{\__/}')
        print('( o_o)')
        print('( >  ) Want a taco?\n')

def find_message(filename, pos_iend):
    with open(filename,"rb") as file:
        file.read(pos_iend + IEND_LENGTH)
        msg = file.read().decode('UTF-8')
        if msg:
            print("Jackpot!")
            print(msg+"\n")
        else:
            print("I couldn't find a hidden message. Try with LSB or maybe is just a PNG scam.")

def main():
    # Define and parse the input arguments
    parser = argparse.ArgumentParser(description="Hide or find a text message in a PNG file. In order to find the message it should be appended after the IEND PNG chunk. The same idea is to hide the message.")
    parserGroup = parser.add_mutually_exclusive_group()
    parserGroup.add_argument("-find",help="Find the hidden message",action="store_true")
    parserGroup.add_argument("-hide",help="Add a hidden message",metavar="Message")
    parser.add_argument("file",help="a PNG file")
    args = parser.parse_args()

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
    
    if args.hide:
        hide_message(filename, pos, args.hide)
    elif args.find:
        find_message(filename,pos)

if __name__ == "__main__":
    main()

