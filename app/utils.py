import streamlit as st

def inject_custom_css():
    """Injects high-end UI styling for Streamlit."""
    st.markdown("""
    <style>
    /* Styling for Streamlit */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }
    div[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95);
        border-right: 1px solid rgba(125, 211, 252, 0.2);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 8px 8px 0px 0px;
        gap: 4px;
        padding-top: 10px;
        padding-bottom: 10px;
        color: #94a3b8;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(99, 102, 241, 0.1);
        border-bottom: 2px solid #818cf8;
        color: #f8fafc;
        font-weight: 600;
    }
    .stat-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(125, 211, 252, 0.15);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #818cf8, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .item-card {
        background: linear-gradient(135deg, rgba(8, 14, 44, 0.8), rgba(20, 25, 60, 0.8));
        border-left: 4px solid #6366f1;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.8rem;
    }
    </style>
    """, unsafe_allow_html=True)

def render_item_card(title: str, item: dict):
    """Renders a visually appealing HTML card for an ensemble item."""
    if not item:
        st.warning(f"No suitable {title} found.")
        return
        
    st.markdown(f"""
    <div class="item-card">
        <h4 style="color: #cbd5e1; font-size:0.9rem; text-transform:uppercase; margin-bottom:0.3rem;">👗 {title}</h4>
        <h3 style="margin-top:0; color:#f8fafc; font-size:1.2rem;">{item['name']}</h3>
        <p style="color:#94a3b8; font-size:0.85rem; margin-bottom:0;">
            Color: <strong>{item.get('color', 'N/A')}</strong> | Style: <strong>{item.get('style_type', 'N/A')}</strong>
        </p>
        <p style="color:#64748b; font-size:0.75rem; margin-top:0.2rem; margin-bottom:0;">
            Pattern: {item.get('pattern', 'N/A')} | Warmth Index: {item.get('warmth_index', 'N/A')}/10
        </p>
    </div>
    """, unsafe_allow_html=True)
