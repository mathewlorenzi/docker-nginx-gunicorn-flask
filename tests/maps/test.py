# https://stackoverflow.com/questions/49103709/how-to-use-shared-memory-in-python-and-c-c

import mmap
import os
import time

def test_org():
    fname = './pods.txt'
    if not os.path.isfile(fname):
        # create initial file
        with open(fname, "w+b") as fd:
            fd.write(b'\x01\x00\x00\x00\x00\x00\x00\x00')

    # at this point, file exists, so memory map it
    with open(fname, "r+b") as fd:
        mm = mmap.mmap(fd.fileno(), 8, access=mmap.ACCESS_WRITE, offset=0)

        # set one of the pods to true (== 0x01) all the rest to false
        posn = 0
        while True:
            print(f'writing posn:{posn}')

            # reset to the start of the file
            mm.seek(0)

            # write the true/false values, only one is true
            for count in range(8):
                curr = b'\x01' if count == posn else b'\x00'
                mm.write(curr)

            # admire the view
            time.sleep(2)

            # set up for the next position in the next loop
            posn = (posn + 1) % 8

        mm.close()
        fd.close()

def test_timestamp(): # hr min sec ms
    fname = './pods.txt'
    if not os.path.isfile(fname):
        # create initial file
        with open(fname, "w+b") as fd:

            fd.write(b'\x01\x00\x00\x00\x00\x00\x00\x00')

    # at this point, file exists, so memory map it
    with open(fname, "r+b") as fd:
        mm = mmap.mmap(fd.fileno(), 8, access=mmap.ACCESS_WRITE, offset=0)

        # set one of the pods to true (== 0x01) all the rest to false
        posn = 0
        while True:
            print(f'writing posn:{posn}')

            # reset to the start of the file
            mm.seek(0)

            # write the true/false values, only one is true
            for count in range(8):
                curr = b'\x01' if count == posn else b'\x00'
                mm.write(curr)

            # admire the view
            time.sleep(2)

            # set up for the next position in the next loop
            posn = (posn + 1) % 8

        mm.close()
        fd.close()

def checking():
    byte_val=b'\x00\x00\x00\x09'
    print(type(byte_val))
    # converting to int
    # byteorder is big where MSB is at start
    int_val = int.from_bytes(byte_val, "big")
    print(int_val)

    byte_val=b'\x00\x00\x01\x09'
    for a in byte_val:
        print(type(a), a)
        #a_val = int.from_bytes(a, "big")
        #print(a_val)

def checking2():
    # 16h57mn03mn123ms
    byte_val=b'\x01\x06\x05\x07\x00\x03\x01\x02\x03'
    print(type(byte_val))
    # converting to int
    # byteorder is big where MSB is at start
    int_val = int.from_bytes(byte_val, "big")
    print(int_val)

    for a in byte_val:
        print(type(a), a)
        #a_val = int.from_bytes(a, "big")
        #print(a_val)

def checking3():

    int_array = [1, 6, 5, 7, 0, 3, 1, 2, 3]
    byte_array = []
    for vali in int_array:
        # converting int to bytes with length 
        # of the array as 1 length and byter order as 
        # little
        bytes_val = vali.to_bytes(1, 'little')
        byte_array.append(bytes_val)
        
        # printing integer in byte representation
        print(bytes_val)

    print(byte_array)
    print(type(byte_array))

def test1():
    int_array = [8, 6, 5, 7, 0, 3, 1, 2, 3]
    byte_array = []
    for vali in int_array:
        bytes_val = vali.to_bytes(1, 'little')
        byte_array.append(bytes_val)

    fname = './pods.txt'
    if not os.path.isfile(fname):
        # create initial file
        with open(fname, "w+b") as fd:
            fd.write(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00')

    # at this point, file exists, so memory map it
    with open(fname, "r+b") as fd:
        mm = mmap.mmap(fd.fileno(), 9, access=mmap.ACCESS_WRITE, offset=0)

        while True:
            print(f'writin')

            # reset to the start of the file
            mm.seek(0)

            for byte_val in byte_array:
                mm.write(byte_val)

            # admire the view
            time.sleep(2)

        mm.close()
        fd.close()

            # now = datetime.now()
            # now = now.strftime("%m-%d-%YT%H:%M:%S.%f")[:-3]    


# test_org()
checking3()
# test1()