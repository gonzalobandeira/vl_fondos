# VL_Fondos

Program to retrieve funds information from Morningstar web-site. 

    *Public project from a private one with more features and analysis.* 

master branch: 
- Version to perform the analysis and scraping using CSV files as outputs to use info with other software.

database branch: 
- Version to perform the analysis and scraping using a MySQL Database in order to save past values. 

### Usage

To use it: 
- add repository to local machine
- add funds name, ISIN, and Morningstar URL to the input/info_fondos.csv file
- run src/main.py and wait for web-scraping to perform data acquisiton

```python
    python main.py 
````

- results should appear in output/info_fondos.csv

### Input

Folder with files with fund information to be retrieve from the web. 
Add name, ISIN and fund website in Morningstar to obtain its data. 

### Output

Folder with files with the fund information retrieved from the web in CSV format. 

### SRC 

Folder with .py files. 

## Libraries 

pandas 
dotenv
sentry_sdk
os
requests
bs4.BeautifulSoup

