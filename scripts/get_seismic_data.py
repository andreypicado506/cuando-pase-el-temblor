#!/usr/bin/env python3

import argparse
import requests
from bs4 import BeautifulSoup
from typing import Union, List, Dict, Optional

def get_seismic_data(url: str) -> Union[requests.Response, None]:
    """
    Fetch seismic data from a specified URL using an HTTP GET request.

    :param url: The URL to fetch seismic data from.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response
        else:
            print(f"API request failed with status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error while making API request: {str(e)}")
        return None

def parse_seismic_data(html_content: requests.Response, header_tag: str ='tr', amount_of_rows: int =1) -> List[Dict[str, str]]:
    """
    Parse seismic data from an HTML table and return a list of dictionaries.

    :param html_content: HTML content as a BeautifulSoup object.
    :param header_tag: The HTML tag to match for rows (default is 'tr').
    :param amount_of_rows: The number of rows to parse (default is 1).
    """
    seisms = []
    soup = BeautifulSoup(html_content.text, 'html.parser')
    # Find the first table row (excluding the header row)
    rows = soup.find_all(header_tag, class_='header')[0].find_next(header_tag)
    for row in range(amount_of_rows):
        target_row = rows.contents[row].find_all('td')
        seism = {
            'date': target_row[0].text.strip(),
            'time': target_row[1].text.strip(),
            'magnitude': target_row[2].text.strip()
        }
        seisms.append(seism)
    return seisms

def main() -> List[Dict[str, str]]:
    parser = argparse.ArgumentParser(description="Script that get data from the last earthquake in Costa Rica.")
    parser.add_argument("-u", "--ovsicori-url", type=str, required=True, help="'Sismos Sentidos' table from the OVSICORI website.")

    ovsicori_url = parser.parse_args().ovsicori_url

    html_content = get_seismic_data(ovsicori_url)
    seismic_data = parse_seismic_data(html_content)
    
    return seismic_data

if __name__== "__main__":
    print(main())


