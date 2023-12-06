import re
# import emoji
import nltk
from nltk import TweetTokenizer, WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from lib.abbreviation import abbr_dict
from openread import open_csv_twitter

# nltk.download('punkt')
# nltk.download('stopwords')


def preprocess_text(tweet:str) -> str:
    """
    1/ Tokenize the text
    2/ Remove stop words
    3/ Lemmatize the tokens
    4/ Join the tokens back into a string
    :param text: tweet
    :return: processed_text
    """

    # def replace_emoji(text):
    #     return emoji.demojize(text)

    def replace_acronyms(text, dictionary):
        """
        F to replace acronyms getted from abbreviation
        :param text:
        :param dictionary:
        :return:
        """
        for acronym, full_form in dictionary.items():
            text = text.replace(acronym, full_form)
        return text

    def remove_non_ascii(text):
        """
        F to remove non ascii
        :param text:
        :return:
        """
        return ''.join([char for char in text if ord(char) < 128])

    def remove_urls(text):
        """
        Dell URL
        :param text:
        :return:
        """
        text = re.sub(r'@\w+', '', text)
        text = re.sub(r'http\S+', '', text)
        return text

    def remove_numbers(text):
        """
        F to dell numbers
        :param text:
        :return:
        """
        return re.sub(r'\d+', '', text)

    def remove_stopwords(text):
        """
        Remove stopwords
        :param text:
        :return:
        """
        words = word_tokenize(text)
        filtered_words = [word for word in words if word not in stopwords.words('english')]
        return ' '.join(filtered_words)

    tweet = remove_urls(tweet.lower())
    tweet = remove_non_ascii(tweet)
    tweet = remove_numbers(tweet)
    tweet = replace_acronyms(tweet, abbr_dict)
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in word_tokenize(tweet)]
    processed_text = ' '.join(lemmatized_tokens)
    return remove_stopwords(processed_text)


def info(db):
    label_counts = db['label'].value_counts()
    return label_counts

#
# sts_gt_db = open_csv_twitter('lib/sts_gold_tweet.csv')
# sts_gt_db.name = 'sts_gold_tweet'
# print(sts_gt_db.name[:-4])
# # sts_gt_db['text'] = sts_gt_db['text'].apply(preprocess_text)
# # print(sts_gt_db.head())
#
#
# print(info(sts_gt_db))
