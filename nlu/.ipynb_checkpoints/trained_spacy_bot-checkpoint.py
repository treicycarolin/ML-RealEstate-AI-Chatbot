import spacy
from spacy.training.example import Example
from spacy.util import minibatch, compounding
from spacy.tokens import DocBin
import random
from pathlib import Path

# Define labels
LABELS = ["LOCATION", "PRICE", "PROPERTY_TYPE", "BEDROOMS", "BATHROOMS", "AMENITY"]

# Initial raw TRAIN_DATA with approximate offsets
import pandas as pd

def load_train_data_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    train_data = []
    for _, row in df.iterrows():
        text = row['text']
        # Convert stringified list of tuples back to Python list
        entities = eval(row['entities'])  
        train_data.append((text, {"entities": entities}))
    return train_data

TRAIN_DATA = load_train_data_from_csv("real_estate_ner_dataset.csv")

from spacy.training import offsets_to_biluo_tags
from spacy.tokens import DocBin

def validate_entities(nlp, training_data):
    for text, annotations in training_data:
        doc = nlp.make_doc(text)
        try:
            tags = offsets_to_biluo_tags(doc, annotations["entities"])
        except Exception as e:
            print(f"⚠️ Misaligned entity in: '{text}'\nReason: {e}")


# Load blank English model
nlp = spacy.blank("en")
ner = nlp.add_pipe("ner")

# Add labels to the pipeline
for label in LABELS:
    ner.add_label(label)

# Fix and validate entity offsets using spaCy's char_span
def align_entities(raw_data):
    aligned_data = []
    for text, ann in raw_data:
        doc = nlp.make_doc(text)
        entities = []
        for start, end, label in ann["entities"]:
            span = doc.char_span(start, end, label=label)
            if span is not None:
                entities.append((span.start_char, span.end_char, label))
            else:
                print(f"⚠️ Skipped misaligned entity '{text[start:end]}' in: '{text}'")
        aligned_data.append((text, {"entities": entities}))
    return aligned_data

TRAIN_DATA = align_entities(RAW_TRAIN_DATA)

# Train the NER model
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
with nlp.disable_pipes(*other_pipes):
    optimizer = nlp.begin_training()
    for iteration in range(30):
        print(f"Iteration {iteration + 1}")
        random.shuffle(TRAIN_DATA)
        losses = {}
        batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.5))
        for batch in batches:
            examples = []
            for text, annotations in batch:
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)
                examples.append(example)
            nlp.update(examples, drop=0.35, losses=losses)
        print("Losses:", losses)

# Save model
output_dir = Path("trained_realestate_ner")
output_dir.mkdir(exist_ok=True)
nlp.to_disk(output_dir)
print(f"\n✅ Model saved to {output_dir}")

# Load and test model
print("\n--- Test the trained model ---")
test_text = "I want a villa in Cap Cana with 5 bedrooms and a pool for $450,000"
loaded_nlp = spacy.load(output_dir)
doc = loaded_nlp(test_text)

# Show extracted entities
for ent in doc.ents:
    print(f"{ent.text} -> {ent.label_}")

# Parse entities into model input format
def ner_output_to_model_input(doc, all_labels):
    input_dict = {label: None for label in all_labels}
    for ent in doc.ents:
        if ent.label_ in input_dict:
            input_dict[ent.label_] = ent.text
    return input_dict

parsed_input = ner_output_to_model_input(doc, LABELS)
print("\nParsed Input for Model:")
print(parsed_input)