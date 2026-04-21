import streamlit as st
import pandas as pd

from data_manager import load_wardrobe_data
from engine import StyleEngine
from utils import inject_custom_css, render_item_card

def main():
    st.set_page_config(page_title="Context Style AI PRO", page_icon="👔", layout="wide")
    
    inject_custom_css()

    wardrobe_df = load_wardrobe_data()
    engine = StyleEngine(wardrobe_df)

    with st.sidebar:
        st.markdown("<h2 style='text-align:center;'>🧠 Advanced Context</h2>", unsafe_allow_html=True)
        st.markdown("Set the hyper-parameters for your outfit:")
        
        gender = st.radio("👤 Gender Target", ["Male", "Female"], horizontal=True)

        occasion = st.selectbox(
            "📍 Social Occasion",
            [
                "Formal Event", "Wedding Guest", "Business Casual", 
                "Tech Interview", "Date Night", "Casual Outing", 
                "Beach Party", "Gym/Workout"
            ]
        )
        
        weather = st.select_slider(
            "🌤️ Weather Conditions",
            options=["Cold & Snowy ❄️", "Rainy 🌧️", "Mild & Breezy ⛅", "Sunny & Hot ☀️"],
            value="Mild & Breezy ⛅"
        )
        
        st.markdown("---")
        generate_clicked = st.button("✨ GENERATE OUTFIT", use_container_width=True, type="primary")

    st.markdown(f"<h1 style='text-align: center; margin-bottom: 0.5rem;'>Context Style AI <span style='color:#a855f7;'>PRO</span></h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #94a3b8; margin-bottom: 2rem;'>Analyzing {len(wardrobe_df)}+ garments. Powered by Pattern Harmony, Gender Dynamics, & Thermal Reasoning.</p>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["✨ Recommendations", "📥 My Wardrobe", "📊 Analytics"])

    with tab1:
        if generate_clicked:
            st.markdown(f"### 🎯 Synthesizing **{gender}** Ensemble for: **{occasion}**")
            
            result = engine.generate_ensemble(occasion, weather, gender)
            
            if "error" in result:
                st.error(result["error"])
            else:
                st.markdown(f"""
                <div style='display:flex; justify-content:space-between; align-items:center; background:rgba(30,41,59,0.5); padding:1rem; border-radius:10px; margin-bottom:1.5rem; border:1px solid #334155;'>
                    <div><span style='color:#94a3b8;'>Style Theme:</span> <strong style='color:#e2e8f0;'>{result['style_theme']}</strong></div>
                    <div><span style='color:#94a3b8;'>Target:</span> <strong style='color:#e2e8f0;'>{result['gender']}</strong></div>
                    <div><span style='color:#94a3b8;'>Match Score:</span> <strong style='color:#10b981; font-size:1.2rem;'>{result['score']}/100</strong></div>
                </div>
                """, unsafe_allow_html=True)

                col1, col2 = st.columns([2, 1])
                
                with col1:
                    items = result.get('items', {})
                    order = ['Outerwear', 'Top', 'Bottom', 'Footwear', 'Accessory']
                    for part in order:
                        if part in items:
                            render_item_card(part, items[part])
                    
                with col2:
                    st.markdown("### 🚦 System Logs")
                    if result.get("warnings"):
                        for warning in result["warnings"]:
                            if "Warning" in warning or "clash" in warning:
                                st.warning(warning)
                            else:
                                st.info(warning)
                    else:
                        st.success("Perfect Harmony. No clashes detected.")
                        
                    st.markdown("### 💈 Grooming Protocol")
                    st.markdown(f"<div style='background:rgba(20,40,30,0.6); padding:1rem; border-radius:8px; border:1px solid #10b981; color:#a7f3d0;'>{result['grooming'].replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
                    
        else:
            st.info("👈 Define your occasion, biological target, and thermal requirements, then click **Generate Outfit**.")

    with tab2:
        st.markdown(f"### 🗃️ Complete Database ({len(wardrobe_df)} Items)")
        # Allow user to quickly filter the dataframe by gender in the UI
        g_filter = st.selectbox("View Items for:", ["All", "Female", "Male", "Unisex"])
        if g_filter != "All":
            f_df = wardrobe_df[wardrobe_df['gender'] == g_filter]
            st.dataframe(f_df, use_container_width=True)
        else:
            st.dataframe(wardrobe_df, use_container_width=True)

    with tab3:
        st.markdown("### 📊 Enterprise Wardrobe Analytics")
        if not wardrobe_df.empty:
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.markdown(f"<div class='stat-card'><div class='stat-number'>{len(wardrobe_df)}</div><div style='color:#94a3b8'>Items</div></div>", unsafe_allow_html=True)
            with c2:
                cat_count = wardrobe_df['category'].nunique()
                st.markdown(f"<div class='stat-card'><div class='stat-number'>{cat_count}</div><div style='color:#94a3b8'>Categories</div></div>", unsafe_allow_html=True)
            with c3:
                m_count = (wardrobe_df['gender'] == 'Male').sum()
                st.markdown(f"<div class='stat-card'><div class='stat-number'>{m_count}</div><div style='color:#94a3b8'>Male Only</div></div>", unsafe_allow_html=True)
            with c4:
                f_count = (wardrobe_df['gender'] == 'Female').sum()
                st.markdown(f"<div class='stat-card'><div class='stat-number'>{f_count}</div><div style='color:#94a3b8'>Female Only</div></div>", unsafe_allow_html=True)
                
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("#### Gender Distribution")
                st.bar_chart(wardrobe_df['gender'].value_counts())
                
                st.markdown("#### Color Variety")
                st.bar_chart(wardrobe_df['color'].value_counts())
            with col_b:
                st.markdown("#### Composition Breakdown")
                st.bar_chart(wardrobe_df['category'].value_counts())
                
                st.markdown("#### Pattern Distribution")
                st.bar_chart(wardrobe_df['pattern'].value_counts())
        else:
            st.warning("Analytics offline. Data source empty.")

if __name__ == "__main__":
    main()
