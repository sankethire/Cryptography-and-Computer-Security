lower = []
for i in range(97,123):
    lower.append(chr(i))

rev_lower = lower[::-1]

upper = []
for i in range(65,91):
    upper.append(chr(i))

rev_upper = upper[::-1]

def decipher_letter(cipher_letter):
    # print(cipher_letter)
    if(cipher_letter == " "):
        return " "
    elif(cipher_letter == "."):
        return "."
    elif(cipher_letter == ","):
	    return ","
    elif(ord(cipher_letter)>=97 and ord(cipher_letter)<=122):
        return rev_lower[ord(cipher_letter) - 97]
    else:
        return rev_upper[ord(cipher_letter) - 65]


cipher = "Nbzmnzi rh z xlfmgib rm Zhrz. Nzmb Ilsrmtbz Nfhornh orev gsviv. Gsvri orevh ziv evib wruurxfog. Gsvb nfhg nrtizgv z olg. Rm 2017, gsviv rh hgilmt nrorgzib zxgrlm ztzrmhg Ilsrmtbz Nfhornh. Gsviv rh z olg lu erlovmxv. Nzmb kvlkov wrv. Z olg lu kvlkov ifm zdzb gl zmlgsvi xlfmgib. Hlnv kvlkov yvorvev gszg gsviv rh tvmlxrwv lu gsv Ilsrmtbzh. Gsv Nbzmnzi tlevimnvmg zhph z xlnnrggvv gl urmw lfg dszg szkkvmh. Gsv xlnnrggvv hzbh gszg gsviv rh ml tvmlxrwv. Sldvevi, gsviv rh hvirlfh xirnv. Z olg lu kvlkov wl mlg yvorvev gsrh. Gsvb hzb gszg gsv tlevimnvmg dzmgh gl srwv gsv gifgs."

decipher = ""
for i in range(0,len(cipher)):
    decipher += decipher_letter(cipher[i])

print(decipher)

