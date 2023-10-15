from collections import Counter
import ast
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file into a dataframe
df = pd.read_csv('data/paperlist.csv')

# Extracting keywords and counting their occurrences
keywords_list = df['keywords'].dropna().apply(ast.literal_eval).tolist()
all_keywords = [keyword for sublist in keywords_list for keyword in sublist]
keyword_counts = Counter(all_keywords)

# Get the top 20 most common keywords
top_keywords = keyword_counts.most_common(20)

# Merging keywords with different cases
keyword_counts_case_insensitive = Counter([keyword.lower() for keyword in all_keywords])

# Get the top 20 most common keywords after merging cases
top_keywords_case_insensitive = keyword_counts_case_insensitive.most_common(20)
keywords, counts = zip(*top_keywords_case_insensitive)
plt.figure(figsize=(12, 8))
plt.barh(keywords, counts, color='skyblue')
plt.xlabel('Count')
plt.title('Top 20 Keywords')
plt.gca().invert_yaxis()
plt.savefig('top_keywords.png', bbox_inches='tight')
