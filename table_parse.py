import requests
from bs4 import BeautifulSoup

def fetch_data_from_url(url):
    #fetch the content from the URL
    response = requests.get(url)
    
    if response.status_code == 200:
        #print("url gotten")
        return response.text
    else:
        raise Exception(f"Failed to fetch the document. Status code: {response.status_code}")

def parse_table_from_html(html):
    #parse the HTML using bs4
    soup = BeautifulSoup(html, 'html.parser')
    
    #extract table data
    table = soup.find('table')
    #print(table)
    if not table:
        raise Exception("No table found in the document.")
    
    characters = []
    
    #iterate through each row in the table
    for row in table.find_all('tr'):
        #print(row)
        cells = row.find_all('td')
        #print(cells)
        if len(cells) == 3:
            try:
                #strip inner text and append to characters
                x = int(cells[0].get_text(strip=True))
                char = cells[1].get_text(strip=True)
                y = int(cells[2].get_text(strip=True))
                characters.append((x, char, y))
            except ValueError:
                continue  #skip rows with invalid data
    
    return characters

def create_grid(characters):
    #find the max x and y to determine grid size
    max_x = max(x for x, _, _ in characters)
    max_y = max(y for _, _, y in characters)
    #print(max_x, max_y)

    #fill grid with empty spaces
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    #fill in empty spaces with appropriate characters
    for x, char, y in characters:
        grid[y][x] = char

    return grid

def print_grid(grid):
    #print the grid from top to bottom (row 0 is the topmost)
    for row in reversed(grid):  #reverse the order to print bottom to top
        print(''.join(row))

def display_grid_from_url(url):
    #fetch the data from the URL
    html = fetch_data_from_url(url)
    
    #parse the coordinates and characters from the table in the HTML
    characters = parse_table_from_html(html)
    
    #create a 2D grid of characters
    grid = create_grid(characters)
    
    #print the resulting grid
    print_grid(grid)
