import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from collections import Counter
import matplotlib.pyplot as plt
from collections import Counter
import ast
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Download required resources
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Function to convert nltk tag to first character used by WordNetLemmatizer
def nltk_tag_to_wordnet_tag(nltk_tag):
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:          
        return None

def lemmatize_sentence(sentence):
    # Tokenize the sentence and find the POS tag for each token
    nltk_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))
    # Tuple of (token, wordnet_tag)
    wordnet_tagged = map(lambda x: (x[0], nltk_tag_to_wordnet_tag(x[1])), nltk_tagged)
    lemmatized_sentence = []
    for word, tag in wordnet_tagged:
        if tag is None:
            # If no available tag, append the token as is
            lemmatized_sentence.append(word)
        else:        
            # Else use the tag to lemmatize the token
            lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))
    return " ".join(lemmatized_sentence)

# Load the CSV file into a dataframe
df = pd.read_csv('../data/paperlist.csv')

# Extracting keywords and counting their occurrences
keywords_list = df['keywords'].dropna().apply(ast.literal_eval).tolist()
all_keywords = [keyword.lower() for sublist in keywords_list for keyword in sublist]
keyword_counts = Counter(all_keywords)

# Now lemmatize all the keywords
all_keywords_lemmatized = [lemmatize_sentence(keyword) for keyword in all_keywords]
keyword_counts_lemmatized = Counter(all_keywords_lemmatized)

top_k = 50

# Get the top k most common lemmatized keywords
top_keywords_lemmatized = keyword_counts_lemmatized.most_common(top_k)
keywords, counts = zip(*top_keywords_lemmatized)
plt.figure(figsize=(8, 12))
plt.barh(keywords, counts, color='skyblue')
plt.xlabel('Count')
plt.title(f'Top {top_k} Keywords after Lemmatization')
plt.gca().invert_yaxis()
plt.savefig('top_keywords_bar.png', bbox_inches='tight', dpi=300)

wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(keyword_counts_lemmatized)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title(f'Top {top_k} Keywords Word Cloud after Lemmatization')
plt.savefig('top_keywords_wordcloud.png', bbox_inches='tight', dpi=300)
