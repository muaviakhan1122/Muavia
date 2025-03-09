def binary_to_text(binary):
    return ''.join(chr(int(b, 2)) for b in binary.split())
binary_input = input("Enter binary code (space-separated): ")
text_output = binary_to_text(binary_input)
print(f"Original text: {text_output}")
