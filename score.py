import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import json
from article import Article

stop_words = set(stopwords.words('english'))
lemma = WordNetLemmatizer()

# Load the JSON data
with open('samples/sample-articles.json', 'r') as f:
  data = json.load(f)

# Create Article objects
articles = [Article(**article) for article in data]
print('number of articles', len(articles))
for article in articles:
  tokens = word_tokenize(article.content)
  tokens = [lemma.lemmatize(word) for word in tokens if word not in stop_words]
  article.tokens = tokens

# Get user prompt  
topic = input("What news do you want? ")
topic_tokens = word_tokenize(topic.lower())

# Compare prompt tokens to article tokens and calculate scores
scores = []
for article in articles:
  intersect = set(topic_tokens) & set(article.tokens)
  score = len(intersect)
  scores.append(score)
  print(f"Article: {article.title}, Score: {score}")

print(scores)

# Recommend article with highest score  
best_article = max(articles, key=lambda x: scores[articles.index(x)])
print("\nRecommended article:", best_article.title, "with score:", max(scores))
