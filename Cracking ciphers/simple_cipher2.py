lower = []
for i in range(97,123):
    lower.append(chr(i))

cipher_lower = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m']

upper = []
for i in range(65,91):
    upper.append(chr(i))

cipher_upper = ['Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M']

def decipher_letter(cipher_letter):
    # print(cipher_letter)
    if(cipher_letter == " "):
        return " "
    elif(cipher_letter == "."):
        return "."
    elif(cipher_letter == "'"):
        return "'"
    elif(ord(cipher_letter)>=97 and ord(cipher_letter)<=122):
        return lower[cipher_lower.index(cipher_letter)]
    else:
        return upper[cipher_upper.index(cipher_letter)]

cipher = "Htghst xlt lxflekttfl zg hkgztez zitok laof ykgd zit lxf. Zitkt ol q ftv lzxrn. Oz lqnl ziqz lgdt eitdoeqsl of lxflekttfl utz ofzg htghst'l wsggr Leotfzolzl ztlz ygxk royytktfz lxflekttfl qfr lob eitdoeqsl. Zitn yofr ziqz qss lob eitdoeqsl utz ofzg zit wgrn. Zitn rg fgz afgv viqz zitlt eitdoeqsl rg zg htghst. Oz ol vgkknofu. Leotfzolzl dxlz rg dgkt ktltqkei zg xfrtklzqfr igv eitdoeqsl utz ofzg zit wgrn."

decipher = ""
for i in range(0,len(cipher)):
    decipher += decipher_letter(cipher[i])

print(decipher)