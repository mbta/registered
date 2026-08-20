"""
Test elyse_read.py
"""

from pathlib import Path
import pandas as pd
from registered import elyse_read

TEST_PATH = Path(__file__).parent / "support" 

T = elyse_read.parse_elyse2('elyse2_test.pdf', input_loc = TEST_PATH, export = False)

def test_columns_parsed():
    """
    Testing that logic is filtering out the header
    (Route/Entry/Front) column from the start of each page
    """
    assert ~(T['Signcode'] == 'Route').any()
    assert ~T['Headsign'].str.contains('Entry').any()
    assert ~T['Headsign'].str.contains('Front').any()

def test_headers_removed():
    """
    Testing that logic is filtering out any rows with 2 blanks / 3
    Rows with these words are blank otherwise Front: , Led 16x160/10
    """
    for word in ['Front:', 'Led 16x160/10']:
        assert ~T['Signcode'].str.contains(word).any()
        assert ~T['Headsign'].str.contains(word).any()

def test_no_blank_headsigns():
    """
    Test that there are no blank headsigns
    """
    assert ~T['Headsign'].isna().any()

def test_type_correct():
    """
    Test that output is a pandas Dataframe
    """
    assert isinstance(T, pd.DataFrame)
