#text_to_morse
#Permanent Variables
MORSE_CODE_DICT= {
    'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.',
    'f': '..-.', 'g': '--.', 'h': '....', 'i': '..', 'j': '.---',
    'k': '-.-', 'l': '.-..', 'm': '--', 'n': '-.', 'o': '---',
    'p': '.--.', 'q': '--.-', 'r': '.-.', 's': '...', 't': '-',
    'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-', 'y': '-.--', 'z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', " ": " "
}

CHAR_LIST = [chr(i) for i in range(ord('a'), ord('z')+1)] + [str(i) for i in range(10)] + [" "]
#####---------------------------------------------#####

#Ask for input function
def ask_input():
    '''Ask user for input and make string lowercase and list'''
    #input function
    string = input("What is the text to translate to morse?").lower()
    #break string into list
    string_list = [char for char in string]
    return(string_list)

#Verify if there are symbols in the list. If not, repeat loop for asking input.
good_to_go = False
while not good_to_go:
    string_list = ask_input()
    if any(char not in CHAR_LIST for char in string_list):
        print("No symbols allowed.")
    else:
        good_to_go = True

#Step 3: Verify list against dictionary
morse_txt = " ".join([MORSE_CODE_DICT[char] for char in string_list])
print(f"Translated Morse Code: {morse_txt}")

