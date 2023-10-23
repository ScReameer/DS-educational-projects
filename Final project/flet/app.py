import flet as ft
import pickle
import pandas as pd

with open('../models/xgb_pipeline.pkl', 'rb') as xgb:
    xgb_pipeline = pickle.load(xgb)
    xgb_pipeline.set_params(xgbregressor__verbosity=0, xgbregressor__device='cpu')

def main(page: ft.Page):
    
    page.window_height = 550
    page.window_width = 400
    
    def btn_click(e):
        
        def is_numeric(str:str):
            try:
                float(str)
                return True
            except:
                return False
        
        numeric_columns = [txt_carat, txt_depth, txt_table]
        categorical_columns = [txt_cut, txt_color, txt_clarity]
        validation = False
        for numeric_col, cat_col in zip(numeric_columns, categorical_columns):

            if numeric_col.value == '' or not is_numeric(numeric_col.value):
                numeric_col.error_text = 'Нужно ввести число'
                page.update()
                validation = False
            else:
                numeric_col.error_text = ''
                validation = True
                
            if cat_col.value == '' or is_numeric(cat_col.value):
                cat_col.error_text = 'Нужно ввести строку'
                page.update()
                validation = False
            else:
                cat_col.error_text = ''
                validation = True 
                
        if validation:
            request_df = pd.DataFrame({
                'carat': [float(txt_carat.value)], 
                'cut': [txt_cut.value], 
                'color': [txt_color.value], 
                'clarity': [txt_clarity.value], 
                'depth': [float(txt_depth.value)], 
                'table': [float(txt_table.value)], 
                'x': [0],
                'y': [0], 
                'z': [0]
            })
            prediction = xgb_pipeline.predict(request_df)[0]
            output.value = f'Предсказанная цена: {prediction:.2f} $'
            # page.add(ft.Text(f'Предсказанная цена: {prediction:.2f} $'))
            page.update()
        
    txt_carat = ft.TextField(
        label='Вес алмаза (карат)',
        width=400, 
        border='underline',
        border_color=ft.colors.PINK_400
    )
    txt_cut = ft.Dropdown(
        width=400,
        label='Качество огранки алмаза',
        hint_text='Выбрать качество огранки',
        focused_border_color=ft.colors.PINK_400,
        border_color=ft.colors.PINK_400,
        options=[
            ft.dropdown.Option('Fair'),
            ft.dropdown.Option('Good'),
            ft.dropdown.Option('Very Good'),
            ft.dropdown.Option('Premium'),
            ft.dropdown.Option('Ideal')
        ]
    )
    txt_color = ft.Dropdown(
        width=400,
        label='Цвет алмаза',
        hint_text='Выбрать цвет',
        border_color=ft.colors.PINK_400,
        focused_border_color=ft.colors.PINK_400,
        options=[
            ft.dropdown.Option('J'),
            ft.dropdown.Option('I'),
            ft.dropdown.Option('H'),
            ft.dropdown.Option('G'),
            ft.dropdown.Option('F'),
            ft.dropdown.Option('E'),
            ft.dropdown.Option('D')
        ]
    )
    txt_clarity = ft.Dropdown(
        width=400,
        label='Уровень чистоты алмаза',
        hint_text='Выбрать уровень чистоты',
        border_color=ft.colors.PINK_400,
        focused_border_color=ft.colors.PINK_400,
        options=[
            ft.dropdown.Option('I1'),
            ft.dropdown.Option('SI2'),
            ft.dropdown.Option('SI1'),
            ft.dropdown.Option('VS2'),
            ft.dropdown.Option('VS1'),
            ft.dropdown.Option('VVS2'),
            ft.dropdown.Option('VVS1'),
            ft.dropdown.Option('IF')
        ]
    )
    txt_depth = ft.TextField(
        label='Общий процент глубины алмаза', 
        width=400,
        border='underline',
        border_color=ft.colors.PINK_400        
    )
    txt_table = ft.TextField(
        label='Ширина вершины алмаза',
        width=400,
        border='underline',
        border_color=ft.colors.PINK_400
    )
    
    output = ft.Text(
        value='NaN',
        size=20
    )
    
    page.title = 'Предсказание цены алмазов на основе признаков'
    page.add(txt_carat)
    page.add(txt_depth)
    page.add(txt_table)
    page.add(txt_cut)
    page.add(txt_color)
    page.add(txt_clarity)
    page.add(
        ft.ElevatedButton(
            "Submit",
            on_click=btn_click,
            bgcolor=ft.colors.PINK_400,
            color=ft.colors.BLACK
        )
    )
    page.add(output)
    
if __name__ == '__main__':
    ft.app(target=main)
