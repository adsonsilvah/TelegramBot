import os
import telebot
from dotenv import load_dotenv
import requests

load_dotenv()
API_TOKEN = os.getenv('API_KEY')
bot = telebot.TeleBot(API_TOKEN)
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

boavindas = open("arq/boasvindas.txt", "r").read()
plastico = open("arq/reciclagem_plastico.txt", "r").read()
vidro = open("arq/reciclagem_vidro.txt", "r").read()
eletronicos = open("arq/reciclagem_eletronicos.txt", "r").read()

perguntas = [
    "O que é mais reciclável? (Responda com o número da opção)\n1. Sacolas plásticas\n2. Garrafas PET",
    "Qual é o impacto principal da reciclagem? (Responda com o número da opção)\n1. Reduzir a emissão de gases do efeito estufa\n2. Aumentar a poluição do ar",
    "Qual item é considerado lixo eletrônico? (Responda com o número da opção)\n1. Lâmpadas\n2. Pilhas e baterias"
]
respostas_corretas = ['2', '1', '2']
estado_quiz = {}

def get_news():
    url = f"https://newsapi.org/v2/everything?q=sustentabilidade+OR+reciclagem&language=pt&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data['articles'][:15]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, boavindas)

@bot.message_handler(commands=['noticias'])
def noticias(message):
    articles = get_news()
    for article in articles:
        title = article['title']
        url = article['url']
        bot.send_message(message.chat.id, f"{title}\n{url}")

@bot.message_handler(commands=['reciclagem_de_plastico'])
def dicas_reciclagem_plastico(message):
    bot.send_message(message.chat.id, plastico)

@bot.message_handler(commands=['reciclagem_de_vidro'])
def dicas_reciclagem_eletronicos(message):
    bot.send_message(message.chat.id, vidro)

@bot.message_handler(commands=['reciclagem_de_eletronicos'])
def dicas_reciclagem_eletronicos(message):
    bot.send_message(message.chat.id, eletronicos)

@bot.message_handler(commands=['videos'])
def videos(message):
    video_url = "https://youtu.be/UjU0RlTzP4Y?si=5jMhaQSJlnk40Lob"
    video_url2 = "https://youtu.be/H5rbcjYYTXA?si=v32dlAH4t2BizHJW"
    video_url3 = "https://youtu.be/42rzbf_Txug?si=kcJVxHlqIE3Qkc1k"
    video_url4 = "https://youtu.be/ITur0JNJZos?si=bg84RWjJjc6Lk3CW"

    bot.send_message(message.chat.id, 'Aqui estão alguns videos sobre sustentabillidade:')
    bot.send_message(message.chat.id, f'{video_url}')
    bot.send_message(message.chat.id, f'{video_url2}')
    bot.send_message(message.chat.id, f'{video_url3}')
    bot.send_message(message.chat.id, f'{video_url4}')


@bot.message_handler(commands=['quiz'])
def iniciar_quiz(message):
    estado_quiz[message.chat.id] = {'pergunta_atual': 0, 'acertos': 0}
    bot.send_message(message.chat.id, perguntas[0])


@bot.message_handler(func=lambda message: message.chat.id in estado_quiz)
def processar_resposta(message):
    estado = estado_quiz[message.chat.id]
    if str(message.text).strip() == respostas_corretas[estado['pergunta_atual']]:
        estado['acertos'] += 1
        bot.send_message(message.chat.id, "Resposta correta! 🌟")
    else:
        bot.send_message(message.chat.id, "Ops, resposta errada. 😢")

    estado['pergunta_atual'] += 1
    if estado['pergunta_atual'] < len(perguntas):
        bot.send_message(message.chat.id, perguntas[estado['pergunta_atual']])
    else:
        bot.send_message(message.chat.id, f"Quiz finalizado! Você acertou {estado['acertos']} de {len(perguntas)}.")
        del estado_quiz[message.chat.id] 


bot.polling()