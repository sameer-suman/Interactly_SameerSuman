import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from datasets import Dataset
import evaluate
import numpy as np

# Prompt user for the Kaggle dataset path
file_path = input("Please enter the path to the Kaggle dataset CSV file: ")

# Load the dataset
df = pd.read_csv(file_path)

# Use 'Resume_str' for text and 'Category' for labels
df = df[['Resume_str', 'Category']]

# Rename columns for consistency
df.columns = ['text', 'label']

# Map string labels to integers
label_mapping = {label: idx for idx, label in enumerate(df['label'].unique())}
df['label'] = df['label'].map(label_mapping)

# Convert DataFrame to HuggingFace Dataset
dataset = Dataset.from_pandas(df)

# Load a pre-trained model and tokenizer
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=len(label_mapping))

# Tokenize the dataset
def tokenize_function(examples):
    return tokenizer(examples['text'], padding="max_length", truncation=True)

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Define the training arguments
training_args = TrainingArguments(
    output_dir="./results",
    eval_strategy="epoch",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
)

# Define the accuracy metric using the new evaluate library
accuracy_metric = evaluate.load("accuracy")

def compute_metrics(p):
    predictions, labels = p
    preds = np.argmax(predictions, axis=1)
    accuracy = accuracy_metric.compute(predictions=preds, references=labels)
    return accuracy

# Create the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets,
    eval_dataset=tokenized_datasets,
    compute_metrics=compute_metrics
)

# Train the model
trainer.train()

# Save the model
model.save_pretrained("./fine_tuned_model")
tokenizer.save_pretrained("./fine_tuned_model")

# Save the label mapping for inference
import json
with open("label_mapping.json", "w") as f:
    json.dump(label_mapping, f)
