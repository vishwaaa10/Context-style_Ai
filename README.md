# Context Style AI — Enterprise Architecture

This is an automated personal styling system designed to showcase robust Python modularity, data separation, and logical processing for a 4th-semester CSE project.

## Architecture

This project deliberately moves away from absolute single-file monolithic design and applies **Separation of Concerns**.

```text
context_style_ai/
├── app/
│   ├── __init__.py        # Treats directory as a python module
│   ├── main.py            # Streamlit UI & application entrypoint
│   ├── engine.py          # The Core Logic Engine (Style Harmony, Weather logic)
│   ├── data_manager.py    # The Data Integration layer (Reads csv)
│   └── utils.py           # Helper utilities and aesthetic css injection
├── data/
│   └── wardrobe.csv       # Persistent decoupled wardrobe dataset
├── requirements.txt       # Dependencies
└── README.md              # Project documentation
```

## The Data Layer vs Logic Layer
By placing the dataset in `data/wardrobe.csv` and consuming it via `app/data_manager.py`, we implement a professional abstraction over hardcoded items.

## The Contextual Engine (`app/engine.py`)
This file is the "Brain" of the operation. It includes logic gates to ensure that:
1. Styles match the Occasion (Formality filtering).
2. Colors don't clash (Color Theory: e.g., brown belts aren't paired locally with black shoes).
3. Weather dictates dynamic layering suggestions.
4. It outputs an intelligent, synchronized ensemble.

## To Run
1. Ensure dependencies are met: `pip install -r requirements.txt`
2. Run the application from the root project folder:
   ```bash
   streamlit run app/main.py
   ```
