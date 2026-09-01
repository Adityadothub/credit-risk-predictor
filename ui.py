import base64
from pathlib import Path

import streamlit as st


BACKGROUND_IMAGE = (
    Path(__file__).parent
    / "assets"
    / "credit-risk-background.png"
)


def apply_custom_style():
    """Apply the shared navy-and-teal visual design."""
    if not BACKGROUND_IMAGE.exists():
        return

    image_base64 = base64.b64encode(
        BACKGROUND_IMAGE.read_bytes()
    ).decode("utf-8")

    st.markdown(
        f"""
        <style>
            [data-testid="stAppViewContainer"] {{
                background:
                    linear-gradient(
                        rgba(7, 26, 51, 0.72),
                        rgba(7, 26, 51, 0.72)
                    ),
                    url("data:image/png;base64,{image_base64}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}

            .block-container {{
                max-width: 1100px;
                margin-top: 2rem;
                margin-bottom: 2rem;
                padding: 2.5rem;
                border-radius: 20px;
                background: rgba(255, 255, 255, 0.92);
                box-shadow: 0 12px 35px rgba(0, 0, 0, 0.22);
            }}

            h1, h2, h3 {{
                color: #071A33;
            }}

            div.stButton > button {{
                width: 100%;
                border: none;
                border-radius: 10px;
                padding: 0.6rem 1rem;
                background-color: #14B8A6;
                color: white;
                font-weight: 700;
                transition: all 0.2s ease-in-out;
            }}

            div.stButton > button:hover {{
                background-color: #0F9488;
                transform: translateY(-2px);
                box-shadow: 0 6px 14px rgba(20, 184, 166, 0.35);
            }}

            [data-testid="stSidebar"] > div:first-child {{
                background: rgba(7, 26, 51, 0.97);
            }}

            [data-testid="stSidebar"] * {{
                color: #E6FFFB;
            }}

            div[data-baseweb="input"] > div,
            div[data-baseweb="select"] > div {{
                border-radius: 10px;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )