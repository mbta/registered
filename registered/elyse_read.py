"""
ELYSE 2 HEADSIGN PDF -> TXT CONVERSION
"""

import os
import pandas as pd
import pdfplumber

def get_delims(text):
    """ 
    Parses through text extracted from pdf, to split into Entry, Route, and Front
    Accounts for blank spaces in "Route" column  
    """
    text_list = text.split(' ', maxsplit = 2)
    if not all(x.isnumeric() for x in text_list[:2]):
        text_list = [text_list[0], None,  ' '.join(text_list[1:])]
    return text_list


def parse_elyse2(file, input_loc, output_loc = None,
                 export = False, output_file_name ='elyse2_headsigns.txt'):
    # Reads in pdf
    """
        Reads in PDF, returns text as a dataframe
            Signcode: unique signcode ID
            Route: Route (may be blank if not listed)
            Headsign: Text of headsign
    """

    pdf = pdfplumber.open(os.path.join(input_loc, file))
    print(f'Reading {file}')

    to_df = []
    for p in pdf.pages:
        # extract text from each page
        extracted = p.extract_text().split('\n')

        # Split text into rows from get_delims function
        extracted = [get_delims(x) for x in extracted
                if x.split(' ')[0] not in ['File:', 'Led']
                and len(x.split(' '))!=1
                and not x.startswith('Entry Route')]
        to_df += extracted

    # Formatting outputs
    elyse2 = pd.DataFrame(to_df)
    elyse2.columns = ['Signcode', 'Route', 'Headsign']

    # Combine route and front
    elyse2['Headsign'] = ((elyse2['Route'] + ' ').fillna('') + elyse2['Headsign'].fillna(''))\
        .str.replace(", ", " | ")

    elyse2 = elyse2[['Signcode', 'Headsign']]
    # Export
    if export:
        output_file = os.path.join(output_loc, output_file_name)
        print(f'exporting file to {output_loc}')
        elyse2.to_csv(output_file, index = False, sep = '\t')

    return elyse2
