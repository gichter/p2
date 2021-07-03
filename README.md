
# Webscraping project

This project is a webscraping project using python and BeautifulSoup 4 to scrape books data.

## Installation

clone the project using GitHub CLI

```bash
gh repo clone gichter/p2
```

Open a terminal in the root folder, then create a new virtual environment

```bash
python3 -m venv env
```

Activate the virtual environment
```bash
source env/bin/activate
```

Use the packet manager [pip](https://pip.pypa.io/en/stable/) to install the project dependencies

```bash
pip install -r requirements.txt
```

Launch the script

```bash
python3 webscraping.py
```
## Results

Results folder will appear in the root folder

```bash
/Book Data
    /Category_1
        /category_1.csv
        /image_1.png
        /image_2.png
        /image_3.png
        /image_n.png
    /Category_2    
        /category_2.csv
        /image_1.png
        /image_2.png
        /image_3.png
        /image_n.png
    /Category_3
        /category_3.csv
        /image_1.png
        /image_2.png
        /image_3.png
        /image_n.png
    /Category_n
```
