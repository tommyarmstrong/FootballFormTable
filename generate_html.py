# Import Libraries
from datetime import datetime
import pandas as pd
import re
from  bs4 import BeautifulSoup

# Functions to clean and present data
#
def bbc_form_summary(form):
  # Function to convert data in "form" string to a simple W, D, L format
  form = re.sub('No Result', '-', form)           # E.g. match abandoned.
  form = re.sub('WResult Win', 'W', form)
  form = re.sub('DResult Draw', 'D', form)
  form = re.sub('LResult Loss', 'L', form)
  return form

def bbc_form_points(form):
  # Function to calculate number of points from the "form" string.
  # Form string is (for example): "WWDLWD"
  form_points = 0
  for result in form:
    if result == 'W':
      form_points = form_points + 3       # Three points for a win
    elif result == 'D':
      form_points = form_points + 1       # One point for a draw
  return form_points

def generate_html(df, league_name, date_string):
  # Function to create HTML of a Pandas DataFrame
  # Returns: String; containing valid HTML

  # Convert dataframe to HTML table using Pandas
  table_html = df.to_html(table_id="formTable", classes='display')

  html = f"""
  <html>
  <header>
      <style>
      body {{
        font-family: Garamond, serif;
      }}
      /* Align h1 and h2 to the left */
      h1, h2 {{
        text-align: left;
      }}
      table {{
        border-collapse: collapse;
        width: 100%;
        font-family: Garamond, serif; /* Garamond with serif as a fallback */
      }}
      th, td {{
        border: 1px solid #ddd;
        padding: 8px;
        text-align: center;
      }}
      tr:nth-child(even) {{
        background-color: #f2f2f2; /* Alternating row colors */
      }}
      th {{
        background-color: #f4f4f4; /* Light gray for header */
        color: black;
        font-weight: bold;
      }}
      /* Align text in the "Team" column to the left */
      .team {{
        text-align: left;
      }}
      /* Hide columns with the "hide-mobile" class on small screens */
      @media only screen and (max-width: 1000px) and (orientation: portrait) {{
        .hide-mobile {{
          display: none;
        }}
        th, td {{
          font-size: calc(2.5vw + 1em); /* Increase text size on smaller screens */
          padding: 10px;
        }}
        h1 {{
          font-size: 80;
        }}
        h2 {{
          font-size: 40;
        }}
      }}
      /* Hide the last column in the table */
      table tr th:last-child,
      table tr td:last-child {{
        display: none;
      }}
    </style>
  </header>
  <body>
    <h1>{league_name}: Form Table</h1>
    <h2>{date_string}</h2>
    {table_html}
    <script>
      // Function to calculate RGB colour based on points
      function getColorBasedOnPoints(points) {{
        const red = Math.min(255, Math.floor((18 - points) * 14)); // More red for lower points
        const green = Math.min(255, Math.floor(points * 14)); // More green for higher points
        return `rgb(${{red}}, ${{green}}, 0)`; // Mix of red and green, no blue
      }}

      // Apply colors to the "Form" column based on the "Form_Points" value
      document.querySelectorAll('#formTable tbody tr').forEach(row => {{
        const pointsCell = row.cells[12]; // Form_Points is in the thirteenth column (index 12)
        const formCell = row.cells[11];  // Form column is in the twelveth column (index 11)
        const points = parseInt(pointsCell.textContent, 10); // Get the points as a number

        const color = getColorBasedOnPoints(points); // Get the corresponding colour
        formCell.style.backgroundColor = color; // Set the background colour
        formCell.style.color = "white"; //Set text colour
      }});
    </script>
  </body>
  </html>
  """

  # Parse the HTML to add classes
  soup = BeautifulSoup(html, "html.parser")

  # Add class="hide-mobile" to header cells for "P", "W", "D", "L", "F", "A", "GD"
  for th in soup.find_all("th"):
    if th.get_text() in ["P", "W", "D", "L", "F", "A", "GD"]:
      th["class"] = th.get("class", []) + ["hide-mobile"]
    if th.get_text() in ["Team"]:
      th["class"] = th.get("class", []) + ["team"]

  # Add class="hide-mobile" to data cells under "P", "W", "D", "L", "F", "A", "GD"
  for tr in soup.find("tbody").find_all("tr"):
    # Get all <td> cells in the row
    tds = tr.find_all("td")
    # Indices of "P", "W", "D", "L", "F", "A", "GD" columns (based on header order)
    for index in [2, 3, 4, 5, 6, 7, 8,]:
      if index < len(tds):  # Ensure index is within range
        tds[index]["class"] = tds[index].get("class", []) + ["hide-mobile"]
    # Add class="team" to team columns
    tds[0]["class"] = tds[0].get("class", []) + ["team"]

  # Return the modified HTML
  return soup.prettify()

# Dictionary to configure URLs for different leagues

# Note: previously the BBC website used different formats ("legacy" and "new").
# Now all leagues seem to consistently use "new" format.

leagues = {
  'English Premier League':
    {
    'url': 'https://www.bbc.co.uk/sport/football/premier-league/table',
    'format': 'new'
    },
  'EFL Championship':
    {
    'url': 'https://www.bbc.co.uk/sport/football/championship/table',
    'format': 'new'
    },
  'EFL League 1':
    {
    'url': 'https://www.bbc.co.uk/sport/football/league-one/table',
    'format': 'new'
    },
  'EFL League 2':
    {
    'url': 'https://www.bbc.co.uk/sport/football/league-two/table',
    'format': 'new'
    },
  'Spanish La Liga':
    {
    'url': 'https://www.bbc.co.uk/sport/football/spanish-la-liga/table',
    'format': 'new'
    },
  'Italian Serie A':
    {
    'url': 'https://www.bbc.co.uk/sport/football/italian-serie-a/table',
    'format': 'new'
    },
  'German Bundesliga':
    {
    'url': 'https://www.bbc.co.uk/sport/football/german-bundesliga/table',
    'format': 'new'
    },
  }

# Set which league to analyse
league_name = 'English Premier League'

# Set the date of the data
formatted_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

# Get the URL and the format used on the BBC website
url = leagues[league_name]['url']
format = leagues[league_name]['format']

# The web page is simple enough to get the data using Pandas
league_table_scrape = pd.read_html(url)
league_table = league_table_scrape[0]

# Format the Form column into simple string of six 'W' 'D' and 'L' characters
if format =='new':
  league_table.rename(columns = {'Form, Last 6 games, Oldest first':'form_long'}, inplace = True)
  league_table['Form'] = league_table.apply(lambda row: bbc_form_summary(row.form_long) , axis=1)

league_table.drop('form_long', axis=1, inplace=True)

# Calculate Form points
league_table['Form_Points'] = league_table.apply(lambda row: bbc_form_points(row.Form) , axis=1)

# Set more standard column names
cols = ['Position', 'Team', 'P', 'W', 'D', 'L', 'F', 'A', 'GD', 'Pts', 'Form', 'Form_Points']
league_table.columns = cols

# Change position of Team and League Position
league_table = league_table[['Team', 'Position', 'P', 'W', 'D', 'L', 'F', 'A', 'GD', 'Pts', 'Form', 'Form_Points']]

# Sort the table on form
form_table = league_table.sort_values(
    by=['Form_Points', 'Team'],
    ascending=[False, True]
).reset_index(drop=True)
form_table.index = form_table.index + 1

# Display the sorted table
form_style = form_table.style.background_gradient(subset='Form_Points', cmap='RdYlGn')
form_style

# Call function to generate HTML and write to file
html = generate_html(form_table, league_name, date_string=formatted_date)
with open('index.html', 'w') as f:
  f.write(html)