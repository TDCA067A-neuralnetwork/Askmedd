"""Lightweight medical/non-medical query classifier.

The model is trained from a small built-in dataset so deployment does not
need to download or generate a model file at startup.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


MEDICAL_EXAMPLES = [
    "what are the symptoms of diabetes",
    "what causes high blood pressure",
    "how is pneumonia diagnosed",
    "what are common side effects of paracetamol",
    "what does a high fever mean",
    "what is an ECG used for",
    "how does insulin work",
    "what are symptoms of anemia",
    "what is the normal blood pressure",
    "can dehydration cause dizziness",
    "what causes migraine headaches",
    "how is asthma treated",
    "what is a blood test for hemoglobin",
    "what are signs of an allergic reaction",
    "what is a bacterial infection",
    "how does the immune system work",
    "what are symptoms of flu",
    "what is cholesterol",
    "how does the heart pump blood",
    "what is a vaccine",
    "what causes stomach pain",
    "what are kidney stones",
    "how does an antibiotic work",
    "what is a thyroid test",
    "what are symptoms of dengue",
    "what is first aid for a burn",
    "what is CPR",
    "what does blood oxygen saturation mean",
]

NON_MEDICAL_EXAMPLES = [
    "write a python program",
    "what is the capital of france",
    "tell me a joke",
    "write an email to my teacher",
    "what is the weather today",
    "how do I cook pasta",
    "recommend a movie",
    "who won the cricket match",
    "explain machine learning",
    "how to make a website",
    "write a love story",
    "what is the price of a phone",
    "translate this sentence",
    "help me with my homework in mathematics",
    "what is photosynthesis",
    "how do I edit a video",
    "give me travel advice",
    "what is the best laptop",
    "write a resume",
    "what is the meaning of a word",
    "how to use excel",
    "tell me about a famous actor",
    "give me a business idea",
    "how to learn guitar",
    "what is cryptocurrency",
    "write a social media caption",
]


class MedicalQueryClassifier:
    def __init__(self):
        texts = MEDICAL_EXAMPLES + NON_MEDICAL_EXAMPLES
        labels = [1] * len(MEDICAL_EXAMPLES) + [0] * len(NON_MEDICAL_EXAMPLES)
        self.pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), lowercase=True)),
            ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced")),
        ])
        self.pipeline.fit(texts, labels)

    def predict(self, question: str):
        probabilities = self.pipeline.predict_proba([question])[0]
        medical_probability = float(probabilities[1])
        non_medical_probability = float(probabilities[0])

        # A conservative threshold helps prevent unrelated questions from
        # reaching the medical LLM.
        is_medical = medical_probability >= 0.60
        confidence = medical_probability if is_medical else non_medical_probability
        return {
            "is_medical": is_medical,
            "label": "medical" if is_medical else "non-medical",
            "confidence": round(confidence, 3),
        }
