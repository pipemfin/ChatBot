import random
import nltk

G_BOT_DICTIONARY ={
    'hello':{
        'request':['привет', 'здравствуй', 'хай'],
        'response':['Приветствую тебя, Землянин!', 'Кто здесь?', 'Привет, друг!']
    },
    'bye':{
        'request':['пока', 'прощай', 'досвидания'],
        'response':['Я буду скучать', 'Надеюсь, что мы скоро увидимся?', 'Прощай.']
    },
    'how are you':{
        'request':['какдела', 'какты', 'чекого'],
        'response':['У меня всё супер, а как твои дела?', 'Могло быть и лучше!', 'Я лишь безжизненная машина, о каких дела речь?']
    },
}

G_UNKNOWN_ANSWER = ['Что за чушь ты несёшь?', 'Мы говорим с тобой на разных языках :(', 'Повтори ещё раз, я ничешуя не понял!']

def clear_message(text):
    text_lower = text.lower()
    clear_text = ''
    for symb in text_lower:
        if symb in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
            clear_text = clear_text + symb
    return clear_text

def get_request(message):
    for key in G_BOT_DICTIONARY:
        for word in G_BOT_DICTIONARY[key]['request']:
            if nltk.edit_distance(word, message) / max(len(word), len(message)) * 100 < 40:
                return key
    return 'unknown'

def bot():
    while(True):
        input_message = input()
        clean_message = clear_message(input_message)
        request = get_request(clean_message)
        if request == 'unknown':
            print(random.choice(G_UNKNOWN_ANSWER))
        else:
            print(random.choice(G_BOT_DICTIONARY[request]['response']))

def main():
    bot()

if __name__== '__main__':
    main()
