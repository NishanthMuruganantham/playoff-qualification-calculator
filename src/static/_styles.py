import streamlit as st

def _apply_banner_styles():
    """Apply custom CSS styles to the banner."""
    st.markdown(
        """
        <style>
            .description {
                color: black;
                font-size: 20px;
                line-height: 1.5;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
                padding: 20px;
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
            }
            .page-intro {
                margin-top: 10px;
                color: black;
                padding: 30px;
                background-color: #BAFFD0 ; /* Semi-transparent light gray background color */
                border-radius: 10px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            }
            .page-intro p {
                font-size: 16px;
                line-height: 1.6;
                margin-bottom: 15px;
                text-align: justify;
            }
            .page-intro h2 {
                color: black;
                margin-bottom: 20px;
                text-align: center;
            }
            .page-intro h3 {
                color: black;
            }
            .page-intro hr{
                border: 1px solid green;
            }
            .page-intro blockquote{
                font-size: 1.4em;
                width:60%;
                font-family:Open Sans;
                font-style:italic;
                color: #555555;
                padding:1.2em 30px 1.2em 75px;
                border-left:8px solid #78C0A8 ;
                line-height:1.6;
                position: relative;
                background:#EDEDED;
                text-align: left;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def _apply_home_page_styles():
    """Apply custom CSS styles to the home page."""
    css_style = """
        <style>
            .container {
                margin: 0;
                padding: 0;
                width: calc(100% - 40px);
                margin: 20px auto;
                padding: 20px;
                background-color: #fff;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                overflow: auto;
            }
            .container h2 {
                font-size: 28px;
                text-align: center;
                color: #333;
                margin-bottom: 20px;
                text-transform: uppercase;
            }
            .container h3 {
                font-size: 24px;
                color: #333;
                margin-bottom: 15px;
            }
            .container hr {
                border: 1px solid green;
            }
            .container p {
                font-size: 16px;
                line-height: 1.6;
                color: #555;
                margin-bottom: 20px;
            }
            .container ol {
                list-style: none;
                padding-left: 0;
            }
            .container li {
                margin-bottom: 10px;
                color: #333;
            }
            .container li::before {
                content: "➜";
                color: #28a745;
                margin-right: 5px;
            }
        </style>
    """
    st.markdown(css_style, unsafe_allow_html=True)


def _create_banner(
    description: str = "📂 Upload your tournament fixture and calculate the various possible qualification scenarios for your favorite team 📈",
    subtitle: str = "📊 Calculate qualification scenarios for your own tournament fixture 📊",
    title: str = "🏆Playoff Qualification Scenario Generator ⚽"
):
    """Display the banner with title and description."""
    st.markdown(
        f"""
        <div class="banner">
            <div class="title">{title}</div>
            <div class="subtitle">{subtitle}</div>
            <p class="description">{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
