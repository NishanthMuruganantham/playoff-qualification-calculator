import streamlit as st
from src.static._styles import _apply_home_page_styles


def homepage():
    """
    This function displays the homepage of the application.
    """
    _apply_home_page_styles()
    html_content = """
        <div class="container" style="background-color: #BAFFD0;">
            <h2>🏆 Playoff Qualification Scenario Generator ⚽</h2>
            <hr>
            <h3> Introduction</h3>
            <p>During the later part of the league stages in many multi-team tournaments 🏆 such as 🏏 Indian Premier League(IPL), Australian Big Bash League (BBL), ets., the fans will look for possible match outcomes for the remaining league matches, which could lead their favourite team to get qualified for further stage in the tournament (Playoffs). Here, the fans calculate their points table📊 to see their favourite team being placed in the position needed to qualify for Playoffs🏃🏻</p>
            <p>This tool 🛠️ comes in handy for sports enthusiasts, allowing them to foresee the necessary match outcomes to see their favorite team qualify for the playoffs ✅. It provides insights into the potential match results and their impact on the team's standings in the points table 📊. The tool is designed to be user-friendly and intuitive, allowing fans to easily select their favorite team and simulate the qualifying chances for the remaining league matches.</p>
            <h3>Steps to use this tool</h3>
            <ol>
                <li>The user can find the various ongoing tournaments from the dropdown in the sidebar and select the one they want.</li>
                <li>Once the tournament is selected, the page will display three components.</li>
                <li>
                    Tournament Fixture along with the result for the selected tournament
                </li>
                <li>
                    Ponits Table for the selected tournament
                </li>
                <li>A form containing a dropdown containg the list of teams, and also the inputs for their desired position in the points table</li>
                <li>Once the user selects and submits their favorite team, the tool will generate the various lists of possible remaining fixture outcomes which would favor their favorite team's qualification.</li>
            </ol>
            <h3>About this tool</h3>
            <p>The tool is built using Python and Streamlit, allowing it to be easily deployed and used in any web application. The user can customize the tool to suit their needs and preferences, making it a powerful tool for sports enthusiasts and fans alike.</p>
            <p>The tool is currently in beta stage, so please report any bugs or issues you encounter. Thank you for using the tool! 🙏</p>
            <p>Enjoy the tool and let's get started! 👋</p>
            <p style="font-size: 18px; font-weight: bold;">Nishanth Muruganantham</p>
        </div>
    """

    st.markdown(html_content, unsafe_allow_html=True)
