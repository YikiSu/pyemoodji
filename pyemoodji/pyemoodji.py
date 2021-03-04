# Python script for pyemoodji package

import nltk
nltk.download("stopwords")
from nltk.tokenize import TweetTokenizer, RegexpTokenizer
from nltk import word_tokenize
import pandas as pd
import text2emotion as te
from nltk.corpus import stopwords
import altair as alt

def text_counter(text):
    """
    Counts the number of characters, words and sentences of a string.

    Parameters:
    -----------
        text (str): A text string which could contain any number
        of english words

    Returns:
    --------
        [dictionary]: A dictionary containing the number of characters,
        words and sentences. They could be indexed by using ['characters'],
        ['words'] and ['sentences']

    example:
        text_counter("I am very happy")
        returns: {'characters':15,'words':4,'sentences':1}
    """
    return None
  

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

  
def textsentiment_to_emoji(text):
    """
    Detect the word sentiments of a text and replace the
    with the matching emojis.

    Parameters:
    -----------

        text (str): A text string containing english words

    Returns:
    --------
        [str]: A string containing only emoji's with no words.
            The emojis are written in the CLDR short name format.

    example:
        textsentiment_to_emoji("I am very happy")
        returns: "\N{smiling face with smiling eyes}"
    """
    return None


def sentiment_plot(text, sentiment = "Happy", n=10, width=10, height=10):
    """
    Generates a plot to show the top n sentiment words in the input text file.

    Parameters:
    -----------
        text (str): the input text for sentiment analysis
        sentiment (str, optional): the sentiment that the analysis focuses on. Defaults to "happy".
        n (int, optional): the number of sentiment words to show in the plot
        width (int, optional): the width of the output plot. Defaults to 10.
        height (int, optional): the height of the output plot. Defaults to 10.
    
    Returns:
    --------
        graph: a plot that shows the top n sentiment words of the input text file
    """

    sen_list = ["all", "Happy", "Sad", "Surprise", "Fear", "Angry"]
    
    if not type(text) is str:
        raise TypeError("Only strings are allowed for function input")
    elif not type(sentiment) is str:
        raise TypeError("Only strings are allowed for sentiment input")
    elif not type(width) is int:
        raise TypeError("Only integers are allowed for width input")
    elif not type(height) is int:
        raise TypeError("Only integers are allowed for height input")
    elif sentiment not in sen_list:
        raise Exception("Input not in ['all', 'Happy', 'Sad', 'Surprise', 'Fear', 'Angry']")
    



    df = sentiment_df(text, sentiment = sentiment)
    df = df.sort_values(by=['emotion_percentage'], ascending=False)
    df = df[0:10]

    title = "Top 10 " + sentiment + " Words"
    sentiment_plot = alt.Chart(df, title = title).mark_bar().encode(
        x=alt.X('word', title = 'Word', axis=alt.Axis(labelAngle=-45)),
        y=alt.Y('word_count', title = 'Word Count in Text'),
        color=alt.Color("key", title = "Emotion")
    ).properties(
        width=width,
        height=height
    ).configure_axis(
        labelFontSize=15,
        titleFontSize=15
    ).configure_title(fontSize=20)

    return sentiment_plot
