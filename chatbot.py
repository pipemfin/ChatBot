import logging
import pickle
import json
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет, я чат-бот, основанный на алгоритмах машинного обучения!\n\
    Пообщаемся? Я могу посоветовать фильм, или расссказать анекдот!\n\
    Попробуй написать мне что-нибудь ;)')


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Смелее, просто напиши мне что-нибудь!')

def get_intent_by_model(vectorizer_model, classifier_model, text):
    print(type(vectorizer_model))
    vectorized_text = vectorizer_model.transform([text])
    return classifier_model.predict(vectorized_text)[0]

def echo(update: Update, context: CallbackContext, vectorizer, classifier, dictionary) -> None:
    answer = random.choice(dictionary[get_intent_by_model(vectorizer, classifier, update.message.text)]['responses'])
    print(answer)
    update.message.reply_text(answer)

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
    vectorizer_model = CountVectorizer()
    x_vectorized = vectorizer_model.fit_transform(x)
    classifier_model = RandomForestClassifier(random_state=42)
    classifier_model = classifier_model.fit(x_vectorized, y)
    print(classifier_model.score(x_vectorized, y))
    return vectorizer_model, classifier_model

# def load_models():
#     vectorizer = open('vectorizer_model', 'rb')
#     classifier = open('classifier_model', 'rb')
#     vectorizer_model = pickle.load(vectorizer)
#     classifier_model = pickle.load(classifier)
#     vectorizer.close()
#     classifier.close()
#     return vectorizer_model, classifier_model


def main() -> None:
    """Start the bot."""
    dictionary = load_data()
    vectorizer, classifier = fit_models(dictionary)

    # Create the Updater and pass it your bot's token.
<<<<<<< HEAD
    updater = Updater("")
=======
    updater = Updater("token")
>>>>>>> 0f24a6c... little changes

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, lambda bot, update: echo(bot, update, vectorizer, classifier, dictionary)))

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
