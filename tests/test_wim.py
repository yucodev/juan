def wim(*words):
        for word in words:
            preout = str(word) + " in message.content.lower()-"
            nexed = preout.replace("-", " or ")
            x = " ".join(line.strip() for line in nexed
            print(x)

wim('hello', 'how are you', 'hola')

# x = "".join(wim('hello', 'hi', 'hola'))
# print(x)
