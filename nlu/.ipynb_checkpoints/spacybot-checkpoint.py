import spacy
from spacy.training.example import Example
from spacy.util import minibatch, compounding
import random
from pathlib import Path

# Load your training data
from generated_train_data import TRAIN_DATA

# Define the labels manually based on your dataset
LABELS = ["LOCATION", "PRICE", "PROPERTY_TYPE", "BEDROOMS", "BATHROOMS", "AMENITY"]

# Load or create a blank English model
nlp = spacy.blank("en")
ner = nlp.add_pipe("ner")

# Add labels to the NER component
for label in LABELS:
    ner.add_label(label)

# Disable other pipeline components during training
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
with nlp.disable_pipes(*other_pipes):
    optimizer = nlp.begin_training()
    for iteration in range(30):
        print(f"Iteration {iteration + 1}")
        random.shuffle(TRAIN_DATA)
        losses = {}

        # Create Example objects
        batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.5))
        for batch in batches:
            examples = []
            for text, annotations in batch:
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)
                examples.append(example)
            nlp.update(examples, drop=0.35, losses=losses)

        print("Losses", losses)

# Save the trained model
output_dir = Path("beta_test_model")
output_dir.mkdir(exist_ok=True)
nlp.to_disk(output_dir)
print(f"Model saved to {output_dir}")

# Load the trained model and test it
print("\n--- Test the trained model ---")
test_text = "Searching for a building in La Romana with 10 bathrooms for $3,500,000"
loaded_nlp = spacy.load(output_dir)
doc = loaded_nlp(test_text)

# Print NER output
for ent in doc.ents:
    print(f"{ent.text} -> {ent.label_}")

# Convert NER results to model input
def ner_output_to_model_input(doc, all_labels):
    input_dict = {label: None for label in all_labels}
    for ent in doc.ents:
        label = ent.label_
        if label in input_dict:
            input_dict[label] = ent.text
    return input_dict

parsed_input = ner_output_to_model_input(doc, LABELS)
print("\nParsed Input for Model:")
print(parsed_input)
