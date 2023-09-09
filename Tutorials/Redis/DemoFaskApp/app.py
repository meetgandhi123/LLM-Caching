from flask import Flask, redirect, request
import redis
import json

app = Flask(__name__)


def check_cache(user_input):
    """Check for the exact phrase present in the redis queue.
    Key to match : company_role_query

    Args:
        user_input (json)

    Returns:
        _type_: response
    """
    client_key = str(user_input['company'])+"_"+str(user_input['role'])+"_"+str(user_input['query'])

    redis_client = redis.Redis(host='localhost',port=6379,db=0)
    result = redis_client.get(client_key)

    if result is None:
        print("Result not found in Cache")
        redis_client.set(client_key,"CHATGPT_Response")
        cache_response = "CHATGPT_Response"
    else:
        print("Result found in Cache")
        cache_response = result

    return cache_response

@app.route('/search_cache',methods=['POST','GET'])
def get_cache():
    """server request for handeling cache.

    Returns:
        json: procesedresponse.
    """
    if request.method == 'POST':
        user_input = request.get_json()
        company = user_input['company']
        role = user_input['role']
        query = user_input['query']        
        
        response = check_cache(user_input)
        #response = {"Company": company,"role": role,"query": query}
        return response

    else:         
        response = {"Error": "Method Not Allowed"} 
        return response
 

if __name__ == '__main__':
    app.run(debug=True)