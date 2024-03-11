import streamlit as st


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

def simulate_the_qualification_for_custom_schedule():
    _apply_banner_styles()
    _create_banner()
    fixture = st.file_uploader("Upload the CSV file", type="csv", key="file_uploader", accept_multiple_files=False, help="Please upload your tournament fixture file in CSV format.")
