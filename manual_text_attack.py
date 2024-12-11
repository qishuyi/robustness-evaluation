import random
from nltk.corpus import wordnet
import argparse

def replace_with_synonyms(dataset: list[str]):
    result = []
    for index in range(len(dataset)):
        input = dataset[index]
        words = input.split(' ')
        num_words = random.randint(1, 3)
        all_indices = range(len(words))
        indices_to_replace = random.sample(all_indices, min(len(all_indices), num_words))
        for i in indices_to_replace:
            cur_word = words[i]
            all_synonyms = wordnet.synsets(cur_word)
            if all_synonyms:
                synonym = random.choice(all_synonyms).lemmas()[0].name()
                if synonym != cur_word:
                    words[i] = synonym
        result.append(' '.join(words))
    return result

def swap_characters(dataset: list[str]):
    result = []
    for index in range(len(dataset)):
        input = dataset[index]
        words = input.split(' ')
        num_words = random.randint(1, min(2, len(words)))
        all_indices = range(len(words))
        words_indices_to_swap = random.sample(all_indices, num_words)
        for i in words_indices_to_swap:
            num_chars = len(words[i])
            if num_chars > 2:
                char_index_to_swap = random.randint(1, num_chars - 2)
            elif num_chars == 2:
                char_index_to_swap = 0
            else:
                continue
            word_copy = ''
            for j in range(len(words[i])):
                if j == char_index_to_swap:
                    word_copy += words[i][char_index_to_swap + 1]
                elif j == char_index_to_swap + 1:
                    word_copy += words[i][char_index_to_swap]
                else:
                    word_copy += words[i][j]
            words[i] = word_copy
        result.append(' '.join(words))
    return result

def delete_character(dataset: list[str]):
    result = []
    for index in range(len(dataset)):
        input = dataset[index]
        words = input.split(' ')
        word_index_to_delete = random.randint(0, max(0, len(words) - 1))
        num_chars = len(words[word_index_to_delete])
        char_index_to_delete = random.randint(0, max(0, num_chars - 1))
        word_copy = ''
        for i in range(num_chars):
            if i != char_index_to_delete:
                word_copy += words[word_index_to_delete][i]
        words[word_index_to_delete] = word_copy
        result.append(' '.join(words))
    return result

def insert_character(dataset: list[str]):
    result = []
    for index in range(len(dataset)):
        input = dataset[index]
        words = input.split(' ')
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        if len(words) <= 1:
            result.append(' '.join(words))
            continue
        index = random.randint(1, max(1, len(words) - 1))
        if len(words[index]) <= 1:
            result.append(' '.join(words))
            continue
        char_index = random.randint(1, max(1, len(words[index]) - 1))
        insert_char = alphabet[random.randint(1, len(alphabet) - 1)]
        word_copy = ''
        for i in range(char_index):
            word_copy += words[index][i]
        word_copy += insert_char
        for i in range(char_index, len(words[index])):
            word_copy += words[index][i]
        words[index] = word_copy
        result.append(' '.join(words))
    return result

def substitute_character(dataset: list[str]):   
    result = []
    for index in range(len(dataset)):
        input = dataset[index]
        words = input.split(' ')
        word_indices_to_replace = random.sample(range(len(words)), min(len(words), max(len(words), 2)))
        chars_to_substitute = {
            'E': '3', 'I': '1', 'i': '1', 'O': '0', 'o': '0', 'Q': '0', 'C': '0',
            'c': '0', 'q': '9', 'B': '8', 'Z': '7', 'z': '7', 'S': '8', 's': '8'
        }
        for i in word_indices_to_replace:
            word_copy = ''
            char_index = random.randint(0, max(0, len(words[i]) - 1))
            for j in range(len(words[i])):
                if j == char_index and words[i][j] in chars_to_substitute:
                    word_copy += chars_to_substitute[words[i][j]]
                else:
                    word_copy += words[i][j]
            words[i] = word_copy
        result.append(' '.join(words))
    return result

def introduce_noise(dataset: list[str]):
    actions = ['synonyms', 'swap', 'delete', 'insert', 'substitute']
    # Get number of actions
    action_count = random.randint(1, len(actions))
    actions_to_apply = random.sample(actions, action_count)
    dataset = delete_character(dataset)
    for action in actions_to_apply:
        if action == 'synonyms':
            print('synonyms')
            dataset = replace_with_synonyms(dataset)
        if action == 'swap':
            print('swap')
            dataset = swap_characters(dataset)
        if action == 'delete':
            print('delete')
            dataset = delete_character(dataset)
        if action == 'insert':
            print('insert')
            dataset = insert_character(dataset)
        if action == 'substitute':
            print('substitute')
            dataset = substitute_character(dataset)
        print(len(dataset))
    return dataset
        
def main():
    parser = argparse.ArgumentParser(description='Attack an English-to-French dataset.')
    parser.add_argument('--dataset', type=str, required=True, help='Path to the .en file.')
    args = parser.parse_args()
    input_filepath = args.dataset
    with open(input_filepath, 'r') as input_file:
        dataset = input_file.readlines()
        noisy_dataset = introduce_noise(dataset)
        with open('noisy_dataset.en', 'w') as output_file:
            for sentence in noisy_dataset:
                output_file.write(sentence + '\n')

if __name__ == "__main__":
    main()




