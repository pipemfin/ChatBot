import random
import nltk
import json
import sklearn
from sklearn.ensemble import RandomForestClassifier

G_UNKNOWN_ANSWER = ['Что за чушь ты несёшь?', 'Мы говорим с тобой на разных языках :(', 'Повтори ещё раз, я ничешуя не понял!']

# def clear_message(text):
#     text_lower = text.lower()
#     clear_text = ''
#     for symb in text_lower:
#         if symb in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
#             clear_text = clear_text + symb
#     return clear_text

# def get_request(message):
#     for key in G_BOT_DICTIONARY:
#         for word in G_BOT_DICTIONARY[key]['request']:
#             if nltk.edit_distance(word, message) / max(len(word), len(message)) * 100 < 40:
#                 return key
#     return 'unknown'

def bot(vectorizer_model, classifier_model, dictionary):
    while(True):
        input_message = input()
        # clean_message = clear_message(input_message)
        # request = get_request(clean_message)
        intent = get_intent_by_model(vectorizer_model, classifier_model, input_message)
        print("Категория:", intent)
        if input_message == 'unknown':
            print(random.choice(G_UNKNOWN_ANSWER))
        else:
            print(random.choice(dictionary[intent]['responses']))

def load_data():
    dictionary_file = "dictionary.json"
    with open(dictionary_file, 'r') as f:
        dictionary =  json.load(f)
    return dictionary

def vectorize(dictionary):
    x = []
    y = []
    for key in dictionary:
        for element in dictionary[key]['examples']:
            x.append(element)
            y.append(key)
    return x, y

def fit_models(dictionary):
    x, y = vectorize(dictionary)
    vectorizer_model = sklearn.feature_extraction.text.CountVectorizer()
    x_vectorized = vectorizer_model.fit_transform(x)
    classifier_model = RandomForestClassifier(random_state=42)
    classifier_model = classifier_model.fit(x_vectorized, y)
    print(classifier_model.score(x_vectorized, y))
    return vectorizer_model, classifier_model

def get_intent_by_model(vectorizer_model, classifier_model, text):
    vectorized_text = vectorizer_model.transform([text])
    return classifier_model.predict(vectorized_text)[0]

def main():
    dictionary = load_data()
    vectorizer_model, classifier_model = fit_models(dictionary)
    bot(vectorizer_model, classifier_model, dictionary)


if __name__== '__main__':
    main()
