from textblob import TextBlob


class SentimentBot:
    def get_sentiment(self, text):
        try:
            blob = TextBlob(text)
            score = blob.sentiment.polarity

            if score > 0.1:
                return "Positive", "😊"
            elif score < -0.1:
                return "Negative", "😡"
            else:
                return "Neutral", "😐"
        except:
            return "Neutral", "😐"