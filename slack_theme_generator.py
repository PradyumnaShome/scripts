import random
import pyperclip

number_of_colors = 8
color_length = 6

color_list = [
    "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(color_length)])
    for i in range(number_of_colors)
]
slack_theme = ','.join(color_list)

print(slack_theme)
pyperclip.copy(slack_theme)
