APPEARANCE_MODES = {
    "Hacker": {
        "bg_primary": "#0a0e27",
        "bg_secondary": "#1a1f3a",
        "text_primary": "#00ff00",
        "border": "#00ff00",
        "hover_bg": "#00ff00",
        "hover_text": "#0a0e27",
    },
    "Groovy": {
        "bg_primary": "#2d1b4e",
        "bg_secondary": "#422d5f",
        "text_primary": "#ffb347",
        "border": "#ff6b9d",
        "hover_bg": "#ff6b9d",
        "hover_text": "#2d1b4e",
    },
    "Color-Blind": {
        "bg_primary": "#1a1a1a",
        "bg_secondary": "#2d2d2d",
        "text_primary": "#ffeb3b",
        "border": "#64b5f6",
        "hover_bg": "#64b5f6",
        "hover_text": "#1a1a1a",
    },
    "Classic": {
        "bg_primary": "#000000",
        "bg_secondary": "#0d0d0d",
        "text_primary": "#00ffff",
        "border": "#ff00ff",
        "hover_bg": "#ff00ff",
        "hover_text": "#000000",
    },
}


def get_theme_css(appearance_mode):
    """Generate CSS for the selected appearance mode."""
    if appearance_mode not in APPEARANCE_MODES:
        appearance_mode = "Classic"

    theme = APPEARANCE_MODES[appearance_mode]

    css = f"""
    <style>
    body, .main, .stApp {{
        background-color: {theme['bg_primary']} !important;
        color: {theme['text_primary']} !important;
    }}
    .stMarkdown, .stWrite, p {{
        color: {theme['text_primary']} !important;
    }}
    .stExpander > div:first-child {{
        background-color: {theme['bg_secondary']} !important;
        border: 1px solid {theme['border']} !important;
        color: {theme['text_primary']} !important;
    }}
    .stExpanderContent {{
        background-color: {theme['bg_primary']} !important;
        border: 1px solid {theme['border']} !important;
    }}
    .stTextInput > div > div > input {{
        background-color: {theme['bg_secondary']} !important;
        color: {theme['text_primary']} !important;
        border: 1px solid {theme['border']} !important;
    }}
    .stButton > button {{
        background-color: {theme['bg_secondary']} !important;
        color: {theme['text_primary']} !important;
        border: 1px solid {theme['border']} !important;
    }}
    .stButton > button:hover {{
        background-color: {theme['hover_bg']} !important;
        color: {theme['hover_text']} !important;
    }}
    .stCheckbox > label {{
        color: {theme['text_primary']} !important;
    }}
    .stRadio > label {{
        color: {theme['text_primary']} !important;
    }}
    .stSelectbox > label {{
        color: {theme['text_primary']} !important;
    }}
    .stInfo, .stSuccess, .stWarning, .stError {{
        background-color: {theme['bg_secondary']} !important;
        border: 1px solid {theme['border']} !important;
        color: {theme['text_primary']} !important;
    }}
    .stDivider {{
        border-color: {theme['border']} !important;
    }}
    </style>
    """
    return css
