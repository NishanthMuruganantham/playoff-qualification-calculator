import streamlit as st


def _apply_banner_styles():
    css = """
    <style>
        .banner {
            background-color: #72ff9f;
            color: #333;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-family: Arial, sans-serif;
            margin-bottom: 20px;
        }
        .title {
            font-size: 32px;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            margin-bottom: 10px;
        }
        .subtitle {
            font-size: 18px;
            font-style: italic;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


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
    subtitle: str = "📊 Calculate qualification scenarios for your own tournament fixture 📊",
    title: str = "🏆 Playoff Qualification Scenario Generator 🔢"
):
    banner_html = f"""
    <div class="banner">
        <div class="title">{title}</div>
        <div class="subtitle">{subtitle}</div>
    </div>
    """
    st.markdown(banner_html, unsafe_allow_html=True)
