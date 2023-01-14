# search through the file
# phonebrute 555XXXXX43 will return a list of all valid phone numbers in that range
import itertools
import pandas as pd

from tabulate import tabulate

def generate_combinations(string) -> list:
    """Generate all possible combinations
    for 'X' in a phone number 

    Args:
        string (string): partial number ex: 9XX or 60X

    Returns:
        list: all possible combos
    """
    comb = []
    X_indices = [i for i, x in enumerate(string) if x == 'X']
    possible_values = [str(i) for i in range(10)]
    for c in itertools.product(possible_values, repeat=len(X_indices)):
        for i, x in enumerate(X_indices):
            string = string[:x] + c[i] + string[x+1:]
        comb.append(string)
    return comb

def parse_phone(number) -> list:
    """Parse Phone Number

    Args:
        number (string): Phone number to split

    Returns:
        list: split phone number
    """
    return [number[:3], number[3:6], number[6:]]

def join_phone(number) -> str:
    """Join the phone number parts

    Args:
        number (list): parsed phone number

    Returns:
        str: returns a readable phone number
    """
    return ''.join([number[0], number[1], number[2]])

def generate_numbers(phone_number) -> list:
    """Generate partial phone numbers

    Args:
        phone_number (string): Partial phone number

    Raises:
        ValueError: Raises a valueerror if you try
        to brute force an area code.

    Returns:
        _type_: list
    """
    parsed_phone_number = parse_phone(phone_number)
    potential_phone_numbers = []
    if 'X' in parsed_phone_number[0]:
        print('You must specify a valid area code')
        raise ValueError
    else:
        combinations = [generate_combinations(part) if 'X' in part else [part] for 
                        part in parsed_phone_number]

        for combination in itertools.product(*combinations):
            potential_phone_numbers.append(list(combination))
    return potential_phone_numbers

def search_database(filename, parsed_phone_numbers, rate_center="ALL", carrier="ALL", 
                    include_contaminated=False, noprint_table=False, output="None") -> list:
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
    # Create variable for the phone numbers
    valid_phone_numbers = []
    # Rename the column names so they're easier to query
    new_column_names = ['region','state','npa','nxx','x','status','code_holder',
                        'contaminated','tn_not_available','rate_center','block_effective_date',
                        'block_available_date','carrier','ocn','date_assigned']

    chunk_iter = pd.read_csv(filename, names=new_column_names, 
                             na_values = 'NONE', chunksize=10000) # Read 10000 rows at a time
    table = [] # Create table
    headers = ["Phone Number", "State", "Exchange", "Contaminated", "Rate Center",
               "Block Avaliable Date", "Carrier", "Date Assigned"] # Create header
    for chunk in chunk_iter:
        # Fill any exchanges not issued yet with "None"
        chunk = chunk.fillna("NONE")
        for parsed_phone_number in parsed_phone_numbers:
            # Query for when both the NPA and the NXX numbers are equal to one another
            db_query = chunk.query(f'npa=={int(parsed_phone_number[0])} & nxx=={int(parsed_phone_number[1])}')
            # Make sure we're not operating on an empty set
            if not db_query.empty:
                # Check if the include contaminated argument is True
                if include_contaminated is True:
                    # If it's true, then query for when both Y and N are present
                    db_query = db_query.query('contaminated=="Y" | contaminated == "N"')
                # If include contaminated is False, just query normally
                if include_contaminated is False:
                    db_query = db_query.query('contaminated=="N"')
                # Check if a Rate Center is specified
                if rate_center != "ALL":
                    # Query for when the rate center column contains the rate center
                    # Use the python engine here because according to stack overflow
                    # The numbexpr engine doesn't allow this.
                    db_query = db_query.query(f'rate_center.str.contains("{rate_center}")',
                                              engine='python')
                # Check if a carrier is specified
                if carrier != "ALL":
                    # Same thing here as before, query for when the carrier
                    # Is in the string, again using the python engine
                    db_query = db_query.query(f'carrier.str.contains("{carrier}")',
                                              engine='python')
                # Now Make the table data
                for db_values in db_query.values:
                    # Convert the DataFrame into a list
                    phone_info_list = db_values.tolist()
                    # Make a list of only the important things that we want,
                    # Otherwise, the terminal gets cluttered
                    important_phone_info_list = [join_phone(parsed_phone_number),
                                                 phone_info_list[1], phone_info_list[3],
                                                 phone_info_list[7], phone_info_list[9],
                                                 phone_info_list[10], phone_info_list[12],
                                                 phone_info_list[14]]
                    # Make Sure that we aren't adding duplicates
                    if important_phone_info_list not in valid_phone_numbers:
                        # Add this information to the valid phone number list
                        # Which is what we will be returning
                        valid_phone_numbers.append(important_phone_info_list)
                        # Extend the table list with the phone info we put in the list
                        table.append(important_phone_info_list)

    # Check that we aren't working with an empty table
    if len(table) > 0:
        # Check if the noprint argument is present
        if noprint_table is False:
            # If it's not present, we're good to print the table on the terminal
            print(tabulate(table, headers=headers, tablefmt="pipe")) # Print the table
        # If an output file is specified
        if output != "None":
            # Create a file for the output
            with open(output, 'w+', encoding='utf-8') as phone_number_file:
                # Write the phone number data to the file
                phone_number_file.write(tabulate(table, headers=headers, tablefmt="pipe"))
            # Print to the terminal how much was written
            print(f"Wrote {len(valid_phone_numbers)} numbers to {output}")
        # Clear the table
        table.clear()
    # Return the list of valid phone numbers for integration with other programs
    return valid_phone_numbers # Return this list so if we wanna do something with it
