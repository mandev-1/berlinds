import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score, accuracy_score, classification_report
import sys

# Load your existing data (modify paths as needed)
df_training = pd.read_csv('data/Training_knight.csv')
df_validation = pd.read_csv('data/Validation_knight.csv')

# If you have a test file, load it too
try:
    df_test = pd.read_csv('data/Test_knight.csv')
    has_test = True
except:
    print("No Test_knight.csv found, will use validation set for predictions")
    df_test = df_validation.copy()
    has_test = False

print(f"Training data shape: {df_training.shape}")
print(f"Validation data shape: {df_validation.shape}")
print(f"Test data shape: {df_test.shape}")

# Prepare training data
X_train = df_training.drop('knight', axis=1)  # Assuming 'knight' is the target column
y_train = df_training['knight']

# Prepare validation data
X_val = df_validation.drop('knight', axis=1) if 'knight' in df_validation.columns else df_validation
y_val = df_validation['knight'] if 'knight' in df_validation.columns else None

# Prepare test data (remove target if it exists)
X_test = df_test.drop('knight', axis=1) if 'knight' in df_test.columns else df_test

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

print("Data preprocessing completed")

# Test different k values and plot accuracy
k_values = range(1, 31)
accuracies = []
f1_scores = []

print("Testing different k values...")
for k in k_values:
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train_scaled, y_train)
    
    if y_val is not None:
        y_pred_val = knn.predict(X_val_scaled)
        accuracy = accuracy_score(y_val, y_pred_val)
        f1 = f1_score(y_val, y_pred_val, average='weighted', zero_division=0)
    else:
        # If no validation labels, use cross-validation or training accuracy
        accuracy = knn.score(X_train_scaled, y_train)
        f1 = 0.0
    
    accuracies.append(accuracy)
    f1_scores.append(f1)
    
    if k <= 10 or k % 5 == 0:  # Print progress
        print(f"k={k}: accuracy={accuracy:.4f}, f1={f1:.4f}")

# Find best k
best_idx = np.argmax(accuracies)
best_k = k_values[best_idx]
best_accuracy = accuracies[best_idx]
best_f1 = f1_scores[best_idx]

print(f"\nBest k: {best_k} with accuracy: {best_accuracy:.4f}, F1: {best_f1:.4f}")

# Plot the accuracy graph (matching the style from your image)
plt.figure(figsize=(10, 6))
plt.plot(k_values, accuracies, 'b-', linewidth=2)
plt.xlabel('k values')
plt.ylabel('accuracy')
plt.title('Training Piscine datascience - 4')
plt.grid(True, alpha=0.3)
plt.xlim(0, 30)

# Match the y-axis range from your reference image
if max(accuracies) > 0.9:
    plt.ylim(0.925, 0.965)
else:
    plt.ylim(min(accuracies) - 0.01, max(accuracies) + 0.01)

plt.tight_layout()
plt.show()

# Train final model with best k
final_knn = KNeighborsClassifier(n_neighbors=best_k)
final_knn.fit(X_train_scaled, y_train)

# Make predictions on test set
test_predictions = final_knn.predict(X_test_scaled)

# Save predictions to KNN.txt
with open('KNN.txt', 'w') as f:
    for pred in test_predictions:
        f.write(f"{pred}\n")

print(f"\nPredictions saved to KNN.txt")
print(f"Total predictions: {len(test_predictions)}")

# Show some example predictions
print(f"\nFirst 10 predictions: {test_predictions[:10]}")

# Final model evaluation
if y_val is not None:
    final_pred_val = final_knn.predict(X_val_scaled)
    final_f1 = f1_score(y_val, final_pred_val, average='weighted')
    print(f"\nFinal F1-score: {final_f1:.4f}")
    
    if final_f1 >= 0.92:
        print("✓ F1-score requirement met!")
    else:
        print("⚠ F1-score below 92% - consider tuning hyperparameters")
        
    print(f"\nClassification Report:")
    print(classification_report(y_val, final_pred_val))

print(f"\n{'='*50}")
print("KNN Classification Complete!")
print(f"Best k: {best_k}")
print(f"Best accuracy: {best_accuracy:.4f}")
if y_val is not None:
    print(f"F1-score: {final_f1:.4f}")