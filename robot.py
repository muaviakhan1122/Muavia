import pyttsx3

print("Welcome to Robo Speaker")
while True:

    if __name__ == '__main__':
        x = input("Enter what you want me to speak: ")

        engine = pyttsx3.init()
        engine.say(x)
        engine.runAndWait()
    if(x=="q"): #when user said q exit the loop and break
        engine=pyttsx3.init()
        engine.say("Bye bye friend")
        engine.runAndWait()
        break

