import sys

with open(sys.argv[1]) as in_file:
    byte_array = in_file.readline().strip().split()

with open(sys.argv[2]) as key_file:
    key = key_file.readline().strip().split()


def cipher(input_byte, key):
    state = byte_to_state(input_byte)
    key = byte_to_state(key)

    state = add(state, key)
    print_state(state)

def make_sbox(filename):
    with open(filename) as sbox_file:
        lines = sbox_file.readlines()
        sbox = []
        counter = 0
        for line in lines:
            temp_list = line.strip().split()
            new_list = []			
            sbox.append(new_list)
            for each in temp_list:
                sbox[counter].append(int(each, 16))
            counter += 1
    return sbox

def byte_to_state(in_byte):
    state = empty_list()
    counter = 0
    for i in range(4):
        for j in range(4):
            state[j][i] = int(in_byte[counter], 16)
            counter += 1
    return state

def empty_list():
    state = []
    for i in range(4):
        new_list = []
        state.append(new_list)
        for j in range(4):
            state[i].append(0)
    return state

def print_state(state):
    for i in range(len(state)):
        for j in range(len(state[i])):
            print '{:02x}'.format(state[i][j]),
        print
    print

def add(state, key):
    result = empty_list()
    for i in range(len(state)):
        for j in range(len(state[i])):
            result[i][j] = state[i][j] ^ key[i][j]
    return result

def sub_bytes(state):
    result = empty_list()
    for i in range(len(state)):
        for j in range(len(state[i])):
            result[i][j] = 
    return

def shift_rows(state):
    return

def mix_columns(state):
    return

def add_round_key(state, key):
    return

def add_bytes(byte_a, byte_b):
    return byte_a ^ byte_b

def xtime(in_byte):
    result = in_byte*2
    if result > 255:
        result = result ^ int("11b", 16)
    return result

def ff_multiply(byte_a, byte_b):
    current_multiplier = byte_a
    current_total = 0
    multiply_bit = 1
    while multiply_bit < byte_b:
        if multiply_bit != 1:
            current_multiplier = xtime(current_multiplier)
        if byte_b & multiply_bit == multiply_bit:
            current_total = add_bytes(current_multiplier, current_total)
        multiply_bit *= 2
    return current_total
    
sbox = make_sbox("sbox.txt")
inv_sbox = make_sbox("inv_sbox.txt")
xtime(int("57", 16))
print '{:02x}'.format(ff_multiply(int("57", 16), int("13", 16)))
cipher(byte_array, key)
