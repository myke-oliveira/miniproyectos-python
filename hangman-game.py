#! /usr/bin/python3

from random import sample

hangman_images = ["""
  ___________________
  |                 |
  |
  |
  |
  |
  |
  |
  |""",
  """
  ___________________
  |                 |
  |                 O
  |
  |
  |
  |
  |
  |""",
  """
  ___________________
  |                 |
  |                 O
  |                 |
  |
  |
  |
  |
  |""",
  """
  ___________________
  |                 |
  |                 O
  |               / |
  |
  |
  |
  |
  |""",
  """
  ___________________
  |                 |
  |                 O
  |               / | \ 
  |
  |
  |
  |
  |""",
  """
  ___________________
  |                 |
  |                 O
  |               / | \ 
  |                /
  |
  |
  |
  |""",
  """
  ___________________
  |                 |
  |                 O
  |               / | \ 
  |                / \\
  |
  |
  |
  |"""
]

with open('hangman-words.txt') as txt_file:
    words = [word.strip() for word in txt_file.readlines()]

word = sample(words, 1).pop()
template = '_' * len(word)
print(word)

mistakes = 0

while True:
    print(hangman_images[mistakes])
    print(template)
    if '_' not in template:
        print('You won')
        break

    while True:
        guess = input('Enter your guess: ')
        if len(guess) != 1:
            print('You should guess just one letter.')
        break

    if guess not in word:
        print('you guessed wrong.')
        mistakes += 1

    if mistakes > 6:
        print('you lost.')
        break
    
    template_list = list(template)
    for i, letter in enumerate(word):
        if guess == letter:
            template_list[i] = letter
    template = ''.join(template_list)

