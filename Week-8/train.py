import argparse
import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

import os
import joblib

def model_fn(model_dir):
    """
    This function is called by the SageMaker Scikit-Learn container 
    to load the model for inference.
    """
    model_path = os.path.join(model_dir, "model.joblib")
    model = joblib.load(model_path)
    return model

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    # Hyperparameters sent by the HPO Tuner
    parser.add_argument('--n_estimators', type=int, default=100)
    parser.add_argument('--learning_rate', type=float, default=0.1)
    
    # SageMaker paths
    parser.add_argument('--model-dir', type=str, default=os.environ.get('SM_MODEL_DIR'))
    parser.add_argument('--train', type=str, default=os.environ.get('SM_CHANNEL_TRAIN'))

    args, _ = parser.parse_known_args()

    # 1. LOAD DATA
    # Finds the single S3 file in the training channel
    input_files = [os.path.join(args.train, file) for file in os.listdir(args.train)]
    df = pd.read_csv(input_files[0])

    # 2. SPLIT DATA
    # Ensure 'Churn' is the name of your target column
    X = df.drop('Churn_Yes', axis=1)
    y = df['Churn_Yes']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 3. DEFINE MODELS
    rf = RandomForestClassifier(n_estimators=args.n_estimators)
    gb = GradientBoostingClassifier(learning_rate=args.learning_rate)
    lr = LogisticRegression(max_iter=1000)

    # The Voting Classifier "Committee"
    ensemble = VotingClassifier(
        estimators=[('rf', rf), ('gb', gb), ('lr', lr)],
        voting='soft'
    )

    # 4. TRAIN
    print("Training models... please wait.")
    ensemble.fit(X_train, y_train)

    # 5. EVALUATE (Crucial for HPO)
    # We print the AUC so the Tuner can "read" it from the logs
    probs = ensemble.predict_proba(X_test)[:, 1]
    auc_score = roc_auc_score(y_test, probs)
    print(f"VALIDATION_AUC: {auc_score}")

    # 6. SAVE MODEL WEIGHTS
    joblib.dump(ensemble, os.path.join(args.model_dir, "model.joblib"))
    print("Training complete. Model saved.")