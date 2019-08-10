from enum import Enum
import wikipedia
import re
from googletrans import Translator
import unidecode
import pyowm
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import requests
from io import BytesIO
import tempfile

from telebot.credentials import OWM_KEY

class State(Enum):
    TEXT = 'text'
    PHOTO = 'photo'
    ERROR = 'error'

class Engine:
    def __init__(self):
        wikipedia.set_lang('pl')
        self.translator = Translator()
        self.image_ext = ['jpg', 'jpeg', 'png', 'gif']
        self.owm = pyowm.OWM(API_key=OWM_KEY, subscription_type='free')
        self.owm.set_language('pl')

    def get_welcome(self):
        bot_welcome = """
        Cześć! Pisz śmiało, spróbuję dotrzymać Ci towarzystwa ;)
        """

        return [(State.TEXT, bot_welcome)]

    def get_wikipedia(self, text):
        answer = []

        try:
            page = wikipedia.page(text)

        except Exception as e:
            if type(e) == wikipedia.exceptions.DisambiguationError:
                return [(State.ERROR, 'Spróbuj doprecyzować, bo nie pomogę :P')]
            elif type(e) == wikipedia.exceptions.PageError:
                return [(State.ERROR, 'Sorka, ale nie znalazłem tego hasła')]

        text = ' '.join(''.join(re.sub(r'\(.*?\)', '',page.summary).split('\n')[0]).split())

        answer.append((State.TEXT, text))

        if len(page.images) > 0:
            if page.images[0].split('.')[-1] in self.image_ext:
                answer.append((State.PHOTO, page.images[0]))

        return answer

    def get_translator(self, text, dest):
        return [(State.TEXT, self.translator.translate(text, dest=dest).text)]

    def get_weather(self, city):
        _city = unidecode.unidecode(city)
        obs = self.owm.weather_at_place(_city).get_weather()

        img = Image.new("RGB", (400,150), (0,0,0))
        unicode_font = ImageFont.truetype("DejaVuSans.ttf", 42)

        response = requests.get(obs.get_weather_icon_url())
        ico = Image.open(BytesIO(response.content))
        ico = ico.resize((100, 100))

        draw  =  ImageDraw.Draw(img)
        city = city[0].upper()+city[1:]
        city = city.split()[0]
        draw.text((30,30), city, font=unicode_font, fill=(255,255,255))
        draw.text((30,80), '{}°C'.format(obs.get_temperature('celsius')['temp']), font=unicode_font, fill=(255,255,255))
        img.paste(ico,(300,25))

        img.save('temp.png', format='PNG')

        file = open('temp.png', 'rb')

        return [(State.PHOTO, file)]



    def get_answer(self, chat_id, text):
        answer = []
        answer.append((State.TEXT, 'XDD'))

        return answer