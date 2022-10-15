import AutoFAQ
import GoogleSheets
import telebot
from telebot import types


#готовим токены из ttoken.txt и groken.txt
def prepare_token(filename):
    file=open(filename, 'r')
    token=file.read()
    file.close()
    return token

ttoken=prepare_token('ttoken.txt')
gtoken=prepare_token('gtoken.txt')
bot=telebot.TeleBot(ttoken)
problem_user=[]
question_user=[]
    
@bot.message_handler(commands=['start'])
def start(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Обратная связь.")
    item2=types.KeyboardButton("Вопрос.")
    markup.add(item1)
    markup.add(item2)
    bot.send_message(message.chat.id,'Если Вы не получили ответ на свой вопрос или он оказался некорректным, то через обратную связь можете сообщить об этом.',reply_markup=markup)
    bot.send_message(message.from_user.id, "Какой у Вас имеется ко мне вопрос?")

@bot.message_handler(content_types=['text'])
def message_listener(message):
    if message.chat.type=="private":
        if(message.text=="Обратная связь." and message.from_user.id not in problem_user):
            problem_user.append(message.from_user.id)
            bot.send_message(message.from_user.id, "Какой у Вас вопрос? Был ли ответ некорректным или не оказался исчерпывающим?")
        elif(message.from_user.id in problem_user):
            print("Проблема у "+message.from_user.id+": "+message.text)
            problem_user.remove(message.from_user.id)
            bot.send_message(message.from_user.id, "Понял! Ожидайте, вскоре Вам ответят.")
        elif(message.text=="Вопрос." and message.from_user.id not in question_user):
            question_user.append(message.from_user.id)
            bot.send_message(message.from_user.id, "Какой у Вас вопрсо ко мне?")
        elif(message.from_user.id in question_user):
            question_user.remove(message.from_user.id)
            try:
                question=AutoFAQ.cleanRequest(message.text)
                question_embedding=AutoFAQ.bert_model.encode([question])
                answer=AutoFAQ.autoFAQ(question_embedding, AutoFAQ.sent_bertphrase_embeddings, AutoFAQ.df, AutoFAQ.cleaned_questions, AutoFAQ.min_similarity)
                if answer==[]:
                    bot.send_message(message.from_user.id, "К сожалению, я пока ещё не знаю ответа на этот вопрос! Обратитесь в поддержку, чтобы моя база пополнилась.")
                bot.send_message(message.from_user.id, answer)
            except:    
                print("Неизвестная доселе ошибка, сударь!")
                bot.send_message(message.from_user.id, "К сожалению, я пока ещё не знаю ответа на этот вопрос! Обратитесь в поддержку, чтобы моя база пополнилась.")

try:
    bot.polling(none_stop=True, interval=0)
except KeyboardInterrupt:
    sys.exit()