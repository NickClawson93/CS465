import sys

num_bytes = 4
num_words = 4 #4, 6, 8 (Nk)
num_rounds = 10 #10, 12, 14 (Nr)

with open(sys.argv[1]) as in_file:
    byte_array = in_file.readline().strip().split()

with open(sys.argv[2]) as key_file:
    key = int(key_file.readline().strip(), 16)

with open("r_con.txt") as fh:
    temp_list = fh.readline().strip().split()
    r_con = []
    for each in temp_list:
        r_con.append(int(each,16))

def cipher(input_byte, key_expansion):
    state = byte_to_state(input_byte)
    first_key = words_to_state(key_expansion[0:4])

    state = add(state, first_key)
    for i in range(1, num_rounds):
        #print_state(state)
        state = sub_bytes(state)
        #print_state(state)
        state = shift_rows(state)
        #print_state(state)
        state = mix_columns(state)
        #print_state(state)
        state = add(state, words_to_state(key_expansion[i*4:i*4 + 4]))

    state = sub_bytes(state)
    state = shift_rows(state)
    state = add(state, words_to_state(key_expansion[-4:]))
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

def key_expansion(key):
    words = []
    temp_key = key
    for i in range(num_words):
        temp_word = temp_key % 4294967296
        temp_key = temp_key / 4294967296
        words.insert(0, temp_word)
    
    for i in range(num_words, num_bytes * (num_rounds + 1)):
        temp = words[i-1]
        if i % num_words == 0:
            temp = sub_word(rot_word(temp)) ^ r_con[i/num_words]
        elif num_words == 8 and i % num_words == 4:
            temp = sub_word(temp)
        words.append(words[i - num_words] ^ temp)
#    for each in words:
#        word = each
#        print '{:08x}'.format(word)
#        word = rot_word(word)
#        print '{:08x}'.format(word)
#        word = sub_word(word)
#        print '{:08x}'.format(word)
    return words

def rot_word(word):
    string_word = '{:08x}'.format(word)
    string_word = string_word[2:] + string_word[:2]
    return int(string_word, 16)

def sub_word(word):
    string_word = '{:08x}'.format(word)
    mini_words = []
    result_string = ""
    for i in range(4):
        mini_words.append(int(string_word[2*i:2*i+2], 16))
        coord = mini_words[i]
        result_string += '{:02x}'.format(sbox[coord/16][coord % 16])
    return int(result_string, 16)

def words_to_state(words):    
    result = empty_list()
    for i in range(4):
        word = words[i]
        #print_as_hex(word)
        for j in range(4):
            result[3-j][i] = word % 256
            word = word / 256
    return result

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

def print_as_hex(number):
    print '{:02x}'.format(number)

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
            coord = state[i][j]
            result[i][j] = sbox[coord/16][coord % 16] 
    return result

def inv_sub_bytes(state):
    result = empty_list()
    for i in range(len(state)):
        for j in range(len(state[i])):
            coord = state[i][j]
            result[i][j] = inv_sbox[coord/16][coord % 16] 
    return result

def shift_rows(state):
    result = empty_list()
    for i in range(len(state)):
        for j in range(len(state[i])):
            result[i][j] = state[i][(j + i) % 4]
    return result

def inv_shift_rows(state):
    result = empty_list()
    for i in range(len(state)):
        for j in range(len(state[i])):
            result[i][j] = state[i][(j - i) % 4]
    return result

def mix_columns(state):
    result = empty_list()    
    for i in range(4):
        result[0][i] = ff_multiply(state[0][i], 2) ^ ff_multiply(state[1][i], 3) ^ state[2][i] ^ state[3][i]
        result[1][i] = ff_multiply(state[1][i], 2) ^ ff_multiply(state[2][i], 3) ^ state[0][i] ^ state[3][i]
        result[2][i] = ff_multiply(state[2][i], 2) ^ ff_multiply(state[3][i], 3) ^ state[0][i] ^ state[1][i]
        result[3][i] = ff_multiply(state[3][i], 2) ^ ff_multiply(state[0][i], 3) ^ state[1][i] ^ state[2][i]
    return result

def inv_mix_columns(state):
    result = empty_list()    
    for i in range(4):
        result[0][i] = ff_multiply(state[0][i], int('0e', 16)) ^ ff_multiply(state[1][i], int('0b', 16)) ^ ff_multiply(state[2][i], int('0d', 16)) ^ ff_multiply(state[3][i], int('09', 16))
        result[1][i] = ff_multiply(state[0][i], int('09', 16)) ^ ff_multiply(state[1][i], int('0e', 16)) ^ ff_multiply(state[2][i], int('0b', 16)) ^ ff_multiply(state[3][i], int('0d', 16))
        result[2][i] = ff_multiply(state[0][i], int('0d', 16)) ^ ff_multiply(state[1][i], int('09', 16)) ^ ff_multiply(state[2][i], int('0e', 16)) ^ ff_multiply(state[3][i], int('0b', 16))
        result[3][i] = ff_multiply(state[0][i], int('0b', 16)) ^ ff_multiply(state[1][i], int('0d', 16)) ^ ff_multiply(state[2][i], int('09', 16)) ^ ff_multiply(state[3][i], int('0e', 16))
    return result

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
    while multiply_bit <= byte_b:
        if multiply_bit != 1:
            current_multiplier = xtime(current_multiplier)
        if byte_b & multiply_bit == multiply_bit:
            current_total = add_bytes(current_multiplier, current_total)
        multiply_bit *= 2
    return current_total

sbox = make_sbox("sbox.txt")
inv_sbox = make_sbox("inv_sbox.txt")
words = key_expansion(key)
cipher(byte_array, words)
