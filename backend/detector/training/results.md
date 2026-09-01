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

## Experiment 5 — 5-Fold Cross-Validation**

Model: TF-IDF + Linear SVM

Folds: 5

### Accuracy

Fold scores:

- 0.9937
- 0.9935
- 0.9937
- 0.9930
- 0.9927

Mean Accuracy: 99.33%

Standard Deviation: 0.04 percentage points

### Precision

Mean Precision: 99.11%

Standard Deviation: 0.12 percentage points

### Recall

Mean Recall: 99.68%

Standard Deviation: 0.07 percentage points

### F1 Score

Mean F1: 99.39%

Standard Deviation: 0.03 percentage points


## Experiment 6 — Model Interpretability**

Model: TF-IDF + Linear SVM

The learned Linear SVM coefficients were analyzed to identify the features most strongly associated with each class.

### Top Features Associated with Fake News

- read
- video
- just
- featured image
- featured
- image
- GOP
- president Trump
- breaking
- Hillary
- Getty
- watch
- Obama
- Breitbart
- HTTPS

### Top Features Associated with Real News

- Reuters
- said
- Washington Reuters
- Reuters president
- president Donald
- Washington
- Wednesday
- Republican
- Tuesday
- Thursday
- New York Reuters
- factbox
- Democratic
- statement
- London

### Observation

The model learned strong lexical patterns associated with fake and real news.

Several highly weighted features were related to sources or formatting, such as Reuters, Breitbart, Getty Images, video, featured image, and URLs.

This suggested that the model might be partially relying on source-related artifacts rather than only learning characteristics of the article content.


## Experiment 7 — Source-Bias Analysis**

Purpose: Evaluate whether the model's high performance depends heavily on obvious source and formatting artifacts.

Model: TF-IDF + Linear SVM

### Results

Accuracy: 98.85%

### Comparison

| Model | Accuracy |
|---|---:|
| Original Linear SVM | 99.38% |
| Source-cleaned Linear SVM | 98.85% |
| Difference | -0.53 percentage points |

### Observation

Removing obvious source-related artifacts resulted in a small decrease in performance from 99.38% to 98.85%.

The model still maintained very high accuracy after source cleaning, suggesting that source artifacts contributed to the original performance but were not the only predictive signals used by the classifier.