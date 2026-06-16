import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, confusion_matrix, roc_auc_score, roc_curve
)

path = "data/training_dataset.xlsx"
df_ml = pd.read_excel(path)

if 'url' in df_ml.columns:
    df_ml = df_ml.drop(columns=["url"])

X = df_ml.drop(columns=["label"])
y = df_ml['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)


model_ml = LogisticRegression()
model_ml.fit(X_train, y_train)

# выставляем порог 0.3
threshold = 0.3
y_probs = model_ml.predict_proba(X_test)[:, 1] 
y_pred = (y_probs > threshold).astype(int)


print(f"⭐ Результаты модели (Порог 0.3) ⭐")
print(f"Accuracy (Общая точность): {accuracy_score(y_test, y_pred):.4f}")
print(f"Precision (Точность):      {precision_score(y_test, y_pred):.4f}")
print(f"Recall (Полнота):          {recall_score(y_test, y_pred):.4f}")
print(f"F1-Score:                  {f1_score(y_test, y_pred):.4f}")
print(f"ROC-AUC:                   {roc_auc_score(y_test, y_probs):.4f}")


plt.figure(figsize=(12, 5))

# Матрица ошибок
plt.subplot(1, 2, 1)
con_matrix = confusion_matrix(y_test, y_pred)
sns.heatmap(con_matrix, annot=True, fmt='d', cmap='Reds')
plt.title(f"Матрица ошибок (порог {threshold})")
plt.xlabel("Предсказания модели")
plt.ylabel("Реальный класс")

# ROC-кривая
plt.subplot(1, 2, 2)
fpr, tpr, _ = roc_curve(y_test, y_probs)
auc_val = roc_auc_score(y_test, y_probs)
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'AUC = {auc_val:.2f}')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.title("ROC-кривая")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.legend(loc="lower right")
plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()

# Сохранение модели
joblib.dump(model_ml, "model/phishing_model.pkl")
print("\nМодель успешно сохранена в папку model/")