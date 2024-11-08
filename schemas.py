def user_entity(item):
    return {
        "id":str(item["_id"]),
        "first_name":item["first_name"],
        "last_name":item["last_name"],
        "salary":item["salary"],
        "age":item["age"],
        "city":item["city"]

    }

def user_entities(entity):
    return [user_entity(item) for item in entity]