def word_frequency(text):
    text = text.lower()
    words = text.split()
    
    freq = {}
    for w in words:
        if w in freq:
            freq[w] += 1
        else:
            freq[w] = 1
    return freq

text = "hello world hello"
print(word_frequency(text))