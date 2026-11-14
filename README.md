# HW3: Tennis Career Package

## About

This repository contains a Python package for retrieving a professional tennis player's career match data from Tennis Abstract and creating a scatter plot similar to the visualization from HW2.

The package is designed to work for different players rather than only one specific player. It handles both male and female Tennis Abstract career files, even though those files store opponent age information differently.

## Public Functions

The package has two main public functions:

- `get_career_matches()` downloads and processes a player's Tennis Abstract career data into a clean pandas DataFrame
- `plot_age_difference()` creates a scatter plot showing the player's age against the difference between the player's age and the opponent's age

## Installation

Install directly from GitHub:

~~~bash
pip install git+https://github.com/UCB-stat159-f26/hw03-2-knnrd.git
~~~

## Usage

~~~python
from tennis_age import get_career_matches, plot_age_difference

serena = get_career_matches("Serena Williams")
plot_age_difference(serena)

nadal = get_career_matches("Rafael Nadal")
plot_age_difference(nadal)
~~~

Player names can be entered with spaces, different capitalization, or without spaces.

For example:

~~~python
get_career_matches("serena williams")
get_career_matches("SerenaWilliams")
get_career_matches("Rafael Nadal")
get_career_matches("RafaelNadal")
~~~

If the player cannot be found on Tennis Abstract, the function raises a meaningful `ValueError`.

Example:

~~~python
get_career_matches("Gaston Sanchez")
~~~

## Returned Data

`get_career_matches()` returns a pandas DataFrame with the following columns:

- `date_match` — date of the match
- `tournament` — tournament name
- `surface` — court surface
- `age_player` — player's age at the time of the match
- `age_opponent` — opponent's age at the time of the match
- `age_diff` — player age minus opponent age
- `opponent` — opponent's name
- `result` — whether the player won or lost

`age_diff` is calculated as:

`player age - opponent age`

A negative `age_diff` means the opponent was older than the player. A positive value means the player was older than the opponent.

## Male and Female Career Files

Tennis Abstract stores opponent age information differently for male and female players.

For female-player career files, the opponent's date of birth is provided. The package uses this birth date and the match date to calculate the opponent's age.

For male-player career files, the opponent's age is already included directly in the data.

The package recognizes these two cases and processes both formats into the same cleaned DataFrame structure.

## Plot

`plot_age_difference()` takes the cleaned DataFrame returned by `get_career_matches()` and creates a scatter plot similar to the visualization used in HW2.

The plot uses:

- x-axis: player's age
- y-axis: player's age minus opponent's age
- point color: win or loss result

A horizontal line at zero separates matches against older opponents from matches against younger opponents.

## Tests

The automated tests do not make requests to the live Tennis Abstract website.

Instead, the tests use the mock male and female Career JS examples provided in the assignment. This keeps automated tests independent of the live website and avoids issues with availability or rate limiting.

Run the tests with:

~~~bash
pytest -v
~~~

The tests cover:

- player-name normalization
- invalid or empty player names
- parsing Tennis Abstract JS data
- female-player opponent age calculations
- male-player opponent age handling
- cleaned DataFrame creation
- win/loss processing
- plotting behavior

## Repository Structure

~~~text
.
├── pyproject.toml
├── README.md
├── instructions.md
├── src/
│   └── tennis_age/
│       ├── __init__.py
│       ├── career.py
│       └── plotting.py
└── tests/
    ├── conftest.py
    ├── test_career.py
    └── test_plotting.py
~~~

### `src/tennis_age/`

Contains the Python package.

- `career.py` handles player-name normalization, downloading Tennis Abstract data, parsing JS files, player and opponent age calculations, and the public `get_career_matches()` function
- `plotting.py` contains the public `plot_age_difference()` function
- `__init__.py` exposes the package's public functions

### `tests/`

Contains the automated tests.

- `conftest.py` contains mock male and female Tennis Abstract JS fixtures
- `test_career.py` tests parsing, age calculations, and data processing
- `test_plotting.py` tests the plotting function

## Reflection

This assignment helped me understand the difference between writing a script for one specific analysis and building a package that should work for different users and inputs.

In HW2, I only needed to process Serena Williams's career data. For HW3, I had to separate the workflow into smaller reusable parts for downloading data, parsing the JS files, cleaning the results, calculating ages, and plotting. This made the code more modular and made it easier to test individual pieces separately.

The difference between male and female Tennis Abstract career files was also important. Female-player files contain opponent birth dates, while male-player files already contain opponent ages. I learned that when working with real data, two files that look like they contain the same type of information can still require different processing steps.

I also got more practice writing automated tests that do not depend on a live website. Using mock JS content makes the tests faster and more reproducible because they do not depend on Tennis Abstract being available during testing.

Another thing I learned was how important error handling is when creating a package for other users. While testing the package with real players, Tennis Abstract sometimes rate limited requests. Handling request failures and trying alternate player-page endpoints made the package more reliable and gave me more experience dealing with issues that can happen when working with external websites and APIs.

Overall, this assignment helped me understand package structure, public and private functions, automated testing, reusable code, and how to make an analysis workflow work for more than one specific example.
