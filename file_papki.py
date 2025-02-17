import os
import shutil
import re
from typing import List

def extract_image_filenames_by_category(txt_filepath: str) -> dict:
    """Извлекает имена файлов изображений из текстового файла,
    разбивая их по категориям (TN, FP, FN, TP).

    Args:
        txt_filepath: Путь к текстовому файлу.

    Returns:
        Словарь, где ключи - категории (TN, FP, FN, TP),
        а значения - списки имен файлов.
    """
    categories = {
        "TN": [],
        "FP": [],
        "FN": [],
        "TP": []
    }
    current_category = None

    try:
        with open(txt_filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()  # Удаляем пробелы в начале и конце строки

                if "True Negatives (TN) filenames:" in line:
                    current_category = "TN"
                    continue
                elif "False Positives (FP) filenames:" in line:
                    current_category = "FP"
                    continue
                elif "False Negatives (FN) filenames:" in line:
                    current_category = "FN"
                    continue
                elif "True Positives (TP) filenames:" in line:
                    current_category = "TP"
                    continue

                if current_category and line:
                    if ".jpg" in line or ".png" in line or ".jpeg" in line or ".jfif" in line:
                        match = re.search(r'(\d+\.(jpg|png|jpeg|jfif))', line)
                        if match:
                            categories[current_category].append(match.group(1))

    except FileNotFoundError:
        print(f"Файл не найден: {txt_filepath}")
    except Exception as e:
        print(f"Ошибка при чтении файла {txt_filepath}: {e}")
    return categories

def copy_images_by_category(source_dir: str, destination_dir: str, txt_filepath: str):
    """Копирует изображения из исходной директории в целевую,
    создавая подпапки для каждой категории (TN, FP, FN, TP)
    и копируя изображения в соответствующие папки.

    Args:
        source_dir: Путь к директории, где находятся изображения (и подпапки).
        destination_dir: Путь к директории, куда будут скопированы изображения.
        txt_filepath: Путь к текстовому файлу, содержащему имена изображений.
    """
    categories = extract_image_filenames_by_category(txt_filepath)

    for category, image_filenames in categories.items():
        if not image_filenames:
            print(f"В категории {category} в файле {txt_filepath} не найдено имен файлов изображений.")
            continue

        destination_folder = os.path.join(destination_dir, category)
        os.makedirs(destination_folder, exist_ok=True)

        for filename in image_filenames:
            source_filepath = None
            for root, _, files in os.walk(source_dir):
                if filename in files:
                    source_filepath = os.path.join(root, filename)
                    break

            if source_filepath:
                destination_filepath = os.path.join(destination_folder, filename)
                try:
                    shutil.copy2(source_filepath, destination_filepath)
                    print(f"Скопировано: {filename} -> {destination_filepath}")
                except Exception as e:
                    print(f"Ошибка при копировании {filename}: {e}")
            else:
                print(f"Файл не найден: {filename}")


#--------------------------------------------------------------------------------
# Пример использования
#--------------------------------------------------------------------------------
# Замените эти значения на ваши реальные пути
source_directory = "D:/MSDis/МАКЕТЫ размеченные от Русса/marked_sorted_files"  # Исходная директория с изображениями
destination_directory = "D:/MSDis/МАКЕТЫ размеченные от Русса/27.01 Спорт + букмекер"  # Целевая директория для копирования
txt_file = "D:/MSDis/clone_repo_Andr_Storogenko/research-AndreyStorozhenko-rest_prod/rest_prod/27.01 Спорт_букмекерRuss.txt"  # Путь к вашему txt файлу

copy_images_by_category(source_directory, destination_directory, txt_file)
