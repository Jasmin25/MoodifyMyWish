# tests/test_app.py
import pandas as pd
from app import max_days_for_month, get_celebrity_trivia

def test_max_days_for_month():
    """
    Test the max_days_for_month function to ensure it returns the correct maximum number of days for various months and years.

    This function tests:
    - February in a leap year
    - February in a non-leap year
    - Months with 30 days
    - Months with 31 days
    """
    # Test for February in a leap year
    assert max_days_for_month(2, 2020) == 29

    # Test for February in a non-leap year
    assert max_days_for_month(2, 2021) == 28

    # Test for months with 30 days
    for month in [4, 6, 9, 11]:
        assert max_days_for_month(month, 2021) == 30

    # Test for months with 31 days
    for month in [1, 3, 5, 7, 8, 10, 12]:
        assert max_days_for_month(month, 2021) == 31



def test_get_celebrity_trivia():
    """
    Test the get_celebrity_trivia function to ensure it returns the correct trivia for a given date.

    This function tests:
    - The correct trivia is returned for the given date
    - An empty string is returned if no celebrities are found
    """

    sample_data = {
        "day": [1, 1, 1],
        "month": [1, 1, 1],
        "name": ["John Doe", "Jane Doe", "Test Celebrity"],
        "birth_year": [1900, 2000, 2010],
        "death_year": [1950, None, None],
        "alive": [False, True, True],
        "trivia": [
            "Sample trivia for John Doe.",
            "Sample trivia for Jane Doe.",
            "Sample trivia for Test Celebrity.",
        ],
    }

    celebrities_df = pd.DataFrame(sample_data)

    # Test that the correct trivia is returned for the given date
    trivia = get_celebrity_trivia(1, 1, celebrities_df)
    expected_trivia = (
        "Test Celebrity (born 2010, still alive): Sample trivia for Test Celebrity.; "
        "Jane Doe (born 2000, still alive): Sample trivia for Jane Doe.; "
        "John Doe (born 1900, died in 1950): Sample trivia for John Doe."
    )

    print("Expected Trivia:", expected_trivia)
    print("Actual Trivia:", trivia)

    assert trivia == expected_trivia

    # Test that an empty string is returned if no celebrities are found
    trivia = get_celebrity_trivia(31, 2, celebrities_df)  # Invalid date
    assert trivia == ""
