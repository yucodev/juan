def wim(*words):
    for word in words:
        # preout = str(word) + " in message.content.lower()"
        # return preout
        yield str(word) + " in message.content.lower()"

print(wim('hello', 'how are you', 'hola'))

# x = "".join(wim('hello', 'hi', 'hola'))
# print(x)
