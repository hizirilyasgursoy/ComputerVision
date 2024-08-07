import string

dict_char_to_int = {'O': '0',
                    'I': '1',
                    'J': '3',
                    'A': '4',
                    'G': '6',
                    'S': '5',
                    'J': '3'}

dict_int_to_char = {'0': 'O',
                    '1': 'I',
                    '3': 'J',
                    '4': 'A',
                    '6': 'G',
                    '5': 'S',
                    'L': 'T',
                    'I': 'T'}

def check(text):
    
    if len(text) < 4 :
        return False

    if (text[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[0] in dict_char_to_int.keys()) and \
       (text[1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[1] in dict_char_to_int.keys()) and \
       (text[2] in string.ascii_uppercase or text[2] in dict_int_to_char.keys()) and \
       (text[3] in string.ascii_uppercase or text[3] in dict_int_to_char.keys()):
        return True
    else:
        return False

def formatted(text):
    str_list=[]
    for i in text:
        str_list.append(i)
    

    if str_list[0] in dict_char_to_int.keys():
        str_list.insert(0, dict_char_to_int[str_list[0]])
        str_list.pop(1)

    if str_list[1] in dict_char_to_int.keys():
        str_list.insert(1, dict_char_to_int[str_list[1]])
        str_list.pop(2)

    if str_list[2] in dict_int_to_char.keys():
        str_list.insert(2, dict_int_to_char[str_list[2]])
        str_list.pop(3)
    
    if str_list[3] in dict_int_to_char.keys():
        str_list.insert(3, dict_int_to_char[str_list[3]])
        str_list.pop(4)
    if str_list[4] in dict_int_to_char.keys():
        str_list.insert(4, dict_int_to_char[str_list[4]])
        str_list.pop(5)
    text_=''
    for i in str_list:
        text_ += i
    
    return text_

def read(text):
    if check(text):
        return formatted(text)
    return None