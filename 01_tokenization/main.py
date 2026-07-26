import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hello, how are you doing today?"
tokens = enc.encode(text)

# Tokens [13225, 11, 1495, 553, 481, 5306, 4044, 30]
print(tokens)

decoded = enc.decode(tokens)

# Decoded Hello, how are you doing today?
print(decoded)


