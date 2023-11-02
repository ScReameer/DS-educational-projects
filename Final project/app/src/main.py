import flet as ft
import pickle
import pandas as pd

# Десериализация обученной нейросети
with open(r'models\nn_regressor.pkl', 'rb') as nn_file:
    neural_network_regressor = pickle.load(nn_file)
    
# Основное тело программы
def main(page: ft.Page):
    # Глобальные параметры окна
    page.title = 'Предсказание цены алмазов на основе признаков'
    page.window_height = 1000
    page.window_width = 600
    page.theme_mode = ft.ThemeMode.DARK
    
    # Функция для кнопки Submit. Получение предсказания для одного алмаза
    def btn_click(e):
        # Вспомогательная функция для валидации введенных данных
        def is_positive_number(string:str):
            try:
                return float(string) > 0
            except:
                return False
        # Валидация поля         
        if is_positive_number(txt_carat.value):
            txt_carat.error_text = ''
            request_df = pd.DataFrame({
                'carat': [float(txt_carat.value)], 
                'cut': [txt_cut.value], 
                'color': [txt_color.value], 
                'clarity': [txt_clarity.value], 
                'depth': [float(slider_depth.value)], 
                'table': [float(slider_table.value)], 
                'x': [0],
                'y': [0], 
                'z': [0]
            })
            prediction = neural_network_regressor.predict(request_df)[0]
            output.value = f'Предсказанная цена: {prediction:.2f} $'
            
        else:
            txt_carat.error_text = 'Нужно ввести положительное число'
        page.update()
            
    
    # Конвертация файла датасета в pandas.DataFrame
    def pick_files_result(e: ft.FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Отменено"
        )
        selected_files.update()
        try:
            if e.files[0].name.split('.')[-1] not in ['csv', 'txt']:
                raise TypeError
            else:
                global loaded_df
                loaded_df = pd.read_csv(e.files[0].path, index_col=0).drop(columns='price', errors='ignore')
                success_info.value = None
                save_button.disabled = False
        except TypeError:
            save_button.disabled = True
            success_info.value = f'Неверный формат данных'
        finally:
            if selected_files.value == 'Отменено':
                success_info.value = None
            page.update()
    
    # Сохранить предсказания для загруженного датасета
    def save_file_result(e: ft.FilePickerResultEvent):
        save_file_path.value = e.path if e.path else "Отменено"
        save_file_path.update()
        try:
            global predictions, loaded_df
            predictions = neural_network_regressor.predict(loaded_df)
            pd.Series(predictions).to_csv(save_file_path.value)
            success_info.value = f'Предсказания успешно сохранены'
        except:
            success_info.value = f'Неверный формат данных'
        finally:
            save_button.disabled = True
            selected_files.value = None
            save_file_path.value = None
            page.update()
            
    # Отображение примера датасета при клике на кнопку
    def hint_click(e):
        hint_image.visible = not hint_image.visible
        page.update()
    
    # Загруженный датафрейм из файла
    loaded_df = None
    # Объект с предсказаниями
    predictions = None
    
    # Поле для признака веса
    txt_carat = ft.TextField(
        label='Вес алмаза (карат)',
        width=600, 
        border='underline',
        border_color=ft.colors.PINK_400,
        icon=ft.icons.NUMBERS
    )
    # Выбор категории огранки
    txt_cut = ft.Dropdown(
        width=600,
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
        ],
        value='Fair',
        icon=ft.icons.CATEGORY_OUTLINED
    )
    # Выбор категории цвета
    txt_color = ft.Dropdown(
        width=600,
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
        ],
        value='J',
        icon=ft.icons.CATEGORY_OUTLINED
    )
    # Выбор категории чистоты
    txt_clarity = ft.Dropdown(
        width=600,
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
        ],
        value='I1',
        icon=ft.icons.CATEGORY_OUTLINED
    )
    # Слайдер для признака глубины
    depth_text = ft.Row([ft.Icon(ft.icons.NUMBERS, color=ft.colors.GREY_400), ft.Text('Общий процент глубины алмаза')])
    slider_depth = ft.Slider(
        min=50,
        max=70,
        divisions=20,
        label='{value}%',
        active_color=ft.colors.PINK_400,
        value=50
    )
    # Слайдер для признака ширины
    table_text = ft.Row([ft.Icon(ft.icons.NUMBERS, color=ft.colors.GREY_400), ft.Text('Общий процент ширины верхней грани алмаза')])
    slider_table = ft.Slider(
        min=50,
        max=70,
        divisions=20,
        label='{value}%',
        active_color=ft.colors.PINK_400,
        value=50
    )
    
    # Полученное предсказание
    output = ft.Text(
        value='',
        size=20
    )
    # Кнопка для получения предсказания
    submit_button = ft.ElevatedButton(
        "Submit",
        on_click=btn_click,
        bgcolor=ft.colors.PINK_400,
        color=ft.colors.BLACK
    )
    
    # Спойлер с изображением примера датасета
    hint_button = ft.OutlinedButton(text='Пример датасета', on_click=hint_click)
    hint_image = ft.Image(src=r'img\example.png', visible=False)
    
    # Кнопки загрузки/сохранения файла
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
    # Диалог выбора файла для загрузки        
    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    # Имена выбранных файлов
    selected_files = ft.Text()
    # Диалог выбора файла для сохранения предсказаний
    save_file_dialog = ft.FilePicker(on_result=save_file_result)
    # Путь сохраняемого файла
    save_file_path = ft.Text()
    # Информация об операции с файлами
    success_info = ft.Text()
    # Добавляем оба диалога выбора файлов в оверлей
    page.overlay.extend([pick_files_dialog, save_file_dialog])
    # Добавляем на страницу все элементы
    page.add(
        ft.Column(
            controls=[
                txt_carat,
                depth_text,
                slider_depth,
                table_text,
                slider_table,
                txt_cut, 
                txt_color, 
                txt_clarity,
                submit_button,
                output,
                hint_button,
                hint_image,
                ft.Row([upload_button, selected_files]),
                ft.Row([save_button,save_file_path]),
                success_info
            ]
        )
    )

if __name__ == '__main__':
    ft.app(target=main, view=ft.FLET_APP)
