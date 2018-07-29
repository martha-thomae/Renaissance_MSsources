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

        # Presence of a parenthesis or square bracket (both are used to indicate the parts)
        parenthesis = re.search(r".*[\[\(](.*?)[\]\)]", shelfmark)

        # If the item does not have any parenthesis or bracket,
        # Add it to the list of unique_sources since (most probably) is not a partbook
        if parenthesis is None:
            unique_sources.append(name_item)
            unique_sources_info.append(item)
        # In the case that at least one of them (a parenthesis or bracket) is present
        else:
            # 1. Determine the shelfmark
            shelfmark_edit = re.search(r"(.*)[\[\(].*[\]\)]", shelfmark).group(1)
            name_item_edit = archive + " " + shelfmark_edit
            embedded_content = parenthesis.group(1)

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

print(len(unique_sources_info))

# Remove/Replace less evident items

# 1. Identify these items
items_to_remove = []
for item in unique_sources_info:
    # Remove Machaut
    if item['id'] == '90':
        items_to_remove.append(item)

    # (Not-so-evident) Partbooks found by JULIE
    # Remove Hammond Partbooks
    elif item['id'] in ['1885', '2982', '2983', '2984', '2985']:
        items_to_remove.append(item)
    # Remove Florence Partbooks (164-7)
    elif item['id'] in ['1407', '2895', '2896', '2897']:
        items_to_remove.append(item)
    # Remove Florence Partbooks (122-5)
    elif item['id'] in ['1778', '2892', '2893', '2894']:
        items_to_remove.append(item)

    # Suspected Parbooks found by MARTHA
    # Remove Sadler Partbooks
    elif item['id'] in ['2272', '2273', '2274', '2275', '2276']:
        items_to_remove.append(item)
    # Remove Wanley Partbooks
    elif item['id'] in ['2291', '2292', '2293']:
        items_to_remove.append(item)
    # Remove Baldwin Partbooks
    elif item['id'] in ['2348', '2349', '2350', '2351', '2352']:
        items_to_remove.append(item)
    # Remove Dow Partbooks
    elif item['id'] in ['2353', '2354', '2355', '2356', '2357']:
        items_to_remove.append(item)
    # Remove duplicate copy of the St Andrews Psalter (or Wode) Partbooks
    # [DB and A (recently discovered, not in CCM)]
    elif item['id'] in ['2886', '2887', '4037']:
        items_to_remove.append(item)
    # Remove the St Andrews Psalter (or Wode) Partbooks
    # [D voice, TB have already been merged with D, but A and Q come from 
    # another library, which is why they have to be manually merged]
    elif item['id'] in ['2883', '1891', '2860']:
        items_to_remove.append(item)

# 2. Actually remove the items
for item in items_to_remove:
    unique_sources_info.remove(item)
print(len(unique_sources_info))

# 3. Add the items that belong to the same set of partbooks as a single item (i.e., a single source)

# (Not-so-evident) Partbooks found by JULIE
# Add one source for the Hammond Partbooks
newitem = {'id': '1885, 2982, 2983, 2984, 2985',
            'MS name': 'London', 
            'siglum': 'GB-Lbl',
            'archive': 'British Library',
            'shelfmark': 'Add. MS 30480, 30481, 30482, 30483, 30484',
            'other names': 'Hammond Partbooks'}
unique_sources_info.append(newitem)
# Add one source for the Florence Partbooks 164-7
newitem = {'id': '1407, 2895, 2896, 2897',
            'MS name': 'Florence (Firenze)', 
            'siglum': 'I-Fn',
            'archive': 'Biblioteca Nazionale Centrale',
            'shelfmark': 'MS Magl. XIX.164, 165, 166, 167',
            'other names': ''}
unique_sources_info.append(newitem)
# Add one source for the Florence Partbooks 122-5
newitem = {'id': '1778, 2892, 2893, 2894',
            'MS name': 'Florence (Firenze)', 
            'siglum': 'I-Fn',
            'archive': 'Biblioteca Nazionale Centrale',
            'shelfmark': 'MS Magl. XIX.122, 123, 124, 125',
            'other names': ''}
unique_sources_info.append(newitem)

# Suspected Parbooks found by MARTHA
# Add one source for the Sadler Partbooks
newitem = {'id': '2272, 2273, 2274, 2275, 2276',
            'MS name': 'Oxford', 
            'siglum': 'GB-Ob',
            'archive': 'Bodleian Library',
            'shelfmark': 'MS. Mus. e. 1, 2, 3, 4, 5',
            'other names': 'Sadler Partbooks'}
unique_sources_info.append(newitem)
# Add one source for the Wanley Partbooks
newitem = {'id': '2291, 2292, 2293',
            'MS name': 'Oxford', 
            'siglum': 'GB-Ob',
            'archive': 'Bodleian Library',
            'shelfmark': 'MS. Mus. Sch. e. 420, 421, 422',
            'other names': 'Wanley Partbooks'}
unique_sources_info.append(newitem)
# Add one source for the Baldwin Partbooks
newitem = {'id': '2348, 2349, 2350, 2351, 2352',
            'MS name': 'Oxford', 
            'siglum': 'GB-Och',
            'archive': 'Christ Church',
            'shelfmark': 'Mus. 979, 980, 981, 982, 983',
            'other names': 'Baldwin Partbooks'}
unique_sources_info.append(newitem)
# Add one source for the Dow Partbooks
newitem = {'id': '2353, 2354, 2355, 2356, 2357',
            'MS name': 'Oxford', 
            'siglum': 'GB-Och',
            'archive': 'Christ Church',
            'shelfmark': 'Mus. 984, 985, 986, 987, 988',
            'other names': 'Dow Partbooks'}
unique_sources_info.append(newitem)
# Add one source for the duplicate copy of St Andrews Psalter (or Wode) Partbooks
# [DB and A (recently discovered, not in CCM)]
newitem = {'id': '2886, 2887, 4037',
            'MS name': 'Edinburgh / Washington', 
            'siglum': 'GB-Eu / US-Wgu',
            'archive': 'University Library / Georgetown University Special Collections Joseph Mark Lauinger Library',
            'shelfmark': 'MS Dk.5.14, 5.15 / MS 10',
            'other names': 'St. Andrews Psalter or Wode Partbooks'}
unique_sources_info.append(newitem)
# Add one source for the St Andrews Psalter (or Wode) Partbooks
# [DTB, A, and Q]
newitem = {'id': '2883, 2884, 2885, 1891, 2860',
            'MS name': 'Edinburgh / London / Dublin', 
            'siglum': 'GB-Eu / Gb-Lbl / IRL-Dtc',
            'archive': 'University Library / British Library / Trinity College Library',
            'shelfmark': 'MS La III. 483 (a), (b), (c) / Add. MS 33933 / MS 412',
            'other names': 'St. Andrews Psalter or Wode Partbooks',
            'part': ''}
unique_sources_info.append(newitem)

# Write output file
with open('./Output/unique_polyphonic_ms2_sources.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=['id', 'MS name', 'siglum', 'archive', 'shelfmark', 'other names', 'part'])
    writer.writeheader()
    for source in unique_sources_info:
        writer.writerow(source)
