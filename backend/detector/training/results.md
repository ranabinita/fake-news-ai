# Fake News Detection — Baseline Results
## EXPERIMENT 1 - TF-IDF + Logistic Regression
## Dataset

Total articles: 38,641

- Fake: 17,446
- Real: 21,195

## Split

- Training: 30,912
- Testing: 7,729
- Test size: 20%
- Random state: 42
- Stratified split: Yes

## Model

TF-IDF + Logistic Regression

### TF-IDF

- max_features: 100,000
- ngram_range: (1, 2)
- stop_words: English

### Results

Accuracy: 98.50%

### Classification Report

| Class | Precision | Recall | F1 |
|---|---:|---:|---:|
| Fake | 0.99 | 0.98 | 0.98 |
| Real | 0.98 | 0.99 | 0.99 |

### Confusion Matrix

| | Predicted Fake | Predicted Real |
|---|---:|---:|
| Actual Fake | 3413 | 77 |
| Actual Real | 39 | 4200 |

## Experiment 2 — Linear SVM

Model:

TF-IDF + Linear SVM

Parameters:

- max_features: 100,000
- ngram_range: (1, 2)
- stop_words: English
- random_state: 42

Results:

Accuracy: 99.38%

| Class | Precision | Recall | F1 |
|---|---:|---:|---:|
| Fake | 0.99 | 0.99 | 0.99 |
| Real | 0.99 | 0.99 | 0.99 |

Confusion Matrix:

| | Predicted Fake | Predicted Real |
|---|---:|---:|
| Actual Fake | 3464 | 26 |
| Actual Real | 22 | 4217 |

## Experiment 3 — Title-Only Ablation

Model: TF-IDF + Linear SVM

Input: Article title only

Accuracy: 94.55%

F1: 0.94

Confusion Matrix:

| | Predicted Fake | Predicted Real |
|---|---:|---:|
| Actual Fake | 3249 | 241 |
| Actual Real | 180 | 4059 |


## Experiment 4 — Body-Only Ablation

Model: TF-IDF + Linear SVM

Input: Article body only

Accuracy: 99.24%

F1: 0.99

Confusion Matrix:

| | Predicted Fake | Predicted Real |
|---|---:|---:|
| Actual Fake | 3453 | 37 |
| Actual Real | 22 | 4217 |


## Ablation Comparison

| Input | Accuracy |
|---|---:|
| Title only | 94.55% |
| Body only | 99.24% |
| Title + Body | 99.38% |