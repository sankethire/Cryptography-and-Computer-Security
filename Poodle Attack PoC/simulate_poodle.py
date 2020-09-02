# ######################################################################################################################## #
#                                                                                                                          # 
#           ASSIGNMENT 3: Working Simulation of SSLv3 Vulnerability (POODLE ATTACK - Proof Of Concept)                     #
#                                                                                                                          #
# ######################################################################################################################## #

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import HMAC

# ######################################################################################################################## #

class color:
    VIOLET = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# ######################################################################################################################## #


# pad_hash is function which pads "#" character to string message which has length not in multiples of 16 
# it returns a padded message of length in multiples of 16
def pad_hash(message):
    if(len(message)%16 != 0):
        return message + ("#" * ((16*((len(message)//16) + 1)) - len(message)))
    return message

# ######################################################################################################################## #


# Cryptographic key for computing MAC
# This cryptographic key is only accessible to sender and reciever
# i.e. the key is only used in encrypt and decrypt function
cryptographic_key = Random.new().read(AES.block_size)

# ######################################################################################################################## #


# add padding to a string block
# where a string block = message + MAC
# the return the padded string block which has length in multiple of 16
# this padded string block is then encrypted using AES encryption algorithm.
def pad(message, MAC):
    padded_message = bytes(message,'utf-8') + MAC
    padding_size = 16 - len(padded_message)%16
    if(padding_size == 0):
        padding_size = 16
    return padded_message + bytes([padding_size]) * padding_size


# ######################################################################################################################## #


# Encrypt function is applied by sender
# to encrypt the message using initialization vector and AES key
def encrypt(message, key):
    # Generate a random initialization vector using AES algorithm
    IV = Random.new().read(AES.block_size)
    
    # computing MAC using a message and a cryptographic key shared between sender and reciever
    MAC = HMAC.new(cryptographic_key).update(bytes(message, 'utf-8')).digest()
    
    # pad the message and MAC, to obtain a padded message of length in multiple of 16
    # to get more insight in padding, check out the code comments on pad function written above 
    padded_message = pad(message, MAC)

    # create an AES object for performing CBC encryption 
    cipher_object = AES.new(key, AES.MODE_CBC, IV)

    # generate the encrpted message from the secret message using encrypt function from AES class object 
    # and return it with IV attached to it
    return IV + cipher_object.encrypt(padded_message)

def cbc_encrypt(message,key):
    # Since the decryption process has to start with the last block of data we are encrypting the message 
    # using the AES key, we replace the last block with message block containing the last character 
    # of actual secret message 
    encrypted_message = encrypt(message, key)
    return encrypted_message[:-16] + encrypted_message[32:48]


# ######################################################################################################################## #


# Decrypt function is applied by reciever
# to decrypt the message using initialization vector and AES key
def decrypt(encrypted_message, key):

    # extract the initialization vector from the encrypted message
    IV = encrypted_message[:16]
    
    # extract the ciphertext from encrypted message 
    ciphertext = encrypted_message[16:]

    # create an AES object for performing CBC decryption
    cipher_object = AES.new(key, AES.MODE_CBC, IV)
    deciphertext = cipher_object.decrypt(ciphertext)

    # size of padding is the final or last byte of the deciphered text
    padding_size = deciphertext[-1]

    # removing padding of deciphered text using padding size
    deciphertext_without_padding = deciphertext[:-padding_size]
    
    # extracting the plaintext and MAC from the remaining deciphered text
    plaintext = deciphertext_without_padding[:-16]
    extracted_MAC = deciphertext_without_padding[-16:]

    # computing MAC using a message and a cryptographic key shared between sender and reciever
    MAC_of_deciphered_text = HMAC.new(cryptographic_key).update(plaintext).digest()

    # Comparing the extracted MAC and current MAC of deciphered text
    # So as to ensure the validity of deciphered character such that
    # the deciphered character is actually equal to character corresponding to the secret message 
    # Return True if valid
    if extracted_MAC == MAC_of_deciphered_text:
        return True
    else:
        return False


# ######################################################################################################################## #


def poodle_attack(secret_message, key):
    # pad the secret message using pad_hash function which pads "#" character to string message which has length not in multiples of 16
    message = pad_hash(secret_message)
    # print(message)

    print(f"{color.UNDERLINE}{color.BOLD}{color.BLUE}starting POODLE ATTACK.... {color.ENDC}")
    print()

    # As the name suggests, deciphered_bytes_batch returns the deciphered bytes found in a batch of 5 characters throughout the poodle_attack iterations
    deciphered_bytes_batch = ""
    # Counter for batch number
    batch_no = 0
    
    print(f"{color.BOLD}{color.YELLOW}Deciphered Bytes Found in batches of 5 characters: {color.ENDC}")

    # This is the string which gets appended by a deciphered byte found in the attack iterations
    # To get a final deciphered plaintext with few rotations at places 
    # Rotations are caused due to "right shifted rotation by one character" during each iteration
    # so as to extract the last character of the plaintext 
    deciphered_text=""
    
    for i in range(0,len(message)):
        while True:
            # encrypt the secret message using CBC encryption
            encrypted_message = cbc_encrypt(message,key)
            # If the Decryption is successful
            # i.e if the MAC addresses (current MAC address and computed MAC address) match 
            # then perform CBC decryption 
            if(decrypt(encrypted_message,key)):
                # CBC Decryption to get the last deciphered character of the encrypted message 
                # CBC Formula to find last deciphered byte in a plaintext of length 32
                # last character at 32nd position will be at index 31
                # i.e. deciphered byte = plaintext[31] = (encrypted_message[31]) ^ (encrypted_message[15-31]) ^ (decryption of last byte of encrypted_message = 16)  
                deciphered_byte = chr((encrypted_message[31]) ^ (encrypted_message[-17]) ^ 16)
                
                # print("Deciphered byte: ",deciphered_byte)
                
                # get the batch of 5 deciphered bytes found 
                if len(deciphered_bytes_batch)%5 == 0 and deciphered_bytes_batch != "":
                    print(f"Batch {batch_no}: [{deciphered_bytes_batch}]")
                    batch_no += 1
                    deciphered_bytes_batch=""

                if deciphered_byte != "#":
                    deciphered_text += deciphered_byte
                    deciphered_bytes_batch += deciphered_byte
                # break the while loop after each successful decryption 
                break
        # Perform "right shifted rotation" on a message by one character to access the last character
        message = message[-1] + message[:-1]
    
    # If the final batch of deciphered bytes is not a multiple of 5 characters and is non-empty 
    # then print out that final batch of deciphered bytes
    if(deciphered_bytes_batch != ""):
        print(f"Batch {batch_no}: [{deciphered_bytes_batch}]")


    # print out the deciphered text with few rotations at places
    print()
    print(f"{color.BOLD}{color.VIOLET}Deciphered Text on POODLE attack: {color.ENDC}")
    print(f"[{color.VIOLET}{deciphered_text}{color.ENDC}]")
    print()

    # reordering the deciphered text to get our final secret message i.e. deciphered_secret_message 
    deciphered_secret_message = ""
    for i in range(0,len(deciphered_text)):
        deciphered_secret_message += deciphered_text[(len(deciphered_text)-i+31)%len(deciphered_text)]

    # print out that deciphered secret message
    print(f"{color.BOLD}{color.GREEN}Deciphered Secret Message on POODLE attack: {color.ENDC}")
    print(f"[{color.BLUE}{deciphered_secret_message}{color.ENDC}]")
    print()


# ######################################################################################################################## #


def main():
    secret_message = "This is a secret message I have sent to you please keep it confidential"
    
    # Print out the secret message
    print()
    print(f"{color.BOLD}{color.RED}Secret Message: {color.ENDC}")
    print(f"[{color.RED}{secret_message}{color.ENDC}]")
    print()

    # Generate a random key using AES algorithm
    key = Random.new().read(AES.block_size)
    
    # run the POODLE simulation
    poodle_attack(secret_message, key)

 
if __name__ == "__main__":
    main()

# ######################################################################################################################## #