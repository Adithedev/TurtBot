import os
import discord
from discord.ext import commands
import spacy
import re
from heapq import nlargest

intents = discord.Intents.all() 
bot = commands.Bot(command_prefix=";",intents=intents)


class Model():
    # try:
    #     nlp = spacy.load("en_core_web_sm")
    # except OSError:
    #     import subprocess
    #     subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    def predict(text):
        stop_words = [ 'stop', 'the', 'to', 'and', 'a', 'in', 'it', 'is', 'I', 'that', 'had', 'on', 'for', 'were', 'was']
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)

        lemmatized_text = " ".join([token.lemma_ for token in doc])

        re_text = re.sub("[^\s\w,.]"," ",lemmatized_text)
        re_text = re.sub("[ ]{2,}"," ",re_text).lower()

        word_frequencies = {}
        for word in doc:
            if word.text not in "\n":
                if word.text not in stop_words:
                    if word.text not in word_frequencies.keys():
                        word_frequencies[word.text] = 1
                    else:
                        word_frequencies[word.text] +=1

        max_word_frequency = max(word_frequencies.values(),default=0)

        for word in word_frequencies.keys():
            word_frequencies[word] = word_frequencies[word] / max_word_frequency

        sent_tokens = [sent for sent in doc.sents]
        sent_scores = {}

        for sent in sent_tokens:
            for word in sent:
                if word.text in word_frequencies.keys():
                    if sent not in sent_scores.keys():
                        sent_scores[sent] = word_frequencies[word.text]
                    else:
                        sent_scores[sent] += word_frequencies[word.text]
   
        sentence_length = int(len(sent_tokens)*0.5)
        summary = nlargest(sentence_length,sent_scores,sent_scores.get)
        final_summary = [word.text for word in summary]
        final_summary = " ".join(final_summary)
        return final_summary
# ----------------------------------------------------------------------------------------------------

@bot.slash_command(
  name="test",
  guild_ids=[992417069675057172]
)

async def test(ctx): 
    await ctx.respond("I am Alive!!")
#-----------------------------------------------------

@bot.slash_command(
  name="text_summerizer",
  description = "Text summerizer model built by Adithegeek",
  guild_ids=[992417069675057172]
)

async def text_summerizer(ctx,text):
    prediction = Model.predict(text=text) 
    await ctx.respond(prediction)
#-----------------------------------------------------
@bot.slash_command(
  name="youtube_qna",
  description = "Youtube Qna LLM model built by Adithegeek",
  guild_ids=[992417069675057172]
)

async def youtube_qna(ctx,url,question):
    await ctx.respond("uhh.. Adi is still working on this :joy:")   








# ----------------------------------------------------------------------------------------------------
bot.run(os.environ['token'])
# ----------------------------------------------------------------------------------------------------
