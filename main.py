# Johnny Nguyen
# CPSC 323
# Tokenizer Project

import re

# function to remove the comments and excess space in the input file and output it to an output file. returns the list of comments.
def clean(input_file, output_file):
    # open file, read every line
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # arrays to store cleaned lines and comments
    new_lines = []
    comments = []
    block_comment = False  # flag check if we are in a block comment

    for line in lines:
        # if inside block comment, keep going until we reach end
        if block_comment:
            if '"""' in line:  # End of block comment
                comment, code = line.split('"""', 1)  # Split after the closing """
                comments.append(comment.strip())  # Capture the remaining part of the block comment
                block_comment = False  # End the block comment mode
            else:
                comments.append(line.strip())  # Continue capturing the block comment lines
            continue  # Skip further processing of this line

        # find start of block comment
        if '"""' in line:
            code, comment = line.split('"""', 1)
            comments.append(comment.strip())  # Capture the start of the block comment
            block_comment = True  # Enable block comment mode
            continue  # Skip processing this line since it's part of a comment

        # remove comments after #
        if '#' in line:
            code, comment = line.split('#', 1)
            comments.append(comment.strip())  # add comment to comment list
        else:
            code = line

        # remove spaces
        new_line = ' '.join(code.split())

        # add the cleaned up lines
        if new_line:
            new_lines.append(new_line)
    
    # remove empty "" from comments list
    comments = [comment for comment in comments if comment]

    # write the input with the cleaned up lines to the output file
    with open(output_file, 'w') as file:
        for line in new_lines:
            file.write(line + '\n')

    # return list of comments for use later
    return comments

# function that looks for keywords in the keyword dictionary, add it to a list
def keywords(input_file):
    # keyword list to store found keywords
    keyword_array = []
    # keyword dictionary to store keywords
    keyword_dictionary = {"def", "print", "return", "range", "for", "in", 'False', "await", "else", "import", "pass", "None", "break", "except", "in", "raise", "True", "class", "finally", "is", "and", "continue", "lambda", "try", "as", "from", "nonlocal", "while","assert", "del", "global", "not", "with", "async", "elif", "if", "or", "yield"}

    # open file, read every line
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # iterate through each line
    for line_number, line in enumerate(lines, start=1):
        # uses regular expression to get words, ignores punctuation
        words = re.findall(r'\b\w+\b', line)

        # check if the word is in the dictionary
        for word in words:
            if word in keyword_dictionary:
                keyword_array.append(word)

    # return list of keywords found
    return keyword_array
                

# function that looks for identifiers in the identifier dictionary, add it to a list
def indentifiers(input_file):
    # identifier list for found identifiers
    identifier_array = []
    # identifier dictionary to store identifiers
    identifier_dictionary = {"add", "result", "a", "b", "greet", "count", "i",}

    # open file, read every line
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # iterate through each line
    for line_number, line in enumerate(lines, start=1):
        # uses regular expression to get words, ignores punctuation
        words = re.findall(r'\b\w+\b', line)

        # check if the word is in the dictionary
        for word in words:
            if word in identifier_dictionary:
                identifier_array.append(word)
    
    # return list of identifiers found
    return identifier_array


# function that looks for operators in the operators dictionary, add it to a list
def operators(input_file):
    # operators list to store found operators
    operator_array = []
    # operators dictionary to hold operators
    operator_dictionary = {"+", "-", "=", "++", "--", "==", "<", ">", "<<", ">>"}

    # open file, read every line
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # iterate through each line
    for line_number, line in enumerate(lines, start=1):
        # check every character in the line if it's in the operator dictionary
        for char in line:
            if char in operator_dictionary:
                operator_array.append(char)
    
    # return list of operators found
    return operator_array


# function that looks for separators in the separators dictionary, add it to a list
def separators(input_file):
    # list of separators found
    separator_array = []
    # separator dictionary to hold separator values
    separator_dictionary = {"(", ")", "[", "]", "{", "}", ".", ":", ","}

    # flag to check if we're inside a string literal
    in_string = False

    # open file, read every line
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # iterate through each line. need to ensure that separators inside of literals are not counted.
    for line_number, line in enumerate(lines, start=1):
        for i, char in enumerate(line):
            # check start or end of a string literal so we can ignore the separators inside of it
            if char == '"' or char == "'":
                in_string = not in_string  # toggle flag
                continue

            # check if char is in separator dictionary and we're not inside a string
            if not in_string and char in separator_dictionary:
                separator_array.append(char)

    # return found separators list
    return separator_array

# function that looks for literals in the literals dictionary, add it to a list
def literals(input_file):
    # list of literals found
    literal_array = []
    # dictionary of literals
    literal_dictionary = {"5", "3", "1", "2", "4,", "5", "6", "7", "8", "9"}

    # Regular expression to find literals enclosed in double quotes
    literal_pattern = r'\"(.*?)\"'

    # Open file and read every line
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # iterate through every line
    for line_number, line in enumerate(lines, start=1):
        # check if literal is in dictionary
        for literal in literal_dictionary:
            if literal in line:
                literal_array.append(literal)

        # find all literals in quotes and add them
        literals_found = re.findall(literal_pattern, line)
        literal_array.extend(literals_found)
    
    # return list of literals
    return literal_array

# function to make the table, add up all the tokens
def makeTable(input_file, output_file):
    comment = clean(input_file, output_file)
    keyword = keywords(output_file)
    keyword_set = set(keyword)  # make a set to remove duplicates
    operator = operators(output_file)
    operator_set = set(operator)
    literal = literals(output_file)
    literal_set = set(literal)
    separator = separators(output_file)
    separator_set = set(separator)
    identifier = indentifiers(output_file)
    identifier_set = set(identifier)
    
    # classified_tokens = keyword_set | operator_set | literal_set | separator_set
    # identifier = []
    # identifier_set = set()
    # with open(output_file, 'r') as file:
    #     lines = file.readlines()

    # for line in lines:
    #     words = re.findall(r'\b\w+\b', line)
    #     for word in words:
    #         if word not in classified_tokens:
    #             identifier.append(word)

    # tally the total tokens (comments not included in token count)
    total = len(keyword) + len(operator) + len(literal) + len(separator) + len(identifier)

    print("Clean Code:")
    with open(output_file, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        print(line, end='')
    
    # print table header
    print("\nCategory       |     Tokens")
    print("---------------|---------------------------------------------")
    
    # print each category if the set has an element
    if keyword_set:
        print(f"Keywords:      | {keyword_set}")
    if identifier_set:
        print(f"Identifiers:   | {identifier_set}")
    if literal_set:
        print(f"Literals:      | {literal_set}")
    if operator_set:
        print(f"Operators:     | {operator_set}")
    if separator_set:
        print(f"Separators:    | {separator_set}")
    if comment:
        print(f"Comments:      | {comment}")
    
    # print total token count
    print(f"Total:         | {total}")
    print("\n")

#run program
test1 = 'test.txt'
output1= 'output.txt'
makeTable(test1, output1)

test2 = 'test2.txt'
output2 = 'output2.txt'
makeTable(test2, output2)

test3 = 'test3.txt'
output3 = 'output3.txt'
makeTable(test3, output3)