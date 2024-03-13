import streamlit as st


session_state = {
    "column_name_input_form_submitted": False,
}

def _apply_banner_styles():
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
    st.markdown(
        """
        <div class="banner">
            <div class="title">🏆⚽ Qualification Scenario Generator ⚽🏆</div>
            <div class="subtitle">📊 Calculate qualification scenarios for your own tournament fixture 📊</div>
            <p class="description">📂 Upload your tournament fixture and calculate the various possible qualification scenarios for your favourite team 📈</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def _create_column_name_inputs_form():
    st.markdown("<p>Please enter the names for the respective columns in your fixture if they are different from the below defaults</p>", unsafe_allow_html=True)
    st.write("")

    input_column_1, input_column_2, input_column_3, input_column_4 = st.columns(4, gap="small")
    home_team_column_name = input_column_1.text_input("Home team column name", value="Home")
    away_team_column_name = input_column_2.text_input("Away team column name", value="Away")
    winner_team_column_name = input_column_3.text_input("Winner team column name", value="Winner")
    match_number_column_name = input_column_4.text_input("Match number column name", value="Match No")

    st.write("")

    return home_team_column_name, away_team_column_name, winner_team_column_name, match_number_column_name


def simulate_the_qualification_for_custom_schedule():
    _apply_banner_styles()
    _create_banner()
    fixture = st.file_uploader("Upload the CSV file", type="csv", key="file_uploader", accept_multiple_files=False, help="Please upload your tournament fixture file in CSV format.")

    if fixture:
        with st.form(key="column_name_inputs_form", clear_on_submit=True):
            home_team_column_name, away_team_column_name, winner_team_column_name, match_number_column_name = _create_column_name_inputs_form()
            column_name_inputs_form_submit_button_clicked = st.form_submit_button("Submit")

        if column_name_inputs_form_submit_button_clicked:
            session_state["column_name_input_form_submitted"] = True
            session_state.update(
                {
                    "home_team_column_name": home_team_column_name,
                    "away_team_column_name": away_team_column_name,
                    "winner_team_column_name": winner_team_column_name,
                    "match_number_column_name": match_number_column_name,
                }
            )
