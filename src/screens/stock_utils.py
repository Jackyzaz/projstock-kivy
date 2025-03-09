import os
import csv
from fuzzywuzzy import fuzz
from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.uix.list import OneLineListItem

def fetch_stock_symbols():
    stock_file = os.path.join(os.path.dirname(__file__), "stocks.csv")
    stock_list = []
    try:
        with open(stock_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # ข้าม header
            for row in reader:
                if len(row) >= 2:
                    symbol, company = row[0], row[1]
                    stock_list.append(f"{symbol} ({company})")
        return stock_list
    except FileNotFoundError:
        print("stocks.csv not found, using default list")
        return []
    except Exception as e:
        print(f"Error reading stocks.csv: {e}")
        return []

def handle_dropdown(instance, value=None, keycode=None, scancode=None, codepoint=None, modifier=None, search_input=None, suggestion_list=None, stock_symbols=None):
    print(f"Dropdown event: {value if value else keycode}")

    is_dropdown_open = getattr(instance, 'is_dropdown_open', False)
    selected_index = getattr(instance, 'selected_index', -1)
    suggestions = getattr(instance, 'suggestions', [])

    if isinstance(value, str):
        suggestion_list.clear_widgets()
        selected_index = -1
        
        if value and len(value) >= 2:
            suggestions = []
            for stock in stock_symbols:
                try:
                    symbol = stock.split(" (")[0]
                    company_name = stock.split(" (")[1][:-1] if " (" in stock else ""
                    exact_match = value.lower() in symbol.lower() or (company_name and value.lower() in company_name.lower())
                    symbol_score = fuzz.partial_ratio(value.lower(), symbol.lower())
                    company_score = fuzz.partial_ratio(value.lower(), company_name.lower()) if company_name else 0
                    score = max(symbol_score, company_score)
                    if exact_match:
                        score += 50
                    if score > 70:
                        suggestions.append((stock, score))
                except Exception as e:
                    print(f"Error processing stock {stock}: {e}")
                    continue
            
            suggestions.sort(key=lambda x: x[1], reverse=True)
            max_suggestions = min(5, len(suggestions))
            if max_suggestions > 0:
                is_dropdown_open = True
                update_dropdown(instance, suggestion_list, suggestions, selected_index)
            else:
                is_dropdown_open = False
                suggestion_list.height = 0
                search_input.helper_text = "No suggestions found"
        else:
            suggestions = []
            is_dropdown_open = False
            suggestion_list.height = 0
            search_input.helper_text = "Type to see suggestions"

    elif keycode:
        if not is_dropdown_open or not suggestions:
            return
        if keycode == 273:  # Up arrow
            selected_index = max(-1, selected_index - 1)
            update_dropdown(instance, suggestion_list, suggestions, selected_index)
            return True
        elif keycode == 274:  # Down arrow
            selected_index = min(len(suggestions) - 1, selected_index + 1)
            update_dropdown(instance, suggestion_list, suggestions, selected_index)
            return True
        elif keycode == 13 and selected_index >= 0:  # Enter
            select_suggestion(instance, suggestions[selected_index][0], suggestion_list, search_input)
            return True

    elif instance == Window and value.button == 'left':
        if is_dropdown_open:
            if not suggestion_list.collide_point(*value.pos) and not search_input.collide_point(*value.pos):
                is_dropdown_open = False
                suggestion_list.height = 0
                suggestion_list.clear_widgets()
                selected_index = -1
                suggestions = []
                return True

    instance.is_dropdown_open = is_dropdown_open
    instance.selected_index = selected_index
    instance.suggestions = suggestions

def update_dropdown(instance, suggestion_list, suggestions, selected_index):
    suggestion_list.clear_widgets()
    max_suggestions = min(5, len(suggestions))
    
    for i in range(max_suggestions):
        stock_item = suggestions[i][0]
        bg_color = [0.3, 0.5, 0.7, 1] if i == selected_index else [0.98, 0.98, 0.98, 1]
        item = OneLineListItem(
            text=stock_item,
            on_press=lambda x, s=stock_item: select_suggestion(instance, s, suggestion_list, instance.search_input),
            bg_color=bg_color,
            theme_text_color="Custom",
            text_color=[0, 0, 0, 0.87],
            divider="Full"
        )
        suggestion_list.add_widget(item)
    
    suggestion_list.height = dp(48) * max_suggestions

def select_suggestion(instance, suggestion, suggestion_list, search_input):
    search_input.text = suggestion
    instance.is_dropdown_open = False
    suggestion_list.height = 0
    suggestion_list.clear_widgets()
    instance.selected_index = -1
    instance.suggestions = []