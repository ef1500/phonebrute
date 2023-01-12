# search through the file
# phonebrute 555XXXXX43 will return a list of all valid phone numbers in that range
import itertools
import pandas as pd

from tabulate import tabulate

def generate_combinations(string) -> list:
    comb = []
    X_indices = [i for i, x in enumerate(string) if x == 'X']
    possible_values = [str(i) for i in range(10)]
    for c in itertools.product(possible_values, repeat=len(X_indices)):
        for i, x in enumerate(X_indices):
            string = string[:x] + c[i] + string[x+1:]
        comb.append(string)
    return comb

def parse_phone(number) -> list:
    return [number[:3], number[3:6], number[6:]]

def join_phone(number) -> str: 
    return ''.join([number[0], number[1], number[2]])

def generate_numbers(phone_number):
    parsed_phone_number = parse_phone(phone_number)
    potential_phone_numbers = []
    if 'X' in parsed_phone_number[0]:
        print('You must specify a valid area code')
        raise ValueError
    else:
        combinations = [generate_combinations(part) if 'X' in part else [part] for part in parsed_phone_number]
        for combination in itertools.product(*combinations):
            potential_phone_numbers.append(list(combination))
    return potential_phone_numbers

def search_database(filename, parsed_phone_numbers, rate_center="ALL", carrier="ALL", include_contaminated=False, noprint_table=False, output="None") -> list:
    """
    Searches a specified CSV file for phone numbers that match the parsed phone numbers,
    and returns a list of valid phone numbers. 
    Optionally, it can also print the valid phone numbers in a table format and/or write the valid
    phone numbers to a specified file.
    The rate center and contaminated numbers can also be filtered.
    
    Parameters:
    - filename (str): The path to the CSV file to be searched.
    - parsed_phone_numbers (list): A list of parsed phone numbers to be searched for
    in the CSV file.
    - rate_center (str, optional): The rate center to filter the phone numbers by. 
    Default is "ALL".
    - include_contaminated (bool, optional): Whether to include contaminated phone numbers in the 
    search results. Default is False.
    - output (str, optional): The path to a file to write the valid phone numbers to. 
    If not provided, the valid phone numbers will not be written to a file.
    
    Returns:
    - valid_phone_numbers (list): A list of valid phone numbers found in the CSV 
    file that match the parsed phone numbers.
    """
    valid_phone_numbers = []
    chunk_iter = pd.read_csv(filename, chunksize=10000) # Read 10000 rows at a time
    table = [] # Create table
    headers = ["Phone Number", "State", "Exchange", "Contaminated", "Rate Center", "Block Avaliable Date", "Carrier", "Date Assigned"] # Create header
    for chunk in chunk_iter:
        for chunk_value in chunk.values:
            for parsed_phone_number in parsed_phone_numbers:
                if chunk_value.tolist()[7] == 'Y' and include_contaminated is False:
                    break # Contaminated Filter
                if rate_center != "ALL" and chunk_value.tolist()[9] not in rate_center:
                    break # Rate Center Filter
                if carrier != "ALL" and carrier not in str(chunk_value.tolist()[12]):
                    break # Carrier Filter
                if chunk_value[2] == int(parsed_phone_number[0]) and chunk_value[3] == int(parsed_phone_number[1]): # Check if there's a phone number in the directory that matches the area code and exchange
                    joined_phone_number = [join_phone(parsed_phone_number)] # Join the parsed phone number together
                    phone_info_list = chunk_value.tolist() # Convert the info to a list
                    important_phone_info_list = [phone_info_list[1], phone_info_list[3], phone_info_list[7], phone_info_list[9], phone_info_list[10], phone_info_list[12], phone_info_list[14]] # Put the important stuff together
                    valid_phone_info = joined_phone_number + important_phone_info_list
                    valid_phone_numbers.append(joined_phone_number + important_phone_info_list) # Add it to the list of valid numbers
                    table.append(valid_phone_info) # Append it to the table
            if chunk_value.tolist()[2] > int(parsed_phone_numbers[-1][0]):
                break
        if len(table) > 0:
            if noprint_table is False:
                print(tabulate(table, headers=headers, tablefmt="pipe")) # Print the table
            if output != "None":
                with open(output, 'w+', encoding='utf-8') as phone_number_file:
                    phone_number_file.write(tabulate(table, headers=headers, tablefmt="pipe"))
                print(f"Wrote {len(valid_phone_info)} numbers to {output}")
            table.clear()
    return valid_phone_numbers # Return this list so if we wanna do something with it

if __name__ == '__main__':
    search_database('phone_numbers.csv', generate_combinations('9706851176'), carrier="VERIZON") 