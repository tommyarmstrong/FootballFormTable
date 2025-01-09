# Football Form Table

This is a small pet project to automate a "Form Table" for English Premier League football teams and present it online. It is useful, as a football fan, to be able to quickly check which teams are in good or poor form.

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Availability](#availability)
- [Google Colab Notebook](#google-colab-notebook)
- [Local Installation and Usage](#local-installation-and-usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)


## Description

The aim was to create a table of all the teams in the league, sorted on recent form, and make available over the internet, for personal use. 

The project:
- Scrapes generaly available data on a daily basis.
- Constructs a "Form Table" rendered as HTML.
- Commits the HTML to GitHub daily.
- Serves the HTM as a simple static web page using Github Pages.

## Features 

- The table is sorted on form over each club's most recent six results.
- The table uses colour coded according to good (green) and poor (red) form.
- The table renders according to screen size and orientation (i.e. viewable in phone or laptop).
- The code is configurable for EPL, EFL, La Liga, Serie A and Bundesliga leagues.
- The Github deployment refreshes the form table daily at 22:30 UTC.

## Availability

The table can be accessed in a browser from https://tommyarmstrong.github.io/FootballFormTable/.

## Google Colab Notebook

The code was developed in a Google Colab Notebook. This notebook is available in the repository as `Football_Form_Tables.ipynb`.

This notebook can be opened in Google Colab from: https://colab.research.google.com/github/tommyarmstrong/FootballFormTable/blob/main/Football_Form_Tables.ipynb.


## Local Installation and Usage

### Installation

To set up the project locally, follow these steps:

1. Clone the repository:
  ```bash
  git clone https://github.com/tommyarmstrong/footballformtable.git
  cd your-repository
  ```

2. (Optional) Create a virtual environment using conda or venv:
```bash
conda create --name footballformtable
conda activate footballformtable
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

### Usage

To create the Form Table as an HTML file, run the `generate_html.py` script:

```bash
python generate_html.py
```

The file `index.hmtl` can be viewed in a browser or served by a webserver.

### Changing the League Configuration 

By default the script generates a form table for the English Premier League. To generate a form table for a different league edit the `generate_html.py` script and modify the line:

```bash
# Set which league to analyse
league_name = 'English Premier League'
```

For example to generate a table for the German Bundesliga, modify the script as:
```bash
# Set which league to analyse
league_name = 'German Bundesliga'
```

Then re-run the script.

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository.

2. Create a new branch:
```bash
git checkout -b feature-name
```

3. Make your changes and commit them:
```bash
git commit -m "Add a new feature"
```

4. Push to your branch:
```bash
git push origin feature-name
```

5. Open a pull request.

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).

You are free to use, modify, and distribute this software, provided that any derivative work is also licensed under the GPLv3. See the [LICENSE](LICENSE) file for detailed terms and conditions.

For more information about the GPLv3, visit the official [GNU licenses page](https://www.gnu.org/licenses/gpl-3.0.en.html).


## Acknowledgements

The data used to populate the Form Table is taken from the [BBC Sport](https://www.bbc.co.uk/sport/football) website.




   

