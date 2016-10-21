import requests
import sys
import json
import pymongo
from alchemyapi import AlchemyAPI


def DBConnection(searchTerm):
    try:
        connection = MongoClient('localhost', 27017)
        dbconn = connection.get_database('reviews')
        dbconn.get_collection(collection_name):
            
        return dbconn.get_collection(collection_name)
    except:
        print("Unable to establish connection to mongoDB server")
		print("Please ensure that the mongoDB server is running on mongod process")



def AnalyzeSentiment(collection_name):
    analysisAPI = AlchemyAPI()
    dataCollection = DBConnection(collection_name)
    documents = dataCollection.find()
    reviews = []
    for document in documents:
        try:
            if document.get("sentiment", None) == None:
                analysisResponse = analysisAPI.sentiment("text", document["text"])
                documentSentiment = analysisResponse["docSentiment"]["score"]
                dataCollection.update_one({"_id":document["_id"]}, {"$set": {"sentiment": analysisResponse["docSentiment"][score]}})
            else:
                documentSentiment = document["sentiment"]["score "]

            
            reviews.append(document["text"].strip()+"\n\n***Review-Sentiment: "+documentSentiment+"***\n"+"-"*70)
        except:
            print("Unable to parse review \n")
            dataCollection.delete_one({'text':document['text']})
return reviews