"""
Author: Alpha-V
"""

import asyncio
import aiohttp
import ujson
import async_timeout
from .helpers import *

class PySo:
    def __init__(self, access_token, key='uKDJS)Ck32rrSYrweVOoOQ(('):
        """
        Creates a PySO instance that allows you to search Stack Overflow.
        
        access_token: string | your stack exchange access token
        key: string | your application's key. Default has been set to the PySO app.
        """

        self.credentials = (key, access_token)

    async def search(self, query):
        """ 
        Searches stack overflow for an answer to the provided query and returns a StackAnswer object containing the result.
        query: string | text to search Stack Overflow for
        """

        async with aiohttp.ClientSession() as session:
            # Find a question matching the query
            question = await find_question(self.credentials, session, query)

            # Grab the the first (top-voted) answer
            answer_id = question.get("items", [{}])[0].get('accepted_answer_id', -1)

            # Grab the answer's JSON
            answer = await fetch_answer(self.credentials, session, answer_id)
            
            if answer.get('items', None) == None or len(answer.get('items')) == 0:
                return None

            # Convert the answer's JSON into a StackAnswer object
            answer_dict = {
                    'link': answer['items'][0].get('share_link', "Not Found!"), 
                    'body': answer['items'][0].get('body_markdown', "Not Found!"), 
                    'answerer': answer['items'][0].get('owner', {}).get('display_name', "Not Found!"), 
                    'title': question['items'][0].get('title', "Not Found!"), 
                    'score': answer['items'][0].get('score', "Not Found!"),
                    'answerer_profile_image': answer['items'][0].get('owner', {}).get('profile_image', "https://cdn.discordapp.com/avatars/196989358165852160/b7645b3661eaf16bb2510c2292057890.png?size=256")
            }

            # Debug log if required
            #print("Link => {}\nBody => {}\nUsername => {}\nTitle => {}\nScore => {}\n".format(answer['link'], answer['body'], answer['answerer'], answer['title'], answer['score']))

            return answer_dict

