from googletrans import Translator
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import random

duration = 10  # секунды записи
sample_rate = 44100
max_error = 3
error = 0
score = 0

words_by_level = {
    "easy": ["кот", "собака", "яблоко", "молоко", "солнце"],
    "medium": ["банан", "школа", "друг", "окно", "жёлтый"],
    "hard": ["технология", "университет", "информация", "произношение", "воображение"]
    }

print("Выбери уровень: easy, medium, hard")
level = input().lower()
while level not in words_by_level:
    print("Выбери уровень: easy, medium, hard")
    level = input().lower()

word_list = words_by_level [level]
random.shuffle(word_list)

recognizer = sr.Recognizer()
translator = Translator()

for word in word_list:
    print(word)

    print("Говори...")
    recording = sd.rec(
  int(duration * sample_rate), # длительность записи в сэмплах
  samplerate=sample_rate,      # частота дискретизации
  channels=1,                  # 1 — это моно
  dtype="int16")               # формат аудиоданных
    sd.wait()  # ждём завершения записи

    wav.write("output.wav", sample_rate, recording)
    print("Запись завершена, теперь распознаём...")

    try:
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, language="en-US").lower()
        print("Ты сказал:", text)
        
        translated = translator.translate(word, src="ru", dest="en").text.lower()  # здесь 'en' — это английский

        print("🌍 Перевод на английский:", translated)
        if text == translated:
            score += 1
            print ("Верно!")
        else:
            error += 1
            print ("Неверно!")
        if error >= max_error:
            print ("Игра окончена")
            break
    except sr.UnknownValueError:             # - если Google не понял речь (шум, молчание)
        print("Не удалось распознать речь.")
    except sr.RequestError as e:             # - если нет интернета или API недоступен
        print(f"Ошибка сервиса: {e}")
print(f"Итог игры: счёт игры{score}")