
**Week 6 – Ames Housing Price Prediction**

**Project Overview**

This project focuses on building and evaluating machine learning models to predict **residential housing prices in Ames, Iowa** using the Ames Housing dataset.

The goal is to implement a **complete machine learning pipeline**, including:

* Data preprocessing
* Feature engineering
* Model training
* Cloud-based experimentation
* Model performance comparison

A **Model Bake-off** was conducted to benchmark two different algorithms:

* **MLPRegressor (Artificial Neural Network)**
* **XGBoost Regressor (Gradient Boosting)**

---

**Key Objectives**

**1. Data Preprocessing**

* Cleaned the Ames Housing dataset
* Handled missing values
* Removed inconsistencies in features

**2. Feature Engineering**

* Applied **One-Hot Encoding** for categorical variables
* Performed **feature scaling** to support neural network training

**3. Cloud Integration**

* Stored datasets using **AWS S3**
* Used **Amazon SageMaker** for scalable model training

**4. Algorithm Benchmarking**

Compared the performance of:

* **MLPRegressor**
* **XGBoost Regressor**

Evaluation metric used: **R² Score (Coefficient of Determination)**.

---

**Technology Stack**

**Programming Language**

* Python 3.11

**Machine Learning**

* Scikit-Learn
* XGBoost

**Data Processing**

* Pandas
* NumPy

**Cloud Services**

* AWS S3
* Amazon SageMaker

**Version Control**

* Git / GitHub

---

**Repository Structure**

```
Week-6-Ames-Housing/
│
├── data/        # Raw and processed dataset files
├── notebooks/   # Exploratory Data Analysis & experiments
└── README.md
```

---

**Model Performance Summary**

Models were evaluated using the **R² score**, which measures how well the model explains variance in housing prices.

| Model        | R² Score | Observations                                                |
| ------------ | -------- | ----------------------------------------------------------- |
| MLPRegressor | 0.89     | Demonstrated stable convergence with an L-shaped loss curve |
| XGBoost      | 0.92     | Achieved the best performance for tabular data              |

**Best Performing Model: XGBoost Regressor**

XGBoost outperformed the neural network because it is particularly effective for **structured/tabular datasets**.

---

**How to Run the Project**

**Local Exploration**

Run the notebooks inside the `notebooks/` directory for:

* Exploratory Data Analysis
* Feature engineering
* Model experimentation
* Model Bake-off comparison

---

**Cloud Training (SageMaker)**

To train the model using cloud infrastructure, run:

```bash
python scripts/train.py --train s3://your-bucket-path/data/
```

This allows training directly on datasets stored in **Amazon S3**.

---

**Learning Outcomes**

Through this project, the following concepts were reinforced:

* Implementation of the **ReLU activation function** for non-linear modeling
* Understanding **neural network convergence behavior**
* Importance of **max_iter tuning** in neural networks
* Feature encoding for **machine learning pipelines**
* Transition from **local experimentation to cloud-based training**
* Practical use of **Amazon SageMaker for scalable ML workflows**

