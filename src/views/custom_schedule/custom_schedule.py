from typing import List, Dict
import streamlit as st
import pandas as pd
import time
from points_table_simulator.points_table_simulator import PointsTableSimulator
from points_table_simulator.exceptions import InvalidColumnNamesError, InvalidScheduleDataError, NoQualifyingScenariosError


session_state = {
    "column_name_input_form_submitted": False,
    "generate_qualification_scenarios_inputs_submitted": False,
}

def _apply_banner_styles():
    """Apply custom CSS styles to the banner."""
    st.markdown(
        """
        <style>
            .banner {
                background-color: #4CAF50;
                padding: 40px 20px;
                text-align: center;
                margin-bottom: 30px;
                border-radius: 10px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            }
            .title {
                color: white;
                font-size: 36px;
                font-weight: bold;
                margin-bottom: 20px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            }
            .subtitle {
                color: white;
                font-size: 28px;
                margin-bottom: 20px;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
            }
            .description {
                color: white;
                font-size: 20px;
                line-height: 1.5;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def _create_banner():
    """Display the banner with title and description."""
    st.markdown(
        """
        <div class="banner">
            <div class="title">🏆⚽ Qualification Scenario Generator ⚽🏆</div>
            <div class="subtitle">📊 Calculate qualification scenarios for your own tournament fixture 📊</div>
            <p class="description">📂 Upload your tournament fixture and calculate the various possible qualification scenarios for your favorite team 📈</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def _create_column_name_inputs_form() -> Dict[str, str]:
    """Create form inputs for custom column names."""
    st.markdown(
        """
        <div style="margin-bottom: 20px;">
            <p style="font-size: 18px; font-style: italic; color: #4CAF50;">Please enter the names for the respective columns in your fixture if they are different from the below defaults</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")

    input_column_1, input_column_2, input_column_3, input_column_4 = st.columns(4, gap="small")
    home_team_column_name = input_column_1.text_input("Home team column name", value="Home")
    away_team_column_name = input_column_2.text_input("Away team column name", value="Away")
    winner_team_column_name = input_column_3.text_input("Winner team column name", value="Winner")
    match_number_column_name = input_column_4.text_input("Match number column name", value="Match No")

    input_column_5, input_column_6, input_column_7 = st.columns(3, gap="small")
    points_for_a_win = input_column_5.number_input("Points for a win", min_value=1, value=2)
    points_for_a_draw = input_column_6.number_input("Points for a draw", min_value=0, value=1)
    points_for_a_no_result = input_column_7.number_input("Points for a no result", min_value=0, value=1)

    st.write("")

    return {
        "home_team_column_name": home_team_column_name,
        "away_team_column_name": away_team_column_name,
        "winner_team_column_name": winner_team_column_name,
        "match_number_column_name": match_number_column_name,
        "points_for_a_win": points_for_a_win,
        "points_for_a_draw": points_for_a_draw,
        "points_for_a_no_result": points_for_a_no_result,
    }

def _display_given_fixture_and_current_points_table(current_points_table: pd.DataFrame, remaining_fixture: pd.DataFrame):
    """Display the given fixture and current points table."""
    with st.expander("**Click here to expand given fixture and current points table**"):
        schedule_df_column, points_table_df_column = st.columns(2, gap="small")
        schedule_df_column.markdown("Remaining Fixture")
        schedule_df_column.dataframe(remaining_fixture, hide_index=True)
        points_table_df_column.markdown("Current Points Table")
        points_table_df_column.dataframe(current_points_table, hide_index=True)

def _display_qualification_scenarios(
    list_of_points_tables: List[pd.DataFrame], list_of_qualification_scenarios: List[pd.DataFrame], selected_team: str
):
    """Display the qualification scenarios."""
    for scenario_no, (points_table, schedule) in enumerate(zip(list_of_points_tables, list_of_qualification_scenarios)):
        with st.expander(f"**Click here to expand qualification scenario {scenario_no + 1}**"):
            st.write("")
            st.markdown(f"<h3 style='color: #1e90ff;'>Qualification Scenario {scenario_no + 1}:</h3>", unsafe_allow_html=True)
            st.write("")
            qualification_fixture_column, qualification_points_table_column = st.columns(2, gap="small")
            qualification_fixture_column.markdown("<p style='font-weight: bold; color: #4CAF50;'>Remaining Fixture Favourable Outcome</p>", unsafe_allow_html=True)
            qualification_fixture_column.dataframe(
                schedule.style.apply(
                    lambda row: [
                        'background-color: CornflowerBlue;' if row[
                            session_state["away_team_column_name"]
                        ] == selected_team or row[
                            session_state["home_team_column_name"]
                        ] == selected_team else '' for _ in row
                    ],
                    axis=1
                ),
                hide_index=True
            )
            qualification_points_table_column.markdown("<p style='font-weight: bold; color: #4CAF50;'>Points Table</p>", unsafe_allow_html=True)
            qualification_points_table_column.dataframe(
                points_table.style.apply(
                    lambda row: ['background-color: CornflowerBlue;' if row["team"] == selected_team else '' for _ in row],
                    axis=1
                ),
                hide_index=True
            )
            time.sleep(1)

def _get_inputs_to_generate_qualification_scenarios(points_table_simulator: PointsTableSimulator) -> Dict[str, int]:
    """Get inputs to generate qualification scenarios."""
    selected_team = st.selectbox(
        label="Select Team to generate qualification scenarios",
        options=points_table_simulator.available_teams_in_fixture,
        help="Select the team you want to generate the qualification scenarios",
    )
    input_column_1, input_column_2 = st.columns(2, gap="small")
    expected_position_in_the_points_table = input_column_1.number_input(
        "Your expected position in the points table",
        max_value=len(points_table_simulator.current_points_table) + 1,
        min_value=1,
        value=4,
    )
    number_of_qualification_scenarios = input_column_2.number_input(
        "Number of qualification scenarios to generate",
        max_value=10,
        min_value=1,
        value=4,
        help="Select the number of qualification scenarios you want to generate",
        key="number_of_qualification_scenarios"
    )
    return {
        "selected_team_to_generate_qualification_scenarios": selected_team,
        "expected_position_in_the_points_table": expected_position_in_the_points_table,
        "number_of_qualification_scenarios": number_of_qualification_scenarios,
    }

def simulate_the_qualification_for_custom_schedule():
    """Main function to simulate qualification scenarios for a custom schedule."""
    _apply_banner_styles()
    _create_banner()
    fixture = st.file_uploader("Upload the CSV file", type="csv", key="file_uploader", accept_multiple_files=False, help="Please upload your tournament fixture file in CSV format.")

    if fixture:
        with st.form(key="column_name_inputs_form", clear_on_submit=True):
            column_name_inputs = _create_column_name_inputs_form()
            column_name_inputs_form_submit_button_clicked = st.form_submit_button("Submit")

        if column_name_inputs_form_submit_button_clicked:
            session_state["column_name_input_form_submitted"] = True
            session_state.update(column_name_inputs)

        if session_state["column_name_input_form_submitted"]:
            st.write("")
            uploaded_fixture_df = pd.read_csv(fixture)
            try:
                points_table_simulator = PointsTableSimulator(
                    tournament_schedule=uploaded_fixture_df,
                    points_for_a_win=session_state["points_for_a_win"],
                    tournament_schedule_away_team_column_name=session_state["away_team_column_name"],
                    tournament_schedule_home_team_column_name=session_state["home_team_column_name"],
                    tournament_schedule_winning_team_column_name=session_state["winner_team_column_name"],
                    tournament_schedule_match_number_column_name=session_state["match_number_column_name"],
                )

                _display_given_fixture_and_current_points_table(points_table_simulator.current_points_table, uploaded_fixture_df)

                with st.form(key="select_team_to_generate_qualification_scenarios"):
                    generate_qualification_scenarios_inputs = _get_inputs_to_generate_qualification_scenarios(points_table_simulator)
                    generate_qualification_scenarios_inputs_submit_button = st.form_submit_button("Submit")

                if generate_qualification_scenarios_inputs_submit_button:
                    session_state["generate_qualification_scenarios_inputs_submitted"] = True
                    session_state.update(generate_qualification_scenarios_inputs)

                if session_state["generate_qualification_scenarios_inputs_submitted"]:
                    with st.snow():
                        (
                            list_of_points_tables,
                            list_of_qualification_scenarios
                        ) = points_table_simulator.simulate_the_qualification_scenarios(
                            session_state["selected_team_to_generate_qualification_scenarios"],
                            session_state["expected_position_in_the_points_table"],
                            session_state["number_of_qualification_scenarios"]
                        )
                        st.markdown(
                            f"<p>Please find below the various qualification scenarios for <b>\
                                {session_state['selected_team_to_generate_qualification_scenarios']}</b></p><hr>",
                            unsafe_allow_html=True
                        )
                    _display_qualification_scenarios(
                        list_of_points_tables,
                        list_of_qualification_scenarios,
                        session_state["selected_team_to_generate_qualification_scenarios"],
                    )

            except InvalidColumnNamesError as column_name_error:
                st.error(f"Error: Given column '{column_name_error.column_value}' is not found in the given CSV", icon="⚠️")

            except InvalidScheduleDataError as schedule_data_error:
                st.error(f"Error: Given fixture has empty or Nan values in the '{schedule_data_error.column_name}' column", icon="⚠️")

            except NoQualifyingScenariosError as no_qualifying_scenarios_error:
                st.error(
                    f"Error: No qualifying scenarios found for the given team '{no_qualifying_scenarios_error.team_name}' at \
                        position '{no_qualifying_scenarios_error.points_table_position}' in the points table",
                    icon="⚠️"
                )
