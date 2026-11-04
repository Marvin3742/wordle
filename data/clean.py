WORDS_ALPHA = "words_alpha.txt"
WORDS = "words.txt"
with open(WORDS_ALPHA, "r") as f:
    lines = f.readlines()

with open(WORDS, "w") as f:
    for line in lines:
        if len(line) == 6:
            f.write(line)