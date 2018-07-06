# -*- coding: utf-8 -*-
""" 
@author: Andy 
@software: PyCharm 
@file: mongo_test.py 
@time: 2018/7/4 9:31 
"""
from pymongo import MongoClient

db = MongoClient().aggregation_example
# result = db.things.insert_many([{"x": 1, "tags": ["dog"]},
#                                 {"x": 2, "tags": ["banana", "andy"]},
#                                 {"x": 3, "tags": ["cut", "apple"]}])
# print(result.inserted_ids)
from bson.son import SON

pipeline = [{"$unwind": "$tags"},
            {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
            {"$sort": SON([("count", -1), ("_id", 1)])}]
import pprint
pprint.pprint(list(db.things.aggregate(pipeline)))

pprint.pprint(db.command('aggregate', 'things', pipeline=pipeline, explain=True))
from bson.code import Code

mapper = Code("""
              function () {
                this.tags.forEach(function(z) {emit(z, 1);});
              }
              """)

reducer = Code("""
                function (key, values) {
                    var total = 0;
                    for (var i = 0; i < values.length; i++) {
                        total += values[i];
                    }
                    return total;
                }
                """)
result = db.things.map_reduce(mapper, reducer, "myresults")
for doc in result.find():
    pprint.pprint(doc)

