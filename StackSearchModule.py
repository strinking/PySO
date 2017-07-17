"""
Author: Alpha-V
"""

import asyncio
import aiohttp
import ujson
import async_timeout

# Stack Exchange API tokens
# Use https://stackexchange.com/oauth/dialog?client_id=9997&scope=no_expiry&redirect_uri=https://stackexchange.com/oauth/login_success to get an access token tied to your account & the bot's SO app
access_token = 'SOME_ACCESS_TOKEN_HERE'
# Probably no need to change this one, unless you want to create your own SO app
key = 'uKDJS)Ck32rrSYrweVOoOQ(('

class StackAnswer:
    """
    Object to hold all of an answer

    Contains:
    body - string that contians the Markdown of the answer
    link - Link to the answer
    username - Username of the author of the answer
    title - title of the origional question
    upvotes - score of the SO answer
    """

    def __init__(self, link, body, username, title, score, profile_image):
        self.body = body
        self.link = link
        self.username = username
        self.title = title
        self.score = score
        self.user_profile_image = profile_image

async def fetch_answer(session, id):
    """
    (internal function) Fetches the json of an answer with the provided id
    session: asyncio HTTP client session
    id: id of the answer to look of
    """

    with async_timeout.timeout(2):
        # Set up search parameters & a custom filter to get the right fields.
        params = {'order': 'desc', 'sort': 'votes', 'site': 'stackoverflow', 'filter': '!*c891_gm3k)VJfVnZ1wmTSNzvYc7NzX-F4J3j', 'access_token': access_token, 'key': key}

        # Set up a question get url & call the SE API with this url + the above parameters
        url = "https://api.stackexchange.com/2.2/answers/" + str(id)
        async with session.get(url, params=params) as resp:
            return await resp.json()

async def find_question(session, query):
    """
    (internal function) Get's the best rated stack overflow question matching the provided query
    session: asyncio HTTP client session
    query: text to search SO for
    """

    with async_timeout.timeout(2):
        # Set up the parameters and tokens/keys for grabbing a SO answer
        params = {'page': 1, 'pagesize' : 1, 'order': 'desc', 'sort': 'votes', 'site': 'stackoverflow', 'accepted' : True, 'q': query, 'access_token': access_token, 'key': key}
        # Set up a search url & call the SE API with this url + the above parameters
        url = "https://api.stackexchange.com/2.2/search/advanced"
        async with session.get(url, params=params) as resp:
            return await resp.json()

async def search(query):
    """ 
    Searches stack overflow for an answer to the provided query and returns a StackAnswer object containing the result.
    query: Text to search SO for
    """

    async with aiohttp.ClientSession() as session:
        # Find a question matching the query
        question = await find_question(session, query)

        # Grab the the first (top-voted) answer
        answer_id = question.get("items", [{}])[0].get('accepted_answer_id', -1)

        # Grab the answer's JSON
        answer = None
        async with aiohttp.ClientSession() as session_thing:
            answer = await fetchAnswer(session_thing, answer_id)
        
        # Convert the answer's JSON into a StackAnswer object
        answer = StackAnswer(answer.get('items', [{}])[0].get('share_link', "Not Found!"), answer.get('items', [{}])[0].get('body_markdown', "Not Found!"), answer.get('items', [{}])[0].get('owner', {}).get('display_name', "Not Found!"), question.get('items', [{}])[0].get('title', "Not Found!"), answer.get('items', [{}])[0].get('score', "Not Found!"), answer.get('items', [{}])[0].get('owner', {}).get('profile_image', "https://cdn.discordapp.com/avatars/196989358165852160/b7645b3661eaf16bb2510c2292057890.png?size=256"))
        
        # Debug log if required
        #print("Link => {}\nBody => {}\nUsername => {}\nTitle => {}\nScore => {}\n".format(answer.link, answer.body, answer.username, answer.title, answer.score))

        return answer

