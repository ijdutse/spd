#!/usr/bin/env python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict, Counter
from datetime import datetime
import preprocessor as p
import random, os, utils, smart_open, json, codecs, pickle, time
import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedDocument, LabeledSentence
from sklearn.feature_extraction.text import HashingVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.fftpack import fft


# Example of list of Raw Data: data_sources = ['diverse_tweets1.json']

#def main():
 #   spd = Spd(data_sources) #class instantiation
  #  start = time.clock()
   # relevant_tweets = spd.detector(data_sources)
    #stop = time.clock()
    #return relevant_tweets




class Spd:
    """ some functions to accept raw files, extract relevant fields and filter our irrelevent content"""
    #def __init__(self, data_sources):
     #   self.data_sources = data_sources
    pass
        
    # first function in the class:
    def extractor(self,data_source): # accept list of files consisting of raw tweets in form of json object
        #self.data_source = data_source
        data_extracts = {'TweetID':[],'ScreenName':[],'RawTweets':[],'CreatedAt':[],'RetweetCount':[],\
                         'FollowersCount':[],'FriendsCount':[], 'StatusesCount':[],'FavouritesCount':[],\
                         'UserName':[],'Location':[],'AccountCreated':[],'Language':[],'Description':[],\
                         'UserURL':[],'VerifiedAccount':[],'CleanTweets':[],'UserID':[], 'TimeZone':[],'TweetFavouriteCount':[]}
        non_english_tweets = 0 # keep track of the non-English tweets
        with codecs.open(self.data_source, 'r') as f: # data_source is read from extractor() function
            for line in f.readlines():
                non_English = 0
                try:
                    line = json.loads(line)
                    if line['lang'] in ['en','en-gb','en-GB','en-AU','en-IN','en_US']:
                        data_extracts['Language'].append(line['user']['lang'])
                        data_extracts['TweetID'].append(line['id_str'])
                        data_extracts['RawTweets'].append(line['text'])
                        data_extracts['CleanTweets'].append(p.clean(line['text']))
                        data_extracts['CreatedAt'].append(line['created_at'])
                        data_extracts['AccountCreated'].append(line['user']['created_at'])                       
                        data_extracts['ScreenName'].append(line['user']['screen_name'])                          
                        data_extracts['RetweetCount'].append(line['retweet_count'])
                        data_extracts['FollowersCount'].append(line['user']['followers_count'])
                        data_extracts['FriendsCount'].append(line['user']['friends_count'])
                        data_extracts['StatusesCount'].append(line['user']['statuses_count'])
                        data_extracts['FavouritesCount'].append(line['user']['favourites_count'])
                        data_extracts['UserName'].append(line['user']['name'])
                        data_extracts['Location'].append(line['user']['location'])
                        data_extracts['Description'].append(line['user']['description'])
                        data_extracts['UserURL'].append(line['user']['url'])
                        data_extracts['VerifiedAccount'].append(line['user']['verified'])
                        data_extracts['UserID'].append(line['user']['id'])
                        ################
                        data_extracts['TimeZone'].append(line['user']['time_zone'])
                        data_extracts['TweetFavouriteCount'].append(line['favorite_count'])
                        #extracts['Coordinates'].append(line['coordinates'])
                    else:
                        non_english_tweets +=1
                except:
                    continue
            df0 = pd.DataFrame(data_extracts) #convert data extracts to pandas DataFrame
            df0['CreatedAt']=pd.to_datetime(data_extracts['CreatedAt'],errors='coerce') # convert to datetime
            df0['AccountCreated']=pd.to_datetime(data_extracts['AccountCreated'],errors='coerce')
            df0 = df0.dropna(subset=['AccountCreated','CreatedAt']) # drop na in datetime
            AccountAge = [] # compute the account age of accounts
            date_format = "%Y-%m-%d  %H:%M:%S"
            for dr,dc in zip(df0.CreatedAt, df0.AccountCreated):
                #try:
                dr = str(dr)
                dc = str(dc)
                d1 = datetime.strptime(dr,date_format)
                d2 = datetime.strptime(dc,date_format)
                dif = d1 - d2
                AccountAge.append(dif.days)
                #except:
                 #   continue
            df0['AccountAge']=AccountAge
            # add/define additional features ...
            df0['Retweets'] = df0.RawTweets.apply(lambda x: str(x).split()[0]=='RT' )
            df0['RawTweetsLen'] = df0.RawTweets.apply(lambda x: len(str(x))) # modified
            df0['DescriptionLen'] = df0.Description.apply(lambda x: len(str(x)))
            df0['UserNameLen'] = df0.UserName.apply(lambda x: len(str(x)))
            df0['ScreenNameLen'] = df0.ScreenName.apply(lambda x: len(str(x)))
            df0['LocationLen'] = df0.Location.apply(lambda x: len(str(x)))
            df0['Activeness'] = df0.StatusesCount.truediv(df0.AccountAge)
            df0['Friendship'] = df0.FriendsCount.truediv(df0.FollowersCount)
            df0['Followership'] = df0.FollowersCount.truediv(df0.FriendsCount)
            df0['Interestingness'] = df0.FavouritesCount.truediv(df0.StatusesCount)
            df0['BidirFriendship'] = (df0.FriendsCount + df0.FollowersCount).truediv(df0.FriendsCount)
            df0['BidirFollowership'] = (df0.FriendsCount + df0.FollowersCount).truediv(df0.FollowersCount)
            df0['NamesRatio'] = df0.ScreenNameLen.truediv(df0.UserNameLen)
            df0['CleanTweetsLen'] = df0.CleanTweets.apply(lambda x: len(str(x)))
            df0['LexRichness'] = df0.CleanTweetsLen.truediv(df0.RawTweetsLen)       
            # Remove all RTs, set UserID as index and save relevant files:
            df0 = df0[df0.Retweets.values==False] # remove retweets
            df0 = df0.set_index('UserID')
            df0 = df0[~df0.index.duplicated()] # remove duplicates in the tweet
            #df0.to_csv(data_source[:15]+'all_extracts.csv') #save all extracts as csv
            df0.to_csv(data_source[:5]+'all_extracts.csv') #save all extracts as csv 
            with open(data_source[:5]+'non_English.txt','w') as d: # save count of non-English tweets
                d.write('{}'.format(non_english_tweets))
                d.close()
        return df0

    
    def detector(self, data_sources): # accept list of raw tweets as json objects
        self.data_sources = data_sources
        for data_source in data_sources:
            self.data_source = data_source
            df0 = self.extractor(data_source)
            #drop fields not required for predicition
            X = df0.drop(['Language','TweetID','RawTweets','CleanTweets','CreatedAt','AccountCreated','ScreenName',\
                 'Retweets','UserName','Location','Description','UserURL','VerifiedAccount','RetweetCount','TimeZone','TweetFavouriteCount'], axis=1)
            X = X.replace([np.inf,-np.inf],np.nan) # replace infinity values to avoid 0 division ...
            X = X.dropna()
            # reload the trained model for use:
            spd_filter=pickle.load(open('/content/drive/My Drive/project_s/trained_rf.pkl','rb'))
            PredictedClass = spd_filter.predict(X) # Predict spam or automated accounts/tweets:
            X['PredictedClass'] = PredictedClass # include the predicted class in the dataframe
            nonspam = df0.loc[X.PredictedClass.values==1] # sort out the nonspam accounts
            spam = df0.loc[X.PredictedClass.values==0] # sort out spam/automated accounts
            #relevant_tweets = nonspam[['CreatedAt', 'CleanTweets']]
            relevant_tweets = nonspam[['CreatedAt','AccountCreated','ScreenName','Location','TimeZone','Description','VerifiedAccount','RawTweets', 'CleanTweets','TweetFavouriteCount','Retweets']]
            relevant_tweets = relevant_tweets.reset_index() # reset index and remove it from the dataframe
            #relevant_tweets = relevant_tweets.drop('UserID', axis=1) 
            # save files:
            X.to_csv(data_source[:5]+'_all_predicted_classes.csv') #save all extracts as csv, used to be 15
            nonspam.to_csv(data_source[:5]+'_nonspam_accounts.csv')
            spam.to_csv(data_source[:5]+'_spam_accounts.csv')
            relevant_tweets.to_csv(data_source[:5]+'_relevant_tweets.csv') # relevant tweets for subsequent analysis
        return relevant_tweets # or return relevant_tweets, nonspam, spam

#if __name__ =='__main__':
 #   main()
