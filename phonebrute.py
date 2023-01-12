import argparse
import searcher
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
parser.add_argument("-o", "--output", default="None", type=str, help="Output file")

args = parser.parse_args()
print(banner)
db_downloader.download_and_extract('phone_numbers.csv') #  Download Database First Thing if we don't have it

numbers = searcher.generate_numbers(args.NUMBER)
print(f"[PHONEBRUTE]: Generated {len(numbers)} phone numbers")
searcher.search_database('phone_numbers.csv', numbers, rate_center=args.ratecenter, carrier=args.carrier,
                         include_contaminated=args.include_contaminated, noprint_table=args.noprint, output=args.output)