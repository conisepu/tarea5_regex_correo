import os
import re


# Handles lines:
def handle_line(line, input_summary):
    input_len = 0

    for char in line:
        input_list = input_summary.get(input_len)
        updated_list = []

        if input_list is not None:
            for item in input_list:
                updated_list.append(item)

        if char != '\n':
            updated_list.append(char)

        if len(updated_list) > 0:
            input_summary[input_len] = updated_list
            input_len += 1

    return input_summary


def simplify(input_summary):
    simplified_summary = {}
    for line in input_summary:
        elements = input_summary[line]
        new_list = []

        for element in elements:
            if new_list is None:
                new_list.append(element)
            else:
                found = 0
                current_list = new_list

                for list_el in current_list:
                    if element == list_el:
                        found = 1

                if found == 0 and element != '\n':
                    new_list.append(element)

        simplified_summary[line] = new_list
    return simplified_summary


def string_helper(character_list):
    threshold = 2
    char_string = ''

    if len(character_list) >= threshold:
        element = character_list[0]

        if element.isdigit():
            char_string = '[0-9]'
        elif element.isupper():
            char_string = '[A-Z]'
        elif element.islower():
            char_string = '[a-z]'
        else:
            char_string = '[-_]'

    elif len(character_list) > 0:
        for character in character_list:
            char_string += character

    return char_string


# if more than certain number of letters/numbers, replace with [a-z] or [0-9]
def vagueify(input_summary):
    for line in input_summary:
        if len(input_summary[line]) > 1:
            numbers = 0
            upperchars = 0
            number_array = []
            upperchar_array = []
            lowerchars = 0
            lowerchar_array = []
            carctEspecial = 0
            carctEspecial_array = []

            for char in input_summary[line]:
                #print(char + "   " + str(char.isalpha()))
                if char.isdigit():
                    numbers += 1
                    number_array.append(char)
                elif char.isalpha():
                    if char.isupper():
                        upperchars += 1
                        upperchar_array.append(char)
                    else:
                        lowerchars += 1
                        lowerchar_array.append(char)
                else:
                    carctEspecial += 1
                    carctEspecial_array.append(char)
                    
            input_summary[line] = []

            nr_ar = string_helper(number_array)
            if len(nr_ar) > 0:
                input_summary[line].append(nr_ar)

            l_ar = string_helper(lowerchar_array)
            if len(l_ar) > 0:
                input_summary[line].append(l_ar)

            u_ar = string_helper(upperchar_array)
            if len(u_ar) > 0:
                input_summary[line].append(u_ar)

            ce_ar = string_helper(carctEspecial_array)
            if len(ce_ar) > 0:
                input_summary[line].append(ce_ar)

    return input_summary


def checkpart(_r1, _r2):
    r1 = _r1.strip('+')
    r2 = _r2.strip('+')

    if (r1 == '[0-9A-Z]' or r1 == '[A-Za-z]') and (r2 == '[A-Z]' or r2 == '[A-Z]+'):
        return True
    elif (r1 == '[0-9A-Z]' or r1 == '[0-9a-z]') and (r2 == '[0-9]' or r2 == '[0-9]+'):
        return True
    elif (r1 == '[A-Za-z]' or r1 == '[0-9a-z]') and (r2 == '[a-z]' or r2 == '[a-z]+'):
        return True
    elif (r1 == '[0-9A-Z]') and (r2.isnumeric() or r2.isupper()):
        return True
    elif (r1 == '[0-9a-z]') and (r2.isnumeric() or r2.islower()):
        return True
    elif (r1 == '[A-Za-z]') and (r2.isupper() or r2.islower()):
        return True
    else:
        return False


