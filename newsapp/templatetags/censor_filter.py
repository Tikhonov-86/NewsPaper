from django import template

import string

register = template.Library()

forbidden_words = ["редиска", "редиски", "редиска!", "редиски!"]

# @register.filter()
# def censor(text):
#     text_list = text.split()
#     censored_text_list = []
#
#     for word in text_list:
#         clean_word = ''.join(c for c in word if c not in string.punctuation)
#         if clean_word.lower() in bad_words:
#             censored_word = clean_word[0] + (len(clean_word) - 1) * '*'
#             censored_text_list.append(word.replace(clean_word, censored_word))
#         else:
#             censored_text_list.append(word)
#     return ' '.join(censored_text_list)


# text = "Нехороший человек — редиска!"
#
# censored_text = censor(text)
# print(censor(text))


@register.filter
def censor(value):
    words = value.split()
    result = []

    for word in words:
        if word in forbidden_words:
            result.append(word[0] + "*"*(len(word)-2) + word[-1])
        else:
            result.append(word)
    return " ".join(result)

