def word_counts(text):
    punctuation = '.,;:!?"\'()[]{}'
    counts = {}
    for token in text.split():
        token = token.lower().strip(punctuation)
        if token:
            counts[token] = counts.get(token, 0) + 1
    return counts
