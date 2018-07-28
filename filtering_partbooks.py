import csv
import re


# The tags used in DIAMM besides the shelfmark.
# These tags are written in parentheses or brackets and they indicate the partbook.
part_tags = ['1', '2', '3', '4', '5', '6', '7', '8',
             'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII',
             'a', 'b', 'c', 'd', 'e',
             'Discantus', 'Upper Voice', 'Contratenor', 'Superius/Discantus',
             'Tenor', 'Bassus', 'Lower Voice', 'Altus/Contratenor',
             'Altus', 'Discantus/Altus/Tenor', 'Discantus-Bassus',
             'Quintus/Sextus', 'Tenor/Bassus',
             'Sextus', 'Canto', 'Medius', 'Triplex', 'Quintus',
             'Discantus 1', 'Discantus 2', 'Altus 1', 'Altus 2', 'Tenor 1',
             'Tenor 2', 'Bassus 1', 'Bassus 2',
             'Tiple', 'Tenore', 'Basso',
             'C', 'A', 'B', 'T', 'E', 'H', 'Q', 'S', 'i', 'D',
             'Prima Vox', 'Secunda Vox', 'Tertia Vox', 'Quarta Vox',
             'part 1', 'part 2', 'part I']

# Goal: Retrieve all the unique sources by filtering out the partbooks
# (accounting just for one of a set of partbooks, because they all belong to a single source)
unique_sources = []
unique_sources_info = []
with open('./Input/MS_from_DIAMM_1400to1600.csv') as file:

    for item in csv.DictReader(file):
        archive = item['siglum']
        shelfmark = item['shelfmark']
        name_item = archive + " " + shelfmark

        parenthesis = re.search(r".*\((.*?)\)", shelfmark)
        bracket = re.search(r".*\[(.*?)\]", shelfmark)

        # If the item does not have any parenthesis or bracket,
        # Add it to the list of unique_sources since (most probably) is not a partbook
        if parenthesis is None and bracket is None:
            unique_sources.append(name_item)
            unique_sources_info.append(item)
        # In the case that at least one of them (a parenthesis or bracket) is present
        else:
            # 1. Determine the shelfmark

            # If there is a parenthesis
            if parenthesis is not None:
                shelfmark_edit = re.search(r"(.*)\(.*\)", shelfmark).group(1)
                name_item_edit = archive + " " + shelfmark_edit
                embedded_content = parenthesis.group(1)

            # If there is a bracket
            elif bracket is not None:
                shelfmark_edit = re.search(r"(.*)\[.*\]", shelfmark).group(1)
                name_item_edit = archive + " " + shelfmark_edit
                embedded_content = bracket.group(1)

            else:
                print("This shouldn't happen!\nParentheses and brackets at the same time")

            # Determine whether this item is a partbook or not
            if embedded_content in part_tags:
                # If it is a partbook, determine whether the source 
                # is already included in the list of unique_sources
                if name_item_edit in unique_sources:
                    # If it is, pass, don't duplicate the record
                    index = unique_sources.index(name_item_edit)
                    a = unique_sources_info[index]
                    a['part'] = a['part'] + ", " + embedded_content
                else:
                    # If it is not, add the record to the unique_sources without the partbook
                    # number (i.e.. add name_item_edit instead of the original name_item)
                    unique_sources.append(name_item_edit)
                    item['shelfmark'] = shelfmark_edit
                    item['part'] = embedded_content
                    unique_sources_info.append(item)
            else:
                # If it is not a partbook, add the name as it is (name_item)
                unique_sources.append(name_item)
                unique_sources_info.append(item)

print(len(unique_sources))

with open('./Output/unique_polyphonic_ms_sources.csv', 'w') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(['siglum & shelfmark'])
    for source in unique_sources:
        writer.writerow([source])

with open('./Output/unique_polyphonic_ms2_sources.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=['id', 'MS name', 'siglum', 'archive', 'shelfmark', 'other names', 'part'])
    writer.writeheader()
    for source in unique_sources_info:
        writer.writerow(source)
