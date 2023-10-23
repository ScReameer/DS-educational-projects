import flet as ft
import pickle
import pandas as pd

with open('../models/xgb_pipeline.pkl', 'rb') as xgb:
    xgb_pipeline = pickle.load(xgb)
    xgb_pipeline.set_params(xgbregressor__verbosity=0, xgbregressor__device='cpu')

def main(page: ft.Page):
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
            try:
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
            
                page.add(ft.Text(f'Предсказанная цена: {prediction:.2f} $'))
                page.update()
            except:
                page.add(ft.Text('Неверный формат одной из категорий: огранка, цвет или чистота'))
        
    txt_carat = ft.TextField(label='Вес алмаза (карат)')
    txt_cut = ft.TextField(label='Качество огранки')
    txt_color = ft.TextField(label='Цвет алмаза')
    txt_clarity = ft.TextField(label='Чистота алмаза')
    txt_depth = ft.TextField(label='Общий процент глубины алмаза')
    txt_table = ft.TextField(label='Ширина вершины алмаза')

    page.title = 'Предсказание цены алмазов на основе признаков'
    page.add(txt_carat)
    page.add(txt_cut)
    page.add(txt_color)
    page.add(txt_clarity)
    page.add(txt_depth)
    page.add(txt_table, ft.ElevatedButton("Submit", on_click=btn_click))
    
if __name__ == '__main__':
    ft.app(target=main)
