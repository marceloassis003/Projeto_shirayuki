import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pywhatkit
from bs4 import BeautifulSoup
import requests
import json
import pyowm
from pyowm import OWM
from pyowm.utils import timestamps



##################### CHAMADA API Open Weather ##########################
api_key = OWM("0b62da7cd0e63d276804fd297f8dff9a")
mgr = api_key.weather_manager()




audio = sr.Recognizer()
maquina = pyttsx3.init()


def executa_comando():
    try:
        with sr.Microphone() as source:
            print('Escutando...')
            audio.adjust_for_ambient_noise(source)
            voz = audio.listen(source)
            comando = audio.recognize_google(voz, language='pt-BR')
            comando = comando.lower()
            if 'shirayuki' in comando:
                comando = comando.replace('shirayuki', '')
                maquina.say(comando)
                maquina.runAndWait()

    except:
        print('Microfone não esta conectado !')

    return comando

# definições para infromar o valor do bitcoin
urlbt = "https://coinmarketcap.com/currencies/bitcoin/"

resp = requests.get(urlbt)
html = resp.text
soup = BeautifulSoup(html, "html.parser")
valorbt = soup.find("div", {"class": "priceValue"}).text.strip()




def comando_voz_usuario():
    comando = executa_comando()
    if 'horas' in comando:
        hora = datetime.datetime.now().strftime('%H:%M')
        maquina.say('São' + hora)
        maquina.runAndWait()
    elif 'dia' in comando:
        dia = datetime.date.today().strftime('%A, %d. %B %Y')
        maquina.say('Hoje é' + dia)
        maquina.runAndWait()
    elif 'previsão' in comando:
        with sr.Microphone() as source:
            audio.adjust_for_ambient_noise(source)
            # usuario fale sua localização
            maquina.say("Para qual localidade ?")
            print("aguardando...........")
            maquina.runAndWait()
            # escuta o usuario
            escutar = audio.listen(source)
            # converte entrada em texto
            localizacao = audio.recognize_google(escutar, language='pt-BR')
            maquina.say(f"você disse {localizacao}")
            print('Processando........')
            maquina.runAndWait()

            try:

                # obtem objeto de observação para loalizaçao informada
                observacao = mgr.weather_at_place(localizacao)

                # obtem o objeto previsão de observação
                previsao = observacao.weather

                # obtem a decrição do tempo (exemplo 'nublado')
                descricao = previsao.detailed_status


                # obtem a temperatura em celsius
                temperatura = previsao.temperature('celsius')['temp']
                # obtem a temperatura maxima
                maxima = previsao.temperature('celsius')['temp_max']
                # obtem o nivel de humidade do ar
                humidade = previsao.humidity



                # fala para o usuario a previsão
                texto = f"A previsão do tempo para {localizacao} é {descricao} com a temperatura de {temperatura:.1f} graus celsius, com maxima {maxima}," \
                        f" e humidade {humidade}"
                print(texto)
                maquina.say(texto)
                maquina.runAndWait()


            except pyowm.APIResponseError:
                maquina.say(
                    f"Não foi possível encontrar a localização {localizacao}. Por favor, verifique se a ortografia está correta.")
                maquina.runAndWait()

            except sr.UnknownValueError:
                maquina.say("Não consegui compreender o que você disse.")
                maquina.runAndWait()

            except sr.WaitTimeoutError:
                maquina.say("Não foi possivel conectar ao serviço de reconhecimento de fala, tente novamente")
                maquina.runAndWait()

            except sr.RequestError:
                maquina.say("Não foi possivel conectar ao serviço de reconhecimento de fala, tente novamente")
                maquina.runAndWait()
    elif 'bitcoin' in comando:
        maquina.say(f"o valor atual do Bitcoin é {valorbt} dolares.")
        print(valorbt)
        maquina.runAndWait()
    elif 'procure por' in comando:
        procurar = comando.replace('procure por', '')
        wikipedia.set_lang('pt')
        resultado = wikipedia.summary(procurar, 2)
        print(resultado)
        maquina.say(resultado)
        maquina.runAndWait()
    elif 'toque' in comando:
        musica = comando.replace('toque', '')
        resultado = pywhatkit.playonyt(musica)
        maquina.say('Tocando musica')
        maquina.runAndWait()
    elif 'lista de compras' in comando:
        lista_compras = []

        while True:
            maquina.say("o que você gostaria de adicionar á lista de compras mestre?")
            print("Processando......")
            maquina.runAndWait()

            with sr.Microphone() as source:
                audio.adjust_for_ambient_noise(source)
                escutar = audio.listen(source)

            item = audio.recognize_google(escutar, language='pt-BR')
            maquina.say(f"Adicionado {item} á lista de compras mestre.")
            maquina.runAndWait()

            lista_compras.append(item)

            maquina.say('Deseja adicionar mais algum item à lista de compras mestre?')
            maquina.runAndWait()

            with sr.Microphone() as source:
                audio.adjust_for_ambient_noise(source)
                escutar = audio.listen(source)

            resposta = audio.recognize_google(escutar, language='pt-BR')
            if 'não' in resposta or 'nada' in resposta:
                break
        if lista_compras:
            maquina.say('Aqui está a sua lista de compras mestre:')
            maquina.runAndWait()

            for item in lista_compras:
                maquina.say(item)
                maquina.runAndWait()
        else:
            maquina.say('A lista de compras esta vazia mestre.')
            maquina.runAndWait()

    elif 'bom dia' in comando:
        maquina.say('bom dia mestre')
        maquina.runAndWait()
    elif 'boa tarde' in comando:
        maquina.say('boa tarde mestre')
        maquina.runAndWait()
    elif 'boa noite' in comando:
        maquina.say('boa noite mestre')
        maquina.runAndWait()






comando_voz_usuario()