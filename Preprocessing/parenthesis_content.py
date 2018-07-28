import csv
import re


types_of_parenthetical_info = []
types_of_bracketed_info = []
with open('../Input/MS_from_DIAMM_1400to1600.csv') as file:
    for row in csv.reader(file):
        source = row[4]

        # Parenthesis
        parenthesis = re.search(r"\((.*?)\)", source)
        if parenthesis is not None:
            parenthetical_content = re.search(r"\((.*?)\)", source).group(1)
            # print(parenthetical_content)
            if parenthetical_content not in types_of_parenthetical_info:
                types_of_parenthetical_info.append(parenthetical_content)

        # Square brackets
        brackets = re.search(r"\[(.*?)\]", source)
        if brackets is not None:
            bracket_content = re.search(r"\[(.*?)\]", source).group(1)
            # print(bracket_contet)
            if bracket_content not in types_of_bracketed_info:
                types_of_bracketed_info.append(bracket_content)


print('\n\nThe only type of information that was find in parenthesis is:\n')
for info in types_of_parenthetical_info:
    print(info)

print('\n\nThe only type of information that was find in square brackets is:\n')
for info in types_of_bracketed_info:
    print(info)
