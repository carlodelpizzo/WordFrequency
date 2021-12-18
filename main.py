def count_words(file_path='', case_sensitive=False):
    if file_path == '':
        file_path = input('Enter file path:\n')

    errors = (FileNotFoundError, PermissionError, OSError)
    try:
        text_file = open(file_path, 'r', errors='ignore')
    except errors:
        try:
            text_file = open(file_path + '.txt', 'r', errors='ignore')
        except errors:
            file_path = input('Error; Enter file path:\n')
            count_words(file_path)
            return

    symbols = [',', '.', ':', ';', '!', '?', '(', ')', "'", '"', '[', ']', '{', '}', '-', '_', '$', '%', '^', '&', '*',
               '@', '+', '=', '/', '\\', '<', '>', '|', '\n', '\t', '—', '¦']
    special_cases = ['â', '€', '™', 'â', '€']
    special_cases_replacement = {'â€™': "'", 'â€': ''}
    lowercase_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                         't',
                         'u', 'v', 'w', 'x', 'y', 'z']
    uppercase_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                         'T',
                         'U', 'V', 'W', 'X', 'Y', 'Z']
    word_atoms = special_cases + lowercase_letters + uppercase_letters
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    word_counts = {}
    unrecognized_characters = []
    for line in text_file:
        word_string = ''
        for character in line:
            if character in word_atoms:
                if not case_sensitive and character in uppercase_letters:
                    word_string += lowercase_letters[uppercase_letters.index(character)]
                    continue

                word_string += character

            elif word_string != '' and (character == ' ' or character in symbols):
                if character == "'":
                    word_string += character
                    continue

                for special_case in special_cases_replacement:
                    if special_case in word_string:
                        word_string = word_string.replace(special_case, special_cases_replacement[special_case])

                if word_string not in word_counts:
                    word_counts[word_string] = 1
                    word_string = ''
                    continue

                word_counts[word_string] += 1
                word_string = ''

            elif character != ' ' and character not in unrecognized_characters and\
                    character not in symbols and character not in numbers:
                unrecognized_characters.append(character)

        if word_string != '':
            if word_string in word_counts:
                word_counts[word_string] += 1
                continue

            word_counts[word_string] = 1

    if len(word_counts) == 0:
        print('No results')
        return

    ordered_list = []
    first_pass = True
    for key in word_counts:
        if first_pass:
            ordered_list.append([key, word_counts[key]])
            first_pass = False
            continue

        added = False
        for i in range(len(ordered_list)):
            if word_counts[key] > ordered_list[i][1]:
                ordered_list.insert(i, [key, word_counts[key]])
                added = True
                break

        if not added:
            ordered_list.append([key, word_counts[key]])

    word_count = 0
    for word in ordered_list:
        print(word[0], word[1])
        word_count += word[1]

    print('Total word count:', word_count)

    if len(unrecognized_characters) != 0:
        print('Unrecognized characters:', unrecognized_characters)


count_words()
