N = 11

# Read the file
with open(f"./words_fr/fr_full.txt", "r") as file:
    words = file.read()
    words = words.split("[")[1].split("]")[0]
    words = [word.replace("\"", "").strip() for word in words.split(",")]
    words = list(filter(lambda x : len(x) == N, words)) 

print(len(words))
exit()

# Construct a data structure for convenience
def word_to_list(word):
        word_list = {chr(i) : 0 for i in range(65, 65+26)}
        for letter in word:
            try:
                word_list[letter] += 1
            except:
                return {}
        return word_list

def words_to_db(words):
    words_db = {}
    for word in words:
        word_list = word_to_list(word)
        if len(word_list) != 0:
            words_db[word] = word_list
    
    return words_db


# Define helper functions for the game
def test_word(words_db, choosen_word, test_word):
    if len(test_word) != len(choosen_word) :
        print("Different word size not yet implemented")
        exit(0)

    choosen_word_db = words_db[choosen_word]
    correct = True
    placement = {}
    presence = {}
    alphabet = set(chr(i) for i in range(65, 65+26))

    for i in range(len(test_word)):
        letter = test_word[i]
        if letter == choosen_word[i]: # right placement
            placement.setdefault(letter, [])
            placement[letter].append(i)
        else:
            correct = False
        
        presence.setdefault(letter, 0)
        correct = False
        if choosen_word_db[letter] > presence[letter]:
            presence[letter] += 1
        else:
            alphabet.discard(letter)

    return (correct, placement, presence, alphabet)

# def merge_informations(information1, information2):
#     # TODO 
#     return information1

def word_compatibility(informations, word):
    # Check for letter placement
    _ , placement, presence, alphabet = informations
    for letter_right in placement:
        for position in placement[letter_right]:
            if word[position] != letter_right:
                return False
    
    # Check for max number of letter
    word_dict = {}
    for letter in word:
        word_dict.setdefault(letter, 0)
        word_dict[letter] += 1
    
    for letter in word_dict:
        if word_dict[letter] > presence.get(letter, 0):
            if letter not in alphabet:
                return False

    return True

def reduce_words_db(informations, words_db):
    return {word: v for word, v in words_db.items() if word_compatibility(informations, word)}

def valid_try(word):
    return False


# ##################################
# oneit_length = []

# words_db = words_to_db(words)
# print("Taille total de la db :", len(words_db))
# choosen_word = words[0]
# print("Choosed word :", choosen_word)
# for i, word in enumerate(words):
#     print(i)
#     informations = test_word(words_db, choosen_word, word)
#     local_words_db = reduce_words_db(informations, words_db)
#     oneit_length.append(len(local_words_db))
#     print(word)
#     print(oneit_length[i])
#     exit()

# print(sum(oneit_length)/len(oneit_length))

# TODO refaire implémenter les patterns
# TODO refaire implémenter un choix stochastique du premier mot, en le testant contre 1 ou 2% de la cohorte de manière aléatoire puis extraire le top nth et les restester contre toute la cohorte