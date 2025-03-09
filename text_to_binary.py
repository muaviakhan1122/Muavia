def text_to_binary(text):
    return ' '.join(format(ord(char), '08b') for char in text)
sentence = input("Enter a sentence: ")
binary_output = text_to_binary(sentence)
print(f"Binary representation: {binary_output}")
