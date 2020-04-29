import pymongo
import boto3
import os


def get_product_inventory(names=None):
    print('GET PRODUCT INVENTORY')
    #mongo = pymongo.MongoClient('mongodb://localhost:27017/')
    mongo = pymongo.MongoClient('mongodb://3.19.240.27:27017/')
    print('MONGO', mongo)
    db = mongo.lr_engine
    print('DB', db)
    counter = 0
    arr = []
    for a in db.products.find():
        counter += 1
        arr.append(a['name'])
    with open('log/output.log', 'w') as log:
        for item in arr:
            print('ITEM', item)
            log.write(item + '\n')
    log.close()
    print('UPLOAD')
    s3 = boto3.client('s3')
    s3.upload_file('log/output.log', 'lrpub', 'check.log')
    print('DONE')
