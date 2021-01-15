# def wim(*words):
    # a = []
    # for word in words:
    #     preout = str(word) + " in message"
    #     a.append(preout)
    # output = " or ".join(a)
    # return output


def wim(*words):
    return any(x in message.content.lower() for x in [*words])

message = input('Type your message: ')

# if wim('hello', 'car', 'dog'):
#     print

if wim('hello', 'car', 'dog'):
    print('Yes!')
else:
    print('Nope :/')