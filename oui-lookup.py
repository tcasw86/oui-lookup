import csv
import re

def load_oui_data(oui_file):
    """
    Load OUI data from a text file (only base 16 lines) 
    and return a dictionary mapping MAC prefixes to organizations.
    """
    oui_dict = {}
    with open(oui_file, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            match = re.match(r'^([0-9A-Fa-f]{6})\s+\(base 16\)\s+(.*)', line)
            if match:
                mac_prefix, organization = match.groups()
                oui_dict[mac_prefix.upper()] = organization.strip()
    return oui_dict

def normalize_mac(mac_address):
    """
    Normalize MAC address to get the first 6 hexadecimal characters,
    removing any non-hex characters like dots or dashes.
    """
    cleaned = re.sub(r'[^0-9A-Fa-f]', '', mac_address).upper()
    return cleaned[:6]

def get_oui_info(mac_address, oui_dict):
    """
    Get the OUI (manufacturer) for a given MAC address.
    """
    prefix = normalize_mac(mac_address)
    return oui_dict.get(prefix, "Unknown")

def process_csv(input_csv, output_csv, oui_dict):
    """
    Read the CSV, look up MAC addresses from column A (index 0), 
    and write OUI results to column B (index 1).
    """
    with open(input_csv, 'r', encoding='utf-8', newline='') as infile, \
         open(output_csv, 'w', encoding='utf-8', newline='') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        headers = next(reader)

        # Ensure headers has at least 2 columns: MAC Address and OUI
        while len(headers) < 2:
            headers.append('')
        headers[1] = "OUI"
        writer.writerow(headers)

        for row in reader:
            # Ensure the row has at least 2 columns
            while len(row) < 2:
                row.append('')

            mac_address = row[0].strip()
            row[1] = get_oui_info(mac_address, oui_dict)

            writer.writerow(row)

if __name__ == '__main__':
    input_csv = 'input.csv'
    output_csv = 'output_with_oui.csv'
    oui_file = 'oui.txt'

    oui_dict = load_oui_data(oui_file)
    process_csv(input_csv, output_csv, oui_dict)
