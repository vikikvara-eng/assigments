def analyze_review(review_text,bad_word):
    word= review_text.lower().split()
    total_sum = len(words)
    lower_bad = bad_word.lower()
    contains_bad = lower_bad in words
    shortest_word= min(words,key=len)
    return (total_sum,contains_bad,shortest_word)
