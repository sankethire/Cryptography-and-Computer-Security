import numpy as np 
import math

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

def get_multiplicative_inverse(determinant):
    multiplicative_inverse = -1
    for i in range(26):
        inverse = determinant * i
        if inverse % 26 == 1:
            multiplicative_inverse = i
            break
    return multiplicative_inverse

def cofactor(matrix):
    return np.linalg.inv(matrix).T * np.linalg.det(matrix)

def inverse(matrix):
    multiplicative_inverse_det = get_multiplicative_inverse(int(np.linalg.det(matrix)))
    cofactor_matrix = cofactor(matrix)
    adjoint_matrix = (np.transpose(cofactor_matrix)).tolist()
    for i in range(0,len(adjoint_matrix)):
        for j in range(0,len(adjoint_matrix)):
            adjoint_matrix[i][j] = int(adjoint_matrix[i][j] * multiplicative_inverse_det)
    for i in range(0,len(adjoint_matrix)):
        for j in range(0,len(adjoint_matrix)):
            adjoint_matrix[i][j] %= 26
    return adjoint_matrix


# ########################################################## #
#                   ENCRYPTION ALGORITHM                     #
# ########################################################## #

def encrypt(key, plain_text):
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
    
    encrypt_cols = []
    for i in range(0,len(text_cols)):
        encrypt_cols.append(("").join(get_alpha_array(modulo_26((np.dot(key_matrix,text_cols[i])).tolist()))))

    encrypted_text = ("").join(encrypt_cols)
    for i in range(0,len(space_pos)):
        encrypted_text = add_space(encrypted_text,space_pos[i])

    return encrypted_text


# ########################################################## #
#                   DECRYPTION ALGORITHM                     #
# ########################################################## #

def decrypt(key, cipher_text):
    space_pos = []
    for i in range(0,len(cipher_text)):
        if(cipher_text[i] == " "):
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
        decrypt_cols.append(("").join(get_alpha_array(modulo_26((np.dot(inverse(key_matrix),ciphertext_cols[i])).tolist()))))

    decrypted_text = ("").join(decrypt_cols)
    # print(temp_decrypted_text)
    # print(inverse(key_matrix))

    for i in range(0,len(space_pos)):
        decrypted_text = add_space(decrypted_text,space_pos[i])

    return decrypted_text

key = input().split(" ")
key_matrix = make_square_matrix(key)

plain_text = "speaking of dreams in a figurative sense then slowly talking about its impact in the literal sense the \
writer keeps stressing on one very important point that dreams have an important role to play in \
american politics after all a liberal society is formed on the basis of ones imagination these imaginations \
are a result of ones free thoughts which can be related to dreams as dreaming provides a picture of the \
real world uncovering things which otherwise might not have been pondered upon due to narrowed and \
limited freedom of imagining it may seem reckless to consider the possibility of turning to dreams to \
work through the political conditions today but ignoring them altogether might even be more reckless \
says the author"

# plain_text = "help"

print("\nPlain Text: \n")
print(plain_text)
print("\n-------------------------------------------------\n")

encrypted_text = encrypt(key_matrix, plain_text)
print("\nEncrypted Text: \n")
print(encrypted_text)
print("\n-------------------------------------------------\n")

cipher_text = "zskkkisx la nzkkgi hu p emexwfkfqm oxkse xfxk nukycj cpmdhuc cmpdi zee cxqgma lf xkj gronkxk zxkse xfy mitono fwiuj lqwvikhus iq tml gfel eoilphnav busfx xffk nzkkgi ylgf na eoilphnab ndkp up iivg ea nqcitsst zdkzeagg gldji hoi v grihkxk zcigswd wy wzurtc jw xfn qcewy la jwmo eoskhufkkaf xkjse \
eoskhufkkacr zyk k wvownf la jwmo frwi xfemxset lgage xna ih wvivont lf owvkug gp ywvkuhuv oadsdazg g qbxcxwa ql dkj wvho gwrlw rgzhsjihuh mwhsxu iwhni bgkjyzwyu emedv qtx flwn qwit zjwazwvw rilj fkw sv anjvkytc nav peozetc frwiehu ke peeayyjsx ze eek mwid cqwtamol qc ijwecazp hkj ilikxabizey ol dxwyjsx sv nzkkgi sv gwof xfadqid vkj ilgralsso hjwmxaljwl qfouo eza lpcvuhuh mkje enfogpukju rmedv vgxk ih ukwv wvwautik ggkm xfk kdiorhr"

# cipher_text = "hiat"

print("\nCipher Text: \n")
print(cipher_text)
print("\n-------------------------------------------------\n")


decrypted_text = decrypt(key_matrix, cipher_text)
print("\nDecrypted Text: \n")
print(decrypted_text)
print("\n-------------------------------------------------\n")

