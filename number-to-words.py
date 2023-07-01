#! /usr/bin/python3
from math import ceil

def main():
    number = input('Introduzca un número: ')
    words = number_to_words(number)
    print(words)

def number_to_words(number_as_string):
    digits = list(number_as_string)
    three_digits_group_count = ceil(len(digits) / 3)
    missing_digits_count = three_digits_group_count*3 - len(digits)
    digits = ['0' for _ in range(missing_digits_count)] + digits

    if all(map(lambda digit: digit == '0', digits)):
        return 'cero'

    three_digits_groups = [digits[3*i: 3*i+3] for i in range(three_digits_group_count)]
    
    GROUP_SULFIX = (
        '',
        'mil',
        ('millón', 'millónes'),
        'mil millónes',
        ('billón', 'billónes'),
        'mil billónes',
        ('trillón', 'trillónes'),
        'mil trillónes'
    )
    
    word = ''
    for i, three_digit_group in enumerate(three_digits_groups, start=1):
        hundreds, tens, units = three_digit_group
        exponent = len(three_digits_groups) - i
        singular = hundreds == tens == '0' and units == '1';

        if not isinstance(GROUP_SULFIX[exponent], tuple):
            sulfix = GROUP_SULFIX[exponent]
        elif singular:
            sulfix = GROUP_SULFIX[exponent][0]
        else:
            sulfix = GROUP_SULFIX[exponent][1]

        group_word = three_digits_group_to_word(three_digit_group);
        
        if units == '1' and tens != '1' and exponent != 0:
            group_word = group_word[0: -1]
        
        word += ' ' + group_word + ' ' + sulfix
    
    return word

def three_digits_group_to_word(three_digits_group):
    UNIT_NAMES = {
        '0': '',
        '1': 'uno',
        '2': 'dos',
        '3': 'tres',
        '4': 'cuatro',
        '5': 'cinco',
        '6': 'seis',
        '7': 'siete',
        '8': 'ocho',
        '9': 'nueve'
    }

    TEN_NAMES = {
        '0': '',
        '1': 'diez',
        '2': 'veinte',
        '3': 'treinta',
        '4': 'cuarenta',
        '5': 'cincuenta',
        '6': 'sesenta',
        '7': 'setenta',
        '8': 'ochenta',
        '9': 'noventa'
    }

    HUNDRED_NAMES= {
        '0': '',
        '1': 'ciento',
        '2': 'doscientos',
        '3': 'trescientos',
        '4': 'cuatrocientos',
        '5': 'quinientos',
        '6': 'seiscientos',
        '7': 'setecientos',
        '8': 'ochocientos',
        '9': 'novecientos'
    }

    TEN_TO_TWENTY_NINE_NAMES = {
        '10': 'diez',
        '11': 'once',
        '12': 'doce',
        '13': 'trece',
        '14': 'catorce',
        '15': 'quince',
        '16': 'dieciséis',
        '17': 'diecisiete',
        '18': 'dieciocho',
        '19': 'diecinueve',
        '20': 'veinte',
        '21': 'veintiuno',
        '22': 'veintedós',
        '23': 'veintitrés',
        '24': 'veinticuatro',
        '25': 'veinticinco',
        '26': 'veintiséis',
        '27': 'veintisiete',
        '28': 'veintiocho',
        '29': 'veintenueve',
    }

    hundreds, tens, units = three_digits_group
    
    if hundreds == tens == '0':
        return UNIT_NAMES[units]
    
    if tens == units == '0':
        if hundreds == '1':
            return 'cien'
        return HUNDRED_NAMES[hundreds]

    if tens == '1' or tens == '2':
        return ' '.join((HUNDRED_NAMES[hundreds], TEN_TO_TWENTY_NINE_NAMES[tens+units]))
    
    return ' '.join((HUNDRED_NAMES[hundreds], TEN_NAMES[tens], 'y', UNIT_NAMES[units]))

if __name__ == '__main__':
    main()