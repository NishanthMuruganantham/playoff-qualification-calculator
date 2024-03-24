import numpy as np
import pandas as pd
import requests
from typing import Dict, Union


def get_fixture_for_given_tournament(tournament_id: int) -> pd.DataFrame:
    """
    Fetches fixture data for a given tournament ID.

    Parameters:
        tournament_id (int): The ID of the cricket tournament.

    Returns:
        pd.DataFrame: DataFrame containing match information.
    """

    url = "https://hs-consumer-api.espncricinfo.com/v1/pages/series/schedule"
    params = {'seriesId': tournament_id}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    fixture_data = response_data["content"]["matches"]
    match_list = [_get_match_info(match_data, match_index) for match_index, match_data in enumerate(fixture_data)]

    return pd.DataFrame(match_list)


def _get_match_info(match_data: Dict, match_index: int) -> Dict[str, Union[int, str]]:
    """
    Extracts match information from match data.

    Parameters:
        match_data (Dict): Dictionary containing match data.
        match_index (int): Index of the match.

    Returns:
        Dict[str, Union[int, str]]: Dictionary containing match information.
    """
    team_1_id = match_data["teams"][0]["team"]["id"]
    team_1_name = match_data["teams"][0]["team"]["longName"]
    team_2_name = match_data["teams"][1]["team"]["longName"]

    if match_data["status"] == "RESULT":
        winner_team_id = match_data["winnerTeamId"]
        winning_team_name = team_1_name if team_1_id == winner_team_id else team_2_name
    elif match_data["statusText"] == "Match yet to begin":
        winning_team_name = ""
    elif match_data["status"] == "Live":
        winning_team_name = "Live"
    else:
        winning_team_name = "NO RESULT"

    return {
        "match_number": match_index + 1,
        "team_1": team_1_name,
        "team_2": team_2_name,
        "winner": winning_team_name,
    }
