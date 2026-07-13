from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification

MODEL_NAME = "bert-base-uncased"

print("Loading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

print("Loading model...")

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=10
)

print("Model Loaded Successfully")