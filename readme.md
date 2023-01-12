# Phonebrute
After Martin Virgo's [Phonerator](https://www.martinvigo.com/tools/phonerator) went down, I decided to write my own implementation.
This tool generates valid phone numbers using the NPA-NXX Databases from the US Government. Therefore, this tool will only work with US Numbers only.

## Usage & Installation
To get started, simply clone the repository and run
`pip install -r requirements.txt`

After that finishes, go ahead and run
`python phonebrute.py -h` to show all of the options.

```
>python phonebrute.py -h
usage: Phonebrute [-h] [-p] [-iC] [-rC RATECENTER] [-c CARRIER] [-o OUTPUT] NUM

Generate valid phone numbers with NPA-NXX databases

positional arguments:
  NUM                   Phone number to search for in the database

optional arguments:
  -h, --help            show this help message and exit
  -p, --print           Print the results in a table
  -iC, --include_contaminated
                        Include Contaminated Entries
  -rC RATECENTER, --ratecenter RATECENTER
                        Search For a certain rate center
  -c CARRIER, --carrier CARRIER
                        Search for a certain carrier
  -o OUTPUT, --output OUTPUT
                        Output file
```

Example:
![Example](https://files.catbox.moe/783xh3.gif)

## Features
- Filter by Rate Center (use the -rC option)
- Filter by Carrier (use the -c option)
- Output to a text file (use the -o option)
- Include contaminated Entries (use the -iC option)
- Don't print to the terminal (use the -nP option)
