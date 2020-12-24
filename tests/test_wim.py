def wim(*words):
        for word in words:
            preout = str(word) + " in message.content.lower() or "
            # nexed = preout.replace("-", " or ")
            # x = "\n".join(line.strip() for line in nexed)
            x = "\n".join(preout)
            print(x)

wim('hello', 'how are you', 'hola')

# x = "".join(wim('hello', 'hi', 'hola'))
# print(x)
