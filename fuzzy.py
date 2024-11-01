from fuzzywuzzy import process


def fuzzy_search(target_name, text):
    # Split the text into individual words
    words = text.split()

    # Join the words into a string with spaces
    text = " ".join(words)

    # Perform fuzzy search
    result = process.extractOne(target_name, [text])

    return result


# Your example text
example_text = "Once upon a time, there was someone named Joe. He was a great person, his last name was Doe."

# Search for "John Doe" in the example text
search_result = fuzzy_search("John Doe", example_text)

# Print the result
print("Match:", search_result[0])
print("Similarity:", search_result[1])
