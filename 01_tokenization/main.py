import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hey There My name is Sarthak!"

tokens = enc.encode(text);

print('Tokens',tokens)

decoded = enc.decode(tokens)

print("decoded",decoded)