import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix

# Загружаем файл CSV
df = pd.read_csv('D:/MSDis/clone_repo_Andr_Storogenko/research-AndreyStorozhenko-rest_prod/rest_prod/27.01 Спорт + букмекер (основанные на риске игры, пари (азартные игры, букмекерские конторы и т.д.))Russ_OCR.csv', encoding='utf-8')
#df = pd.read_csv('D:/MSDis/clone_repo_Andr_Storogenko/research-AndreyStorozhenko-rest_prod/rest_prod/27.01 Спорт_букмекерRuss.csv', encoding='utf-8')

# Просмотр первых строк DataFrame
print(df.head())

# Убедитесь, что значения threshold_passed являются бинарными
threshold = 0.5
df['threshold_binary'] = (df['threshold_passed'] > threshold).astype(int)

# Удаление пустых значений
df.dropna(inplace=True)

# Подсчет точности
accuracy = accuracy_score(df['category_present'], df['threshold_binary'])
print("Точность:", accuracy)

# Построение матрицы путаницы
cm = confusion_matrix(df['category_present'], df['threshold_binary'])

# Печать результатов матрицы путаницы
results = {
    'tp': cm[1, 1].tolist(),
    'fp': cm[0, 1].tolist(),
    'fn': cm[1, 0].tolist(),
    'tn': cm[0, 0].tolist(),

}
print("Матрица путаницы:", results)

# Получение значений file_name для каждой категории
tn_files = df[(df['category_present'] == 0) & (df['threshold_binary'] == 0)]['file_name'].tolist()
fp_files = df[(df['category_present'] == 0) & (df['threshold_binary'] == 1)]['file_name'].tolist()
fn_files = df[(df['category_present'] == 1) & (df['threshold_binary'] == 0)]['file_name'].tolist()
tp_files = df[(df['category_present'] == 1) & (df['threshold_binary'] == 1)]['file_name'].tolist()

# Запись результатов в текстовый файл
output_file = '27.01 Спорт + букмекер (основанные на риске игры, пари (азартные игры, букмекерские конторы и т.д.))Russ_OCR.txt'  # Имя файла для сохранения результатов

with open(output_file, 'w', encoding='utf-8') as f:
    f.write("Точность: " + str(accuracy) + "\n\n")
    f.write("Матрица путаницы:\n")
    f.write(str(results) + "\n\n")

    f.write("True Negatives (TN) filenames:\n")
    for filename in tn_files:
        f.write(filename + "\n")
    f.write("\n")

    f.write("False Positives (FP) filenames:\n")
    for filename in fp_files:
        f.write(filename + "\n")
    f.write("\n")

    f.write("False Negatives (FN) filenames:\n")
    for filename in fn_files:
        f.write(filename + "\n")
    f.write("\n")

    f.write("True Positives (TP) filenames:\n")
    for filename in tp_files:
        f.write(filename + "\n")
    f.write("\n")

print(f"Результаты сохранены в файл: {output_file}")
