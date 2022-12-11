from ascii_codes import ascii_dict

def sumPolynom(first, second):
    result = ""
    for i in range(len(first)):
        result += str((int(first[i]) + int(second[i])) % 2)

    return result

def textToBits(string):    
    bits = ""
    
    for j in range(len(string)):
        bits += ascii_dict[string[j]]
    
    binblocksText = []
    for i in range(0, len(bits), 64):
        b = bits[i:i + 64].zfill(64)

        binblocksText.append(b[:32])
        binblocksText.append(b[32:])

    return binblocksText

def encodeFunc(keys, text, table):
        answRaw = []

        for index in range(0, len(text), 2):

            N1 = text[index + 1]
            N2 = text[index]
            prevN1 = N1

            for k in range(4):
                if k == 3:
                    keysChecked = list(reversed(keys))
                else:
                    keysChecked = keys
                for key in keysChecked:
                    N1 = bin((int(N1, 2) + int(key, 2)) % (2**32))[2:].zfill(32)
                    
                    binblocksText = []
                    for i in range(0, len(N1), 4):
                        c = N1[i:i + 4].zfill(4)

                        binblocksText.append(c)

                    binblocksText = list(reversed(binblocksText))
                    binblocksTextCopy = binblocksText

                    for ind, block in enumerate(binblocksTextCopy):
                        block10 = int(block, 2)
                        replacement = bin(table[ind][block10])[2:].zfill(4)
                        binblocksText[ind] = replacement

                    binblocksText = list(reversed(binblocksText))

                    binblocksText = ''.join(list(reversed(binblocksText)))
                    N1 = binblocksText[11:] + binblocksText[:11]

                    N1 = sumPolynom(N1, N2)

                    N2 = prevN1
                    prevN1 = N1


            answRaw.append(N1)
            answRaw.append(N2)
        
        answRaw = "".join(answRaw)
        answEnd = [answRaw[i:i+8] for i in range(0, len(answRaw), 8)]
        
        return answEnd

def clearArray(binVals, valToDelete):
    newArr = []
    for val in binVals:
        if val != valToDelete:
            newArr.append(val)

    return newArr

def decodeFunc(keys, text, table):
        answRaw = []

        for index in range(0, len(text), 2):

            N1 = text[index + 1]
            N2 = text[index]
            prevN1 = N1

            for k in range(4):
                if k == 0:
                    keysChecked = keys
                else:
                    keysChecked = list(reversed(keys))
                    
                for key in keysChecked:
                    N1 = bin((int(N1, 2) + int(key, 2)) % (2**32))[2:].zfill(32)
                    
                    binblocksText = []
                    for i in range(0, len(N1), 4):
                        c = N1[i:i + 4].zfill(4)

                        binblocksText.append(c)

                    binblocksText = list(reversed(binblocksText))
                    binblocksTextCopy = binblocksText

                    for ind, block in enumerate(binblocksTextCopy):
                        block10 = int(block, 2)
                        replacement = bin(table[ind][block10])[2:].zfill(4)
                        binblocksText[ind] = replacement

                    binblocksText = list(reversed(binblocksText))

                    binblocksText = ''.join(list(reversed(binblocksText))) # склейка блоков в одну строку
                    N1 = binblocksText[11:] + binblocksText[:11]

                    N1 = sumPolynom(N1, N2)
                    
                    N2 = prevN1
                    prevN1 = N1

            answRaw.append(N1)
            answRaw.append(N2)
        
        
        answRaw = "".join(answRaw)
        answEnd = [answRaw[i:i+8] for i in range(0, len(answRaw), 8)]
        
        return answEnd

def binaryToText(binVals):
    asciiKeys = list(ascii_dict.keys())
    asciiValues = list(ascii_dict.values())

    end = ""
    for value in binVals:
        indexOfVal = asciiValues.index(value)
        end += asciiKeys[indexOfVal]

    return end

def start(isEnc):
    key = input('Input key:\n')
    with open('opentext.txt', "r",encoding="utf8") as f:
        f = f.read()
        f = f.replace('ё', 'е')

    table = [
        [12, 4, 6, 2, 10, 5, 11, 9, 14, 8, 13, 7, 0, 3, 15, 1],
        [6, 8, 2, 3, 9, 10, 5, 12, 1, 14, 4, 7, 11, 13, 0, 15],
        [11, 3, 5, 8, 2, 15, 10, 13, 14, 1, 7, 4, 12, 9, 6, 0],
        [12, 8, 2, 1, 13, 4, 15, 6, 7, 0, 10, 5, 3, 14, 9, 11],
        [7, 15, 5, 10, 8, 1, 6, 13, 0, 9, 3, 14, 11, 4, 2, 12], 
        [5, 13, 15, 6, 9, 2, 12, 10, 11, 7, 8, 1, 4, 3, 14, 0], 
        [8, 14, 2, 5, 6, 9, 1, 12, 15, 4, 11, 0, 13, 10, 3, 7], 
        [1, 7, 14, 13, 0, 5, 8, 3, 4, 15, 10, 6, 9, 12, 11, 2],
    ]

    if len(key) != 32 or f == '':
        print("Некорректное значение ключа")    
    else:
        bittedKey = textToBits(key) 

        if isEnc:
            bittedOpenText = textToBits(f) 
            cipher = binaryToText(encodeFunc(bittedKey, bittedOpenText, table))   

            print("Encrypted text:" , cipher)
            
            with open('cipherText.txt', "w",encoding="utf8") as f:
                f.write(cipher)

        else:
            with open('cipherText.txt', "r",encoding="utf8") as f:
                f = f.read()

            bittedCipherText = textToBits(f)
            end = binaryToText(clearArray(decodeFunc(bittedKey, bittedCipherText, table), "00000000"))
        
            print("Decrypted text:" , end)

            with open('decipheredText.txt', "w",encoding="utf8") as f:
                f.write(end)
        
typeOfOperation = input("Encrypt? (Y/N)\n")

if typeOfOperation.strip().lower() == "y":
    start(True)
elif typeOfOperation.strip().lower() == "n":
    start(False)
else:
    print("Wrong input")
