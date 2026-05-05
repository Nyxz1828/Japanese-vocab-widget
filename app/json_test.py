import json
import urllib.request

levels = ["n5", "n4", "n3", "n2", "n1"]
all_vocab = []

for level in levels:
    url = f"https://raw.githubusercontent.com/wkei/jlpt-vocab-api/main/data-source/db/{level}.json"

    with urllib.request.urlopen(url) as response:
        vocab = json.load(response)

    all_vocab.extend(vocab)
    print(f"Loaded {level}: {len(vocab)} words")

print(f"Total words: {len(all_vocab)}")
print(all_vocab[0])