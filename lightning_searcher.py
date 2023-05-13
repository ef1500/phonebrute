# Lightning Search
# ef1500
import warnings
import pandas as pd
import itertools
import math
import json
from tabulate import tabulate

warnings.simplefilter(action='ignore', category=FutureWarning)

class LightningSearch:

    def __init__(self, input_number, carrier=None, include_contaminated=False,
                 print_data=True, datafile='./phone_numbers.csv'):
        self.input_number = input_number
        self.carrier = carrier
        self.include_contaminated = include_contaminated
        self.print_data = print_data
        self.datafile = datafile

        if len(self.input_number) != 10:
            raise ValueError(f"Expected a 10 Digit phone number, input was \
                             {len(self.input_number)} chars in length")

        self.input_fs = self.input_number[0:3]
        self.input_ns = self.input_number[3:6]
        self.input_ls = self.input_number[6:]

        # REMAP COLUMN NAMES
        self._new_column_names = ['region','state','NPA','NXX','x','status','code_holder',
                    'contaminated','tn_not_available','rate_center','block_effective_date',
                    'block_available_date','carrier','ocn','date_assigned']

        self._column_dtypes = {
            'region' : str,
            'state' : str,
            'NPA' : str,
            'NXX' : str,
            'x' : str,
            'status' : str,
            'code_holder' : str,
            'contaminated' : str,
            'tn_not_available' : str,
            'rate_center' : str,
            'block_effective_date' : str,
            'block_available_date' : str,
            'carrier' : str,
            'ocn' : str,
            'date_assigned' : str
        }

        # Central dataframe we are going to search through
        self.dataframe = pd.read_csv(self.datafile, names=self._new_column_names, na_values = 'NONE', dtype=self._column_dtypes)

        # Combos generated with the last four digits, if 'X' was present
        self.ls_combos = []
        
    @staticmethod
    def print_dataframe(dataframe, headers=None):
        """Print a dataframe

        Args:
            dataframe (dataframe): dataframe
            headers (list, optional): headers to use. Defaults to None.
        """

        if headers:
            print(tabulate(dataframe, headers=headers, tablefmt='pipe'))
        else:
            print(tabulate(dataframe, headers='keys', tablefmt='pipe'))

    @staticmethod
    def export_to_csv(dataframe, filepath):
        """
        Export the dataframe to a file

        Args:
            dataframe (pd.dataframe): dataframe
            filepath (str): the file to write the csv to
        """
        dataframe.to_csv(filepath, index=False)
        print(f"Successfully exported dataframe to {filepath}")

    @staticmethod
    def export_to_json(dataframe, filepath):
        """
        Export dataframe to JSON file

        Args:
            dataframe (pd.dataframe): DataFrame to export
            file_path (str): File path to save the JSON file
        """
        data_for_writing = dataframe.to_dict(orient='records')
        with open(filepath, 'w', encoding='utf-8') as datafile:
            json.dump(data_for_writing, datafile)
            print(f"Successfully exported dataframe to {filepath}")

    @staticmethod
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

    def generate_last_four_combos(self):
        """
        Generate all combos of the last four digits if there
        is an 'X' present
        """
        if 'X' in self.input_ls:
            self.ls_combos = self.generate_combinations(self.input_ls)

    def generic_dataframe_search(self):
        """
        Search through the CSV and find matching NPA and NXX Values
        """
        fs_matches = self.dataframe['NPA'] == self.input_fs
        ns_matches = self.dataframe['NXX'] == self.input_ns

        # If the input contains 'X', treat it as a wildcard
        if 'X' in self.input_fs:
            possible_values = [self.input_fs.replace('X'*self.input_fs.count('X'), str(i)) for i in range(int(math.pow(10, self.input_fs.count('X'))))]
            fs_matches = self.dataframe['NPA'].isin(possible_values)
        if 'X' in self.input_ns:
            possible_values = [
                self.input_ns.replace('X'*self.input_ns.count('X'), str(i)) for i in range(int(math.pow(10, self.input_ns.count('X'))))]
            ns_matches = self.dataframe['NXX'].isin(possible_values)

        self.dataframe = self.dataframe[fs_matches & ns_matches]
        
        if self.include_contaminated is False:
            non_contaminated_matches = self.dataframe["contaminated"] == "N"
            self.dataframe = self.dataframe[non_contaminated_matches]

    def advanced_dataframe_search(self, column, regex):
        """Advanced Dataframe search

        Args:
            column (str): column to search
            regex (str): regex to match
        """
        # We want to search our new dataframe now
        self.dataframe = self.dataframe[self.dataframe[column].str.contains(regex, na=False)]

    ################################################
    #            Phonebrute Stuff                  #
    ################################################  

    def generate_new_table(self):
        """
        Generate the new table for printing and stuff
        """
        new_table = {}
        headers = ["Phone Number", "state", "NXX", "contaminated", "rate_center",
                    "block_effective_date", "carrier", "date_assigned"]
        
        # Use Seperate Headers so the table output looks nice
        table_headers = ["Phone Number", "State", "NXX", "Contaminated", "Rate Center",
                    "Block Effective Date", "Carrier", "Date Assigned"]

        # Combine NPA and NXX
        self.dataframe['Phone Number'] = self.dataframe['NPA'] + self.dataframe['NXX']

        # Create an empty DataFrame to store the results
        new_table = pd.DataFrame(columns=headers)

        # If no combos were generated, just copy the dataframe
        if len(self.ls_combos) == 0:
            temp_df = self.dataframe.copy()
            temp_df['Phone Number'] = temp_df['Phone Number'] + self.input_ls
            new_table = new_table.append(temp_df, ignore_index=True)
        else:
            # For each combo, append it to the end of the Phone Number and create a new row
            for combo in self.ls_combos:
                temp_df = self.dataframe.copy()
                temp_df['Phone Number'] = temp_df['Phone Number'] + combo
                new_table = new_table.append(temp_df, ignore_index=True)

        # Convert nan to NONE
        new_table.fillna("NONE")

        # Select the necessary columns and reorder them
        new_table = new_table[headers]
        if self.print_data:
            self.print_dataframe(new_table, headers=table_headers)

        return new_table
