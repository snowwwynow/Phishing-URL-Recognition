import joblib
import pandas as pd
from features.extract_feat import URL_PRIZNAKI

#Загрузка уже обученной ранее модели
model = joblib.load("model/phishing_model.pkl")

#Ввод данных от пользователя

while True:

    url = input("Введите URL для проверки: ")

    if url.lower() == "стоп":
        print("Завершение работы по запросу пользователя")
        exit()

    if not url:
        print("Пустая строка. Попробуйте снова")
        continue

    if not (url.startswith("http://") or url.startswith("https://")):
        print("URL должен начинаться с http:// или https://")
        continue
    
    if "." not in url:
        print("Некорректный формат. URL должен содержать домен")
        continue

    break

priznaki = URL_PRIZNAKI(url)

df_priznakov = pd.DataFrame([priznaki], columns=[
    'URL length',
    'count_of_ture',
    'count_subdomain',
    'http or https',
    'depth',
    'entropy_domain'
])

prediction_new_priznakov = model.predict(df_priznakov)[0]

if prediction_new_priznakov == 1:
    print("Ссылка выглядит подозрительно, вам не стоит по ней переходить. Это может привести к плохим последствиям.")
else:
    print("Ссылка не выглядит подозрительно, вы можете по ней перейти.")

    
