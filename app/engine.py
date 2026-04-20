import random
import pandas as pd
from typing import Dict, Any, List

class StyleEngine:
    """
    Advanced Logic Engine: Matches outfits using Contextual Logic, Color Theory, 
    Weather Parsing (Warmth Index), Pattern Harmony, Gender Targeting, and Style Scoring.
    """

    def __init__(self, wardrobe_df: pd.DataFrame):
        self.wardrobe = wardrobe_df

    def get_weather_requirements(self, weather: str) -> dict:
        if weather == "Cold & Snowy ❄️":
            return {"min_warmth": 5, "needs_outerwear": True, "condition": "cold"}
        elif weather == "Rainy 🌧️":
            return {"min_warmth": 4, "needs_outerwear": True, "condition": "rain"}
        elif weather == "Sunny & Hot ☀️":
            return {"max_warmth": 4, "needs_outerwear": False, "condition": "hot"}
        else: # Mild
            return {"min_warmth": 2, "max_warmth": 8, "needs_outerwear": False, "condition": "mild"}

    def get_formality_from_occasion(self, occasion: str) -> list:
        occasion_map = {
            "Formal Event": ["Formal"],
            "Tech Interview": ["Smart Casual", "Formal"],
            "Business Casual": ["Smart Casual"],
            "Date Night": ["Smart Casual", "Formal"],
            "Casual Outing": ["Casual", "Smart Casual"],
            "Wedding Guest": ["Formal"],
            "Beach Party": ["Casual"],
            "Gym/Workout": ["Athletic", "Casual"]
        }
        return occasion_map.get(occasion, ["Casual"])

    def color_harmony_check(self, base_color: str, target_color: str) -> int:
        base_color, target_color = base_color.lower(), target_color.lower()
        clashes = {
            "black": ["brown", "navy"],
            "brown": ["black"],
            "navy": ["black"]
        }
        if target_color in clashes.get(base_color, []):
            return -10 # Severe clash
        
        neutrals = ["white", "black", "grey", "beige", "navy", "tan"]
        if base_color in neutrals or target_color in neutrals:
            return 2 # Safe combination
            
        return 0

    def pattern_harmony_check(self, pattern1: str, pattern2: str) -> int:
        if pattern1 != "Solid" and pattern2 != "Solid":
            if pattern1 != pattern2:
                return -15 # Extreme pattern clash
            return -5 # Too much of the same pattern
        return 0

    def get_grooming_advice(self, formality: str, gender: str) -> str:
        if gender == "Male":
            if formality == "Formal":
                return "✂️ Hair: Neat side-part or slicked back.\n🪒 Face: Clean shave or a strictly defined beard.\n🌟 Fragrance: Sophisticated woody or amber EDP."
            elif formality == "Smart Casual":
                return "✂️ Hair: Styled with a flexible hold.\n🪒 Face: Trimmed stubble is fine.\n🌟 Fragrance: Fresh, clean EDT."
            elif formality in ["Athletic", "Casual"]:
                return "✂️ Hair: Effortless texture or tied back.\n🪒 Face: Natural stubble.\n🌟 Fragrance: Aquatic body spray or deodorant."
        elif gender == "Female":
            if formality == "Formal":
                return "✂️ Hair: Elegant updo, or sleek blowout.\n💄 Makeup: Classic red lip or subtle smokey eye.\n🌟 Fragrance: Elegant floral or musky EDP."
            elif formality == "Smart Casual":
                return "✂️ Hair: Soft waves or neat ponytail.\n💄 Makeup: Natural 'no-makeup' makeup look.\n🌟 Fragrance: Light, fresh floral or citrus EDT."
            elif formality in ["Athletic", "Casual"]:
                return "✂️ Hair: Messy bun, braids, or natural.\n💄 Makeup: Lip balm and SPF.\n🌟 Fragrance: Clean body mist."
        
        return "✂️ Keep it clean and presentable. Use a light fragrance."

    def generate_ensemble(self, occasion: str, weather: str, gender: str) -> Dict[str, Any]:
        """Master Matching Algorithm utilizing Gender, Weather, and Style checks."""
        allowed_styles = self.get_formality_from_occasion(occasion)
        target_style = allowed_styles[0]
        weather_reqs = self.get_weather_requirements(weather)

        # 1. Filter by Gender first (allow specific gender + unisex)
        gender_df = self.wardrobe[self.wardrobe['gender'].isin([gender, 'Unisex'])]
        
        # 2. Filter by allowed styles
        style_df = gender_df[gender_df['style_type'].isin(allowed_styles)]
        
        # Fallback to broader styles if absolutely needed
        if style_df.empty:
            style_df = gender_df

        ensemble = {}
        score = 100
        warnings = []

        # --- TOP SELECTION ---
        tops = style_df[style_df['category'] == 'Top']
        if "max_warmth" in weather_reqs:
            tops = tops[tops['warmth_index'] <= weather_reqs['max_warmth']]
        if not tops.empty:
            top_choice = tops.sample(1).iloc[0]
            ensemble['Top'] = top_choice
        else:
            return {"error": f"No suitable Tops found for {gender} given weather '{weather}' and occasion '{occasion}'."}

        # --- BOTTOM SELECTION ---
        bottoms = style_df[style_df['category'] == 'Bottom']
        if not bottoms.empty:
            bot_scores = bottoms.apply(
                lambda row: self.pattern_harmony_check(top_choice['pattern'], row['pattern']), axis=1
            )
            best_bottom_idx = bot_scores.idxmax()
            ensemble['Bottom'] = bottoms.loc[best_bottom_idx]
            
            p_score = bot_scores[best_bottom_idx]
            if p_score < 0:
                warnings.append("Pattern clash detected (Top/Bottom).")
                score += p_score
        else:
            warnings.append("No suitable Bottoms found in standard pool.")

        # --- FOOTWEAR SELECTION ---
        footwear = style_df[style_df['category'] == 'Footwear']
        if not footwear.empty:
            bottom_color = ensemble.get('Bottom', top_choice)['color']
            fw_scores = footwear.apply(
                lambda row: self.color_harmony_check(bottom_color, row['color']), axis=1
            )
            best_fw_idx = fw_scores.idxmax()
            ensemble['Footwear'] = footwear.loc[best_fw_idx]
            
            c_score = fw_scores[best_fw_idx]
            if c_score < 0:
                warnings.append("Color clash detected (Bottoms/Shoes).")
                score += c_score
        
        # --- ACCESSORIES SELECTION ---
        accessories = style_df[style_df['category'] == 'Accessories']
        if not accessories.empty:
            fw_color = ensemble.get('Footwear', top_choice)['color']
            acc_scores = accessories.apply(
                lambda row: self.color_harmony_check(fw_color, row['color']), axis=1
            )
            best_acc_idx = acc_scores.idxmax()
            ensemble['Accessory'] = accessories.loc[best_acc_idx]

        # --- OUTERWEAR SELECTION (Dynamic) ---
        if weather_reqs.get("needs_outerwear") or (gender_df['category'] == 'Outerwear').sum() > 0:
            outerwear = style_df[style_df['category'] == 'Outerwear']
            if weather_reqs.get("needs_outerwear"):
                if "min_warmth" in weather_reqs:
                    outerwear = outerwear[outerwear['warmth_index'] >= weather_reqs['min_warmth']]
                if not outerwear.empty:
                    ensemble['Outerwear'] = outerwear.sample(1).iloc[0]
                    warnings.append("❄️ Weather adaptation: Outerwear added.")
                else: # Fallback to any outerwear if it's strictly needed but misses warmth
                    fallback_ow = style_df[(style_df['category'] == 'Outerwear')]
                    if not fallback_ow.empty:
                         ensemble['Outerwear'] = fallback_ow.sample(1).iloc[0]
                         warnings.append("❄️ Added Outerwear, but may not be perfectly rated for this weather condition.")
                    else:
                        score -= 10
                        warnings.append("⚠️ Weather Warning: Missing suitable Outerwear for conditions.")
        
        result = {
            "success": True,
            "occasion": occasion,
            "weather": weather,
            "gender": gender,
            "style_theme": target_style,
            "score": min(score, 100),
            "warnings": warnings,
            "grooming": self.get_grooming_advice(target_style, gender)
        }
        
        result['items'] = {k: v.to_dict() for k, v in ensemble.items()}
        return result
