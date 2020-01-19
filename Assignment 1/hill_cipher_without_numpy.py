import math
import sys

def make_square_matrix(k_array):
    n = int(math.sqrt(len(k_array)))
    square_matrix = []
    k = 0
    for i in range(0,n):
        row = []
        for j in range(0,n):
            row.append(int(k_array[k]))
            k += 1
        square_matrix.append(row)
    return square_matrix
    
def alpha_to_num(alphabet):
    if(ord(alphabet) >= 97 and ord(alphabet) <= 122):
        return ord(alphabet) - 97
    else:
        print("ERROR: Only a-z alphabets are valid")

def matrix_multiplication(a,b):
    product = [0 for x in range(len(a))]
    for i in range(0,len(a)):
            for k in range(0,len(b)):
                product[i] += a[i][k] * b[k]
    return product    

def modulo_26(matrix):
    for i in range(0,len(matrix)):
        matrix[i] %= 26
    return matrix

def num_to_alpha(num):
    return chr(97 + num)

def get_alpha_array(arr):
    for i in range(0,len(arr)):
        arr[i] = num_to_alpha(int(arr[i]))
    return arr    

def add_space(s, pos):
    s = s[0:pos] + " " + s[pos:]
    return s

# ########################################################## #
#                   ENCRYPTION ALGORITHM                     #
# ########################################################## #
def encrypt(key_matrix, plain_text):
    space_pos = []
    for i in range(0,len(plain_text)):
        if(plain_text[i] == " "):
            space_pos.append(i)

    words = plain_text.split(" ")
    converted_plain_text = ("").join(words)
    # print(converted_plain_text)

    text_cols = []
    total_text_cols = (len(converted_plain_text) // len(key_matrix)) + (len(converted_plain_text) % len(key_matrix))
    len_text_col = len(key_matrix)

    k = 0
    for i in range(0,total_text_cols):
        row = []
        for j in range(0,len_text_col):
            if(k < len(converted_plain_text)):
                row.append(alpha_to_num(converted_plain_text[k]))
            else:
                row.append(alpha_to_num("z"))
            k += 1
        text_cols.append(row)

    # print(text_cols)

    encrypt_cols = []
    for i in range(0,len(text_cols)):
        encrypt_cols.append(("").join(get_alpha_array(modulo_26(matrix_multiplication(key_matrix,text_cols[i])))))

    encrypted_text = ("").join(encrypt_cols)
    # print(temp_encrypted_text)


    for i in range(0,len(space_pos)):
        encrypted_text = add_space(encrypted_text,space_pos[i])
    
    return encrypted_text

# ########################################################## #

# ########################################################## #
#                   DECRYPTION ALGORITHM                     #
# ########################################################## #

def transpose(matrix):
    return map(list,zip(*matrix))

def minor_matrix(matrix,i,j):
    return [x[:j] + x[j+1:] for x in (matrix[:i]+matrix[i+1:])]

def determinant(matrix):
    if(len(matrix) == 2):
        return matrix[0][0]*matrix[1][1]-matrix[0][1]*matrix[1][0]
    det = 0
    for i in range(len(matrix)):
        det += ((-1)**i)*matrix[0][i]*determinant(minor_matrix(matrix,0,i))
    return det

def adjoint(matrix):
    if(len(matrix) == 2):
        return [[matrix[1][1], -1*matrix[0][1]], [-1*matrix[1][0], matrix[0][0]]]
    cofactor_matrix = []
    for i in range(len(matrix)):
        row = []
        for j in range(len(matrix)):
            minor = minor_matrix(matrix,i,j)
            row.append(((-1)**(i+j)) * determinant(minor))
        cofactor_matrix.append(row)
    cofactor_matrix = list(transpose(cofactor_matrix))
    for i in range(len(cofactor_matrix)):
        for j in range(len(cofactor_matrix)):
            cofactor_matrix[i][j] = cofactor_matrix[i][j]
    return cofactor_matrix

def get_multiplicative_inverse(determinant):
    multiplicative_inverse = -1
    for i in range(26):
        inverse = determinant * i
        if inverse % 26 == 1:
            multiplicative_inverse = i
            break
    return multiplicative_inverse

def inverse(matrix):
    multiplicative_inverse_det = get_multiplicative_inverse(determinant(matrix))
    adjoint_matrix = adjoint(matrix)
    for i in range(0,len(matrix)):
        for j in range(0,len(matrix)):
            adjoint_matrix[i][j] *= multiplicative_inverse_det
    for i in range(0,len(adjoint_matrix)):
        for j in range(0,len(adjoint_matrix)):
            adjoint_matrix[i][j] %= 26
    return adjoint_matrix
    


# cipher_text = "hiat"
def decrypt(key_matrix, cipher_text):
    space_pos = []
    for i in range(0,len(plain_text)):
        if(plain_text[i] == " "):
            space_pos.append(i)
    cipher_words = cipher_text.split(" ")
    converted_cipher_text = ("").join(cipher_words)
    # print(converted_cipher_text)

    ciphertext_cols = []
    total_ciphertext_cols = (len(converted_cipher_text) // len(key_matrix)) + (len(converted_cipher_text) % len(key_matrix))
    len_ciphertext_col = len(key_matrix)

    ck = 0
    for i in range(0,total_ciphertext_cols):
        row = []
        for j in range(0,len_ciphertext_col):
            if(ck < len(converted_cipher_text)):
                row.append(alpha_to_num(converted_cipher_text[ck]))
            else:
                row.append(alpha_to_num("z"))
            ck += 1
        ciphertext_cols.append(row)

    # print(ciphertext_cols)

    decrypt_cols = []
    for i in range(0,len(ciphertext_cols)):
        decrypt_cols.append(("").join(get_alpha_array(modulo_26(matrix_multiplication(inverse(key_matrix),ciphertext_cols[i])))))

    decrypted_text = ("").join(decrypt_cols)
    # print(temp_decrypted_text)
    # print(inverse(key_matrix))

    for i in range(0,len(space_pos)):
        decrypted_text = add_space(decrypted_text,space_pos[i])
    
    return decrypted_text

def read_key_and_plaintext(input_file):
    f = open(input_file, "r")
    inputs = f.read().split("\n")
    key, plain_text = make_square_matrix(inputs[0].split(" ")), inputs[1]
    f.close()
    return key,plain_text

def read_key_and_ciphertext(input_file):
    f = open(input_file, "r")
    inputs = f.read().split("\n")
    key, cipher_text = make_square_matrix(inputs[0].split(" ")), inputs[1]
    f.close()
    return key,cipher_text

if __name__ == "__main__":
    key_matrix, plain_text = read_key_and_plaintext(sys.argv[1])
    key_matrix, cipher_text = read_key_and_ciphertext(sys.argv[2])
    encrypted_text = encrypt(key_matrix, plain_text)
    decrypted_text = decrypt(key_matrix, cipher_text)

    print("\nPlain Text: \n")
    print(plain_text)
    print("\n-------------------------------------------------\n")

    print("\nEncrypted Text: \n")
    print(encrypted_text)
    print("\n-------------------------------------------------\n")

    print("\nCipher Text: \n")
    print(cipher_text)
    print("\n-------------------------------------------------\n")

    print("\nDecrypted Text: \n")
    print(decrypted_text)
    print("\n-------------------------------------------------\n")

    print(plain_text == decrypted_text[:-1])
    print(cipher_text == encrypted_text)


# key = input().split(" ")
# key_matrix = make_square_matrix(key)

# plain_text = "speaking of dreams in a figurative sense then slowly talking about its impact in the literal sense the \
# writer keeps stressing on one very important point that dreams have an important role to play in \
# american politics after all a liberal society is formed on the basis of ones imagination these imaginations \
# are a result of ones free thoughts which can be related to dreams as dreaming provides a picture of the \
# real world uncovering things which otherwise might not have been pondered upon due to narrowed and \
# limited freedom of imagining it may seem reckless to consider the possibility of turning to dreams to \
# work through the political conditions today but ignoring them altogether might even be more reckless \
# says the author"

# # plain_text = "help"

# print("\nPlain Text: \n")
# print(plain_text)
# print("\n-------------------------------------------------\n")

# encrypted_text = encrypt(key_matrix, plain_text)
# print("\nEncrypted Text: \n")
# print(encrypted_text)
# print("\n-------------------------------------------------\n")

# cipher_text = "zskkkisx la nzkkgi hu p emexwfkfqm oxkse xfxk nukycj cpmdhuc cmpdi zee cxqgma lf xkj gronkxk zxkse xfy mitono fwiuj lqwvikhus iq tml gfel eoilphnav busfx xffk nzkkgi ylgf na eoilphnab ndkp up iivg ea nqcitsst zdkzeagg gldji hoi v grihkxk zcigswd wy wzurtc jw xfn qcewy la jwmo eoskhufkkaf xkjse \
# eoskhufkkacr zyk k wvownf la jwmo frwi xfemxset lgage xna ih wvivont lf owvkug gp ywvkuhuv oadsdazg g qbxcxwa ql dkj wvho gwrlw rgzhsjihuh mwhsxu iwhni bgkjyzwyu emedv qtx flwn qwit zjwazwvw rilj fkw sv anjvkytc nav peozetc frwiehu ke peeayyjsx ze eek mwid cqwtamol qc ijwecazp hkj ilikxabizey ol dxwyjsx sv nzkkgi sv gwof xfadqid vkj ilgralsso hjwmxaljwl qfouo eza lpcvuhuh mkje enfogpukju rmedv vgxk ih ukwv wvwautik ggkm xfk kdiorhr"

# # cipher_text = "hiat"

# print("\nCipher Text: \n")
# print(cipher_text)
# print("\n-------------------------------------------------\n")


# decrypted_text = decrypt(key_matrix, cipher_text)
# print("\nDecrypted Text: \n")
# print(decrypted_text)
# print("\n-------------------------------------------------\n")
