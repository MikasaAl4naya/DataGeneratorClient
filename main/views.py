from operator import itemgetter

import requests
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .download import download_dataset
from .forms import DatasetForm


def help(request):
    return render(request, 'main/help.html', {'title': 'Справка и документация'})


def index(request):
    url = 'http://127.0.0.1:8000/api/v1/datasetlist/'

    response = requests.get(url)
    response.raise_for_status()

    datasets = response.json().get('datasets', [])

    # Сортировка по полю 'time_create' в обратном порядке (от нового к старому)
    datasets = sorted(datasets, key=itemgetter('time_create'), reverse=True)

    paginator = Paginator(datasets, 6)  # Показывать по 6 датасетов на странице

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/index.html', {'title': 'Главная страница', 'page_obj': page_obj})


def about(request):
    return render(request, 'main/about.html')


def preview_dataset(request, dataset_id):
    # Формируем запрос для API
    url = f'http://127.0.0.1:8000/api/v1/datasetlist/{dataset_id}/'

    # Отправляем GET-запрос для получения данных датасета
    response = requests.get(url)
    response.raise_for_status()

    # Преобразуем данные датасета для вывода
    dataset_data = response.json()

    num_columns = dataset_data['num_columns']
    columns = [column['name'] for column in dataset_data['dataset_columns'][:num_columns]]
    values = [[column['value'] for column in dataset_data['dataset_columns'][i:i+num_columns]] for i in range(0, len(dataset_data['dataset_columns']), num_columns)]

    dataset = {
        'columns': columns,
        'values': values
    }
    # Передаем dataset_id в контекст
    return render(request, 'main/preview.html', {'dataset': dataset, 'dataset_id': dataset_id})

def download_dataset_view(request, dataset_id):
    file_format = request.POST.get('format')
    return download_dataset(dataset_id, file_format)

def regenerate_dataset(request, dataset_id):
    # Получаем информацию о существующем датасете
    dataset_url = f'http://127.0.0.1:8000/api/v1/datasetlist/{dataset_id}/'
    dataset_response = requests.get(dataset_url)
    dataset_response.raise_for_status()
    existing_dataset = dataset_response.json()
    num_rows = existing_dataset['num_rows']
    num_columns = existing_dataset['num_columns']
    column_names = [column['name'] for column in existing_dataset['dataset_columns'][:num_columns]]
    column_types = [column['column_type'] for column in existing_dataset['dataset_columns'][:num_columns]]

    # Создаем новый датасет с такими же параметрами
    create_url = 'http://127.0.0.1:8000/api/v1/datasetlist/'
    create_payload = {
        'title': existing_dataset['title'],
        'num_rows': num_rows,
        'num_columns': num_columns,
        'column_names': column_names,
        'column_types': column_types,
        'file_format': existing_dataset['file_format']
    }
    create_response = requests.post(create_url, json=create_payload)
    create_response.raise_for_status()
    new_dataset_id = create_response.json()['id']

    # Удаление существующего датасета
    delete_url = f'http://127.0.0.1:8000/api/v1/datasetlist/{dataset_id}/'
    delete_response = requests.delete(delete_url)
    delete_response.raise_for_status()

    # Перенаправление на страницу предварительного просмотра нового датасета
    redirect_url = f'/preview/{new_dataset_id}/'

    return redirect(redirect_url)

def create(request):
    error = ''
    if request.method == 'POST':
        form = DatasetForm(request.POST)
        if form.is_valid():
            # Получаем данные формы
            current_columns = request.POST.get('current_columns')
            print('current_columns:'+current_columns)
            if current_columns:
                num_columns = int(current_columns)
            else:
                num_columns = 3

            # Получаем названия столбцов из формы
            columns = [request.POST[f"column{i + 1}"] for i in range(num_columns)]
            # Получаем список значений, которые нужно исключить для каждого столбца
            drops = [request.POST[f"drop{i + 1}"] for i in range(num_columns)]

            # Определяем количество строк для генерации
            rows = form.cleaned_data.get('num_rows')
            # Определяем название файла для выгрузки
            filename = form.cleaned_data.get('title')
            file_format = 'json'

            # Формируем список типов столбцов с атрибутами
            column_types = []
            for drop in drops:
                if ':' in drop:
                    data_type, attributes = drop.split(':')
                    attributes = attributes.split(',')
                    column_types.append(f"{data_type}:{','.join(attributes)}")
                else:
                    column_types.append(drop)

            # Формируем запрос для API
            url = 'http://127.0.0.1:8000/api/v1/datasetlist/'
            payload = {
                "title": filename,
                "num_rows": rows,
                "num_columns": len(columns),
                "column_names": columns,
                "column_types": column_types,
                "file_format": file_format
            }
            print(payload)

            # Отправляем запрос на генерацию данных
            response = requests.post(url, json=payload)
            response.raise_for_status()
            dataset_id = response.json()['id']
            print('dataset_id', dataset_id)
            return redirect('preview', dataset_id=dataset_id)
    else:
        form = DatasetForm()

    data = {
        'form': form,
        'error': error
    }
    return render(request, 'main/create.html', data)
