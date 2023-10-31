import flet as ft
import pickle
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

with open(r'models\nn_regressor.pkl', 'rb') as nn_file:
    neural_network_regressor = pickle.load(nn_file)

def main(page: ft.Page):
    
    page.title = 'Предсказание цены алмазов на основе признаков'
    page.window_height = 1000
    page.window_width = 600
    page.theme_mode = ft.ThemeMode.DARK
    
    def btn_click(e):
        
        def is_positive_number(string:str):
            try:
                return float(string) > 0
            except:
                return False
        
        def validation():
            
            numeric_columns = [txt_carat, txt_depth, txt_table]
            categorical_columns = [txt_cut, txt_color, txt_clarity]
            for numeric_col, cat_col in zip(numeric_columns, categorical_columns):

                if numeric_col.value and is_positive_number(numeric_col.value):
                    numeric_col.error_text = ''
                    page.update()
                    check_numeric = True
                else:
                    numeric_col.error_text = 'Нужно ввести положительное число'
                    page.update()
                    check_numeric = False 
                
                if cat_col.value == None:
                    cat_col.error_text = 'Нужно выбрать категорию'
                    page.update()
                    check_categorical = False
                else:
                    cat_col.error_text = ''
                    page.update()
                    check_categorical = True 
                
            return check_numeric and check_categorical
                
        if validation():
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
            prediction = neural_network_regressor.predict(request_df)[0]
            output.value = f'Предсказанная цена: {prediction:.2f} $'
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
        border='underline',
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
        border='underline',
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
        border='underline',
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
        label='Ширина верхней грани алмаза',
        width=400,
        border='underline',
        border_color=ft.colors.PINK_400
    )
    
    output = ft.Text(
        value='',
        size=20
    )
    
    submit_button = ft.ElevatedButton(
        "Submit",
        on_click=btn_click,
        bgcolor=ft.colors.PINK_400,
        color=ft.colors.BLACK
    )
    
    page.add(
        ft.Column(
            controls=[
                txt_carat,
                txt_depth,
                txt_table,
                txt_cut, 
                txt_color, 
                txt_clarity,
                submit_button,
                output
            ]
        )
    )
    
    # Создадим класс, в атрибуте которого будем хранить изменяемые данные 
    # (для доступа к переменным внутри функций без объявления глобальных переменных)
    class MutableObject():
        def __init__(self) -> None:
            self.data = None
            
    # Pick file dialog
    def pick_files_result(e: ft.FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Отменено"
        )
        selected_files.update()
        try:
            if e.files[0].name.split('.')[-1] not in ['csv', 'txt']:
                raise TypeError
            else:
                loaded_df.data = pd.read_csv(e.files[0].path, index_col=0).drop(columns='price', errors='ignore')
                success_info.value = None
                save_button.disabled = False
        except TypeError:
            save_button.disabled = True
            success_info.value = f'Неверный формат данных'
        finally:
            if selected_files.value == 'Отменено':
                success_info.value = None
            page.update()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text()
    loaded_df = MutableObject()
    
    # Save file dialog
    def save_file_result(e: ft.FilePickerResultEvent):
        save_file_path.value = e.path if e.path else "Отменено"
        save_file_path.update()
        try:
            predictions.data = neural_network_regressor.predict(loaded_df.data)
            pd.Series(predictions.data).to_csv(save_file_path.value)
            success_info.value = f'Предсказания успешно сохранены'
        except:
            success_info.value = f'Неверный формат данных'
        finally:
            save_button.disabled = True
            selected_files.value = None
            save_file_path.value = None
            page.update()
            
    save_file_dialog = ft.FilePicker(on_result=save_file_result)
    save_file_path = ft.Text()
    predictions = MutableObject()
    success_info = ft.Text()

    # hide all dialogs in overlay
    page.overlay.extend([pick_files_dialog, save_file_dialog])

    def hint_click(e):
        hint_image.visible = not hint_image.visible
        page.update()

    hint_button = ft.OutlinedButton(text='Пример датасета', on_click=hint_click)
    hint_image = ft.Image(src='img/example.png', visible=False)
    
    upload_button = ft.ElevatedButton(
        "Загрузить файл",
        icon=ft.icons.UPLOAD_FILE,
        on_click=lambda _: pick_files_dialog.pick_files(),
    )
    
    save_button = ft.ElevatedButton(
        "Сохранить предсказания",
        icon=ft.icons.SAVE,
        on_click=lambda _: save_file_dialog.save_file(file_name='predictions.csv'),
        disabled=True,
    )
    
    page.add(
        hint_button,
        hint_image,
        ft.Row([
            upload_button,
            selected_files
        ]),
        ft.Row([
            save_button,
            save_file_path
        ]),
        success_info
    )
    
if __name__ == '__main__':
    ft.app(target=main)
