from pymongo import MongoClient
from bson.objectid import ObjectId

class MongoDB:
    def __init__(self, uri):
        self.client = MongoClient(uri)
        self.db = self.client['faqsdb']
        self.collection = self.db['faqs']

    def get_all_faqs(self):
        faqs = list(self.collection.find())
        for faq in faqs:
            faq['_id'] = str(faq['_id'])
        return faqs

    def get_faq_by_id(self, faq_id):
        faq = self.collection.find_one({'_id': ObjectId(faq_id)})
        if faq:
            faq['_id'] = str(faq['_id'])  
        return faq

    def create_faq(self, faq):
        return self.collection.insert_one(faq)

    def update_faq(self, faq_id, updated_data):
        return self.collection.update_one({'_id': ObjectId(faq_id)}, {"$set": updated_data})

    def delete_faq(self, faq_id):
        return self.collection.delete_one({'_id': ObjectId(faq_id)})
