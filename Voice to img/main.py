import speech_recognition
import pyttsx3
import requests

recognizer = speech_recognition.Recognizer()

x = input("Press enter to start the listening")

try:
    print("Listening...")
    with speech_recognition.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic, duration=0.2)
        audio = recognizer.listen(mic)

        text  = recognizer.recognize_google(audio)
        text = text.lower()

        print("Generating an image for: " + str(text))

        r = requests.post(
            "https://api.deepai.org/api/text2img",
            data={
                'text': text,
            },
            headers={'api-key': '111b1cd1-abed-4691-9422-dfdfcf818cad'}
        )

        try:
            print(r.json()["output_url"])

        except Exception as e:
            print(r.json())

except Exception as e:
    recognizer = speech_recognition.Recognizer()