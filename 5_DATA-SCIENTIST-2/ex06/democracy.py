import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from sklearn.ensemble import VotingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score, accuracy_score, classification_report, confusion_matrix

# Your existing data loading
df_training = pd.read_csv('data/Training_knight.csv')
df_validation = pd.read_csv('data/Validation_knight.csv')

# Try to load test data
try:
    df_test = pd.read_csv('data/Test_knight.csv')
    print("Test data loaded successfully")
except:
    print("No Test_knight.csv found, using validation for predictions")
    df_test = df_validation.copy()

print(f"Training data shape: {df_training.shape}")
print(f"Validation data shape: {df_validation.shape}")
print(f"Test data shape: {df_test.shape}")

# Prepare data
X_train = df_training.drop('knight', axis=1)
y_train = df_training['knight']

X_val = df_validation.drop('knight', axis=1) if 'knight' in df_validation.columns else df_validation
y_val = df_validation['knight'] if 'knight' in df_validation.columns else None

X_test = df_test.drop('knight', axis=1) if 'knight' in df_test.columns else df_test

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

print("Data preprocessing completed")
print(f"Features: {list(X_train.columns)}")
print(f"Classes: {y_train.unique()}")

# Create individual models
print("\n" + "="*50)
print("CREATING INDIVIDUAL MODELS")
print("="*50)

# 1. Decision Tree
dt_classifier = DecisionTreeClassifier(
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42
)

# 2. Logistic Regression
lr_classifier = LogisticRegression(
    max_iter=1000,
    C=1.0,
    random_state=42
)

# 3. KNN
knn_classifier = KNeighborsClassifier(
    n_neighbors=5,
    weights='distance'
)

# Train and evaluate individual models
models = {
    'Decision Tree': dt_classifier,
    'Logistic Regression': lr_classifier,
    'KNN': knn_classifier
}

individual_scores = {}

print("\nIndividual Model Performance:")
for name, model in models.items():
    # Train model
    model.fit(X_train_scaled, y_train)
    
    if y_val is not None:
        # Evaluate on validation set
        y_pred = model.predict(X_val_scaled)
        accuracy = accuracy_score(y_val, y_pred)
        f1 = f1_score(y_val, y_pred, average='weighted')
        
        individual_scores[name] = {'accuracy': accuracy, 'f1': f1}
        
        print(f"{name}:")
        print(f"  Accuracy: {accuracy:.4f}")
        print(f"  F1-Score: {f1:.4f}")
    else:
        print(f"{name}: Trained successfully")

# Create Voting Classifier
print(f"\n" + "="*50)
print("CREATING VOTING CLASSIFIER")
print("="*50)

voting_classifier = VotingClassifier(
    estimators=[
        ('dt', dt_classifier),
        ('lr', lr_classifier),
        ('knn', knn_classifier)
    ],
    voting='hard'  # Majority voting
)

# Train voting classifier
print("Training voting classifier...")
voting_classifier.fit(X_train_scaled, y_train)
print("Voting classifier trained successfully!")

# Evaluate voting classifier
if y_val is not None:
    y_pred_voting = voting_classifier.predict(X_val_scaled)
    
    voting_accuracy = accuracy_score(y_val, y_pred_voting)
    voting_f1 = f1_score(y_val, y_pred_voting, average='weighted')
    
    print(f"\n" + "="*50)
    print("VOTING CLASSIFIER RESULTS")
    print("="*50)
    print(f"Accuracy: {voting_accuracy:.4f}")
    print(f"F1-Score: {voting_f1:.4f}")
    
    # Check if requirement is met
    if voting_f1 >= 0.94:
        print("✓ F1-score requirement MET (≥94%)!")
    else:
        print("⚠ F1-score below 94% requirement")
        print("Consider tuning hyperparameters or feature engineering")
    
    # Detailed classification report
    print(f"\nDetailed Classification Report:")
    print(classification_report(y_val, y_pred_voting))
    
    # Show individual vs voting performance comparison
    print(f"\n" + "="*50)
    print("PERFORMANCE COMPARISON")
    print("="*50)
    for name, scores in individual_scores.items():
        print(f"{name}: F1={scores['f1']:.4f}")
    print(f"Voting Classifier: F1={voting_f1:.4f}")
    
    # Confusion Matrix
    cm = confusion_matrix(y_val, y_pred_voting)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
               xticklabels=y_val.unique(), yticklabels=y_val.unique())
    plt.title('Voting Classifier - Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.show()

# Make predictions on test set
print(f"\n" + "="*50)
print("MAKING PREDICTIONS")
print("="*50)

test_predictions = voting_classifier.predict(X_test_scaled)

# Show prediction distribution
unique_preds, counts = np.unique(test_predictions, return_counts=True)
print(f"Prediction Distribution:")
for pred, count in zip(unique_preds, counts):
    percentage = (count / len(test_predictions)) * 100
    print(f"  {pred}: {count} samples ({percentage:.1f}%)")

# Save predictions to file
with open('Voting.txt', 'w') as f:
    for pred in test_predictions:
        f.write(f"{pred}\n")

print(f"\nPredictions saved to 'Voting.txt'")
print(f"Total predictions made: {len(test_predictions)}")
print(f"First 10 predictions: {test_predictions[:10]}")

print(f"\n" + "="*60)
print("VOTING CLASSIFIER EXERCISE COMPLETE!")
print("="*60)
if y_val is not None:
    print(f"Final F1-Score: {voting_f1:.4f}")
    requirement_status = "MET" if voting_f1 >= 0.94 else "NOT MET"
    print(f"94% F1-Score Requirement: {requirement_status}")
print("Output file: Voting.txt")

# Show the voting process for a few examples
print(f"\n" + "="*50)
print("INDIVIDUAL MODEL PREDICTIONS (First 5 test samples)")
print("="*50)

sample_indices = range(min(5, len(X_test_scaled)))
for i in sample_indices:
    sample = X_test_scaled[i:i+1]
    
    dt_pred = dt_classifier.predict(sample)[0]
    lr_pred = lr_classifier.predict(sample)[0]
    knn_pred = knn_classifier.predict(sample)[0]
    voting_pred = test_predictions[i]
    
    print(f"Sample {i+1}:")
    print(f"  Decision Tree: {dt_pred}")
    print(f"  Logistic Reg:  {lr_pred}")
    print(f"  KNN:           {knn_pred}")
    print(f"  Voting Result: {voting_pred}")
    print()