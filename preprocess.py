import re


def preprocessing(text):
    text = text.replace("\t", " ")
    text = text.replace("\n", " ")
    text = re.sub(' +', ' ', text)  # remove extra whitespaces

    return text
