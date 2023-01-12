# Phonebrute
After Martin Virgo's [Phonerator](https://www.martinvigo.com/tools/phonerator) went down, I decided to write my own implementation.
This tool generates valid phone numbers using the NPA-NXX Databases from the US Government. Therefore, this tool will only work with US Numbers only.

## Usage & Installation
To get started, simply clone the repository and run
`pip install -r requirements.txt`

After that finishes, go ahead and run
`python phonebrute.py -h` this should show you all of the options.

Example:
![Example](https://files.catbox.moe/783xh3.gif)

## Features
- Filter by Rate Center (use the -rC option)
- Filter by Carrier (use the -c option)
- Output to a text file (use the -o option)
- Include contaminated Entries (use the -iC option)
- Don't print to the terminal (use the -nP option)