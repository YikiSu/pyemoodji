import nltk
nltk.download("stopwords")
from nltk.tokenize import TweetTokenizer, RegexpTokenizer
from nltk import word_tokenize
import pandas as pd
import text2emotion as te
from nltk.corpus import stopwords

def sentiment_df(text, sentiment="all"):
    """
    Generates a sentiment analysis summary dataframe of the input text. The summary dataframe would include 
    the sentiment type, sentiment words, percentage of sentiments and highest sentiment percentage.
    Parameters:
    -----------
        text (str): the input text for sentiment analysis
        sentiment (str, optional): the sentiment that the analysis focuses on, could be happy, positive or sad etc. Defaults to "all".
    Returns:
    --------
        data frame: a data frame that contains the summary of sentiment analysis
    """
    sen_list = ["all", "Happy", "Sad", "Surprise", "Fear", "Angry"]
    
    if not type(text) is str:
        raise TypeError("Only strings are allowed for function input")
    elif not type(sentiment) is str:
        raise TypeError("Only strings are allowed for sentiment input")
    elif sentiment not in sen_list:
        raise Exception("Input not in ['all', 'Happy', 'Sad', 'Surprise', 'Fear', 'Angry']")

    
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    word_list = tokenizer.tokenize(text)

    stop_words = set(stopwords.words("english"))

    cleaned_list = []

    for i in word_list:
        if i not in stop_words:
            cleaned_list.append(i)
    
    count_dict = {}
    for i in cleaned_list:
        count_dict[i] = cleaned_list.count(i)


    df = pd.DataFrame()
    for i in set(cleaned_list):
        df_current = pd.DataFrame()
        dictionary = te.get_emotion(i)
        df_current = pd.DataFrame(dictionary, index = [i])
        if sum(dictionary.values()) == 0:
            df_current["key"] = "None"
        else:
            key = max(dictionary, key=dictionary.get)
            df_current["key"] = key
        df = pd.concat([df, df_current])

    df['emotion_count'] = df.sum(axis=1)

    for i in list(df.index):
        df.loc[i, "word_count"] = count_dict[i]
    df = df.reset_index().rename(columns={'index':'word'})

    df['dummy'] = df['emotion_count'] * df['word_count']
    total_emotion = df['dummy'].sum()
    
    df['emotion_percentage'] = df['dummy'] / total_emotion

    if sentiment == "all":
        return df[["word", "key", "emotion_count", "emotion_percentage", "word_count"]]
    else:
        df = df[df["key"] == sentiment]
        return df[["word", "key", "emotion_count", "emotion_percentage", "word_count"]]

    return df