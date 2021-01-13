def wim(*words):
    a = []
    for word in words:
        preout = str(word) + " in message.content.lower()"
        a.append(preout)
    output = " or ".join(a)
    print(output)

wim('hello', 'how are you', 'hola')