# if multiple occurrences of same possibilities right after each other, only add one with a plus
def summarize(vague_summary, helper_list):
    changes = False
    reg_plus = re.compile(r'(.*)[+]')
    pop_these = []

    for line in vague_summary:
        if line > 0:
            val1 = vague_summary[line - 1]
            val2 = vague_summary[line]
            tempval = ''

            if re.match(r'[(]', str(val1)):
                for i in 1, (len(val1) - 1):
                    tempval += val1[i]
                val1 = tempval

            tempval = ''
            if re.match(r'[(]', str(val2)):
                for i in 1, (len(val1) - 1):
                    tempval += val1[i]
                val2 = tempval

            reg_ex1 = ''.join(val1)
            reg_ex2 = ''.join(val2)

            if reg_ex1 == reg_ex2 or reg_ex1 == reg_ex2.strip('+') or reg_ex1.strip('+') == reg_ex2:
                vague_summary[line] = []
                if not re.search(reg_plus, str(vague_summary[line-1])):
                    temp_string = ''.join(vague_summary[line-1])
                    print(temp_string + "aaaaaaaaaaaaaaaaaaaaaa")
                    if temp_string == '[0-9][A-Z]' or temp_string == '[A-Z][0-9]':
                        temp_string = '[0-9A-Z]'
                    elif temp_string == '[0-9][a-z]' or temp_string == '[a-z][0-9]':
                        temp_string = '[0-9a-z]'
                    elif temp_string == '[A-Z][a-z]' or temp_string == '[a-z][A-Z]':
                        temp_string = '[A-Za-z]'
                    if temp_string[-1] != '+':
                        temp_string = temp_string + '+'

                    if len(vague_summary[line - 1]) <= len(temp_string):
                        vague_summary[line - 1] = [temp_string]
                    pop_these.append(line)
                changes = True

            elif checkpart(reg_ex1, reg_ex2):
                temp_string = reg_ex1
                if reg_ex1[-1] != '+':
                    temp_string = temp_string + '+'
                vague_summary[line - 1] = temp_string
                vague_summary[line] = ''
                pop_these.append(line)
                changes = True

    decluttered_list = []
    for element in vague_summary:
        if len(vague_summary[element]) > 0:
            decluttered_list.append(vague_summary[element])

    dictionary = {}
    for i in range(0, len(decluttered_list)):
        dictionary[i] = decluttered_list[i]

    temp_list = []
    for index in range(len(helper_list)):
        if index not in pop_these:
            temp_list.append(helper_list[index])

    return changes, dictionary, temp_list


def create_regex(input_summary, shortest_input_length, helper_list):
    regex = ''
    for line in input_summary:
        elements = input_summary[line]
        
        reg = re.compile(r'[[].*[]]')

        if len(elements) == 1:
            if helper_list[line] < shortest_input_length:
                el = elements[0]
                if len(el) > 1 and el[-1] != ']' and el[-1] != '?' and el[-1] != '+':
                    regex = regex + '[' + elements[0] + ']'
                    
                else:
                    regex = regex + elements[0]
            elif re.search(reg, elements[0]):
                regex += elements[0] + '?'
            else:
                regex = regex + '[' + elements[0] + ']?'

        elif len(elements) > 1:
            tmp = ''
            if elements != "[0-9A-Z]+" and elements != "[0-9a-z]+" and elements != "[A-Za-z]+":
                for element in elements:
                    new_el = element.strip('[]')
                    tmp = tmp + new_el
            else:
                tmp = elements

            if helper_list[line] < shortest_input_length and tmp[-1] != '+':
                regex = regex + '[' + tmp + ']'
            elif helper_list[line] >= shortest_input_length:
                regex = regex + '[' + tmp + ']?'
            else:
                regex = regex + tmp

    return regex


# Main Function
def main():
    input_file = 'msgID_0.txt'
    filepath = os.path.join(os.path.dirname(__file__), input_file)
    f = open(filepath, 'r')

    input_count = 0
    longest_input_len = 0
    shortest_input_len = 0
    input_summary = {}

    for line in f:
        input_summary = handle_line(line, input_summary)
        input_count += 1

    baseline = len(input_summary[0])
    for line in input_summary:
        if len(input_summary[line]) == baseline:
            shortest_input_len += 1
        longest_input_len += 1

    input_summary = simplify(input_summary)
    #hasta aca esta bien
    # print('output #1 = ' + str(input_summary))

    vague_summary = vagueify(input_summary) # comment out code if using exhaustive input
    
    # vague_summary = input_summary # uncomment code if using exhaustive input
    # print('output #2 = ' + str(vague_summary))

    helper_list = list(range(0, len(vague_summary)))

    changes, summarized_summary, helper_list = summarize(vague_summary, helper_list)
    while changes:
        changes, summarized_summary, helper_list = summarize(summarized_summary, helper_list)

    exact_regex = create_regex(summarized_summary, shortest_input_len, helper_list)
    print('regEx = ' + str(exact_regex))

if __name__ == '__main__':
    main()
