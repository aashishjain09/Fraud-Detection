import os, numpy as np, Fraud-Detection.logging as logger
from transformers import AutoTokenizer
from datasets import load_dataset, load_from_disk
from Fraud-Detection.config.configuration import DataTransformationConfig
from sklearn.impute import SimpleImputer
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.utils.class_weight import compute_class_weight
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_name)

    def convert_examples_to_features(self, example_batch):
        input_encodings = self.tokenizer(example_batch['dialogue'], max_length=1024, truncation=True)

        with self.tokenizer.as_target_tokenizer():
            target_encodings = self.tokenizer(example_batch['summary'], max_length=128, truncation=True)

        return {
            'input_ids': input_encodings['input_ids'],
            'attention_mask': input_encodings['attention_mask'],
            'labels': target_encodings['input_ids']
        }
    
    def convert(self):
        dataset_samsum = load_from_disk(self.config.data_path)
        dataset_samsum_pt = dataset_samsum.map(self.convert_examples_to_features, batched=True)
        dataset_samsum_pt.save_to_disk(os.path.join(self.config.root_dir, "samsum_dataset"))



class DataTransformation_v2:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        # Placeholder: to be set after analyzing correlations
        self.high_corr_features = config.high_corr_features
        # Steps
        self.imputer = SimpleImputer(strategy='median')
        self.outlier_detector = IsolationForest(contamination=config.outlier_frac)
        self.scaler = MinMaxScaler()
        self.encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
        # Imbalance params
        self.rus = RandomUnderSampler()
        self.ros = RandomOverSampler()
        self.class_weights = None

    def fit_transform(self, X, y):
        
        # 1. Impute
        X[self.high_corr_features] = self.imputer.fit_transform(X[self.high_corr_features])
        
        # 2. Remove outliers
        mask = self.outlier_detector.fit_predict(X[self.high_corr_features]) == 1
        X, y = X[mask], y[mask]
        
        # 3. Scale numeric
        num_cols = X.select_dtypes(include=['int64','float64']).columns
        X[num_cols] = self.scaler.fit_transform(X[num_cols])
        
        # 4. Encode categorical
        cat_cols = X.select_dtypes(include=['object','category']).columns
        X_enc = self.encoder.fit_transform(X[cat_cols])
        X = np.hstack([X[num_cols].values, X_enc])
        
        # 5. Class weights
        classes = np.unique(y)
        weights = compute_class_weight('balanced', classes=classes, y=y)
        self.class_weights = dict(zip(classes, weights))
        return X, y

    def undersample(self, X, y):
        return self.rus.fit_resample(X, y)

    def oversample(self, X, y):
        return self.ros.fit_resample(X, y)

    def threshold_predict(self, model, X, threshold):
        probs = model.predict_proba(X)[:,1]
        return (probs >= threshold).astype(int)
