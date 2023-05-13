import argparse
import lightning_searcher
import db_downloader

banner = """
██████╗ ██╗  ██╗ ██████╗ ███╗   ██╗███████╗██████╗ ██████╗ ██╗   ██╗████████╗███████╗
██╔══██╗██║  ██║██╔═══██╗████╗  ██║██╔════╝██╔══██╗██╔══██╗██║   ██║╚══██╔══╝██╔════╝
██████╔╝███████║██║   ██║██╔██╗ ██║█████╗  ██████╔╝██████╔╝██║   ██║   ██║   █████╗  
██╔═══╝ ██╔══██║██║   ██║██║╚██╗██║██╔══╝  ██╔══██╗██╔══██╗██║   ██║   ██║   ██╔══╝  
██║     ██║  ██║╚██████╔╝██║ ╚████║███████╗██████╔╝██║  ██║╚██████╔╝   ██║   ███████╗
╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝
Generate Valid Phone Numbers Using NPA-NXX Databases
https://github.com/ef1500/phonebrute

"""

parser = argparse.ArgumentParser(prog="Phonebrute", description='Generate valid phone numbers with NPA-NXX databases')
parser.add_argument("NUMBER", metavar="NUM", help="Phone number to search for in the database")
parser.add_argument("-nP", "--noprint", default=False, action="store_true", help="Don't print the results in a table")
parser.add_argument("-iC", "--include_contaminated", default=False, action="store_true", help='Include Contaminated Entries')
parser.add_argument("-rC", "--ratecenter", type=str, default="ALL", help="Search For a certain rate center")
parser.add_argument("-c", "--carrier", type=str, default="ALL", help="Search for a certain carrier")
parser.add_argument("-s", "--state", type=str, default="ALL", help="Search for numbers from a specific state by their abbreviation")
parser.add_argument("-o", "--output", default="None", type=str, help="Output file, csv or json")

args = parser.parse_args()
print(banner)
db_downloader.download_and_extract('phone_numbers.csv') #  Download Database First Thing if we don't have it

lightning_search = lightning_searcher.LightningSearch(args.NUMBER, include_contaminated=args.include_contaminated, print_data=not args.noprint)
lightning_search.generate_last_four_combos()
#print(f"[PHONEBRUTE] Generated {len(numbers)} phone numbers")
lightning_search.generic_dataframe_search()
if not args.ratecenter == "ALL":
    lightning_search.advanced_dataframe_search('rate_center', args.ratecenter)
if not args.carrier == "ALL":
    lightning_search.advanced_dataframe_search('carrier', args.carrier)
if not args.state == "ALL":
    lightning_search.advanced_dataframe_search('state', args.state)

valid_numbers = lightning_search.generate_new_table()

if not args.output == "None":
    split_filename = args.output.split('.')
    if split_filename[-1] == "csv":
        lightning_search.export_to_csv(valid_numbers, args.output)
    else:
        lightning_search.export_to_json(valid_numbers, args.output)
