"""
Author: Alpha-V
"""

import aiohttp
from .helpers import fetch_answer, find_question


class PySo:
    """
    Class that allows you to search Stack Overflow.
    """

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
            
            if answer.get('items', None) is None or len(answer.get('items')) == 0:
                return None

            # Convert the answer's JSON into a StackAnswer object
            first_answer = answer['items'][0]
            answer_dict = {
                'link': first_answer.get('share_link', "Not Found!"), 
                'body': first_answer.get('body_markdown', "Not Found!"), 
                'answerer': first_answer.get('owner', {}).get('display_name', "Not Found!"), 
                'title': question['items'][0].get('title', "Not Found!"), 
                'score': first_answer.get('score', "Not Found!"),
                'answerer_profile_image': first_answer.get('owner', {}).get('profile_image', "Not Found!")
            }

            # Debug log if required
            #print("Link => {}\nBody => {}\nUsername => {}\nTitle => {}\nScore => {}\n".format(answer['link'], answer['body'], answer['answerer'], answer['title'], answer['score']))

            return answer_dict

