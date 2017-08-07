import aiohttp
import ujson
import async_timeout

async def fetch_answer(credentials, session, id):
    """
    (internal function) Fetches the json of an answer with the provided id
    session: asyncio HTTP client session
    id: id of the answer to look of
    """

    with async_timeout.timeout(2):
        # Set up search parameters & a custom filter to get the right fields.
        params = {'order': 'desc', 'sort': 'votes', 'site': 'stackoverflow', 'filter': '!*c891_gm3k)VJfVnZ1wmTSNzvYc7NzX-F4J3j', 'access_token': credentials[1], 'key': credentials[0]}

        # Set up a question get url & call the SE API with this url + the above parameters
        url = "https://api.stackexchange.com/2.2/answers/" + str(id)
        async with session.get(url, params=params) as resp:
            return await resp.json()

async def find_question(credentials, session, query):
    """
    (internal function) Get's the best rated stack overflow question matching the provided query
    session: asyncio HTTP client session
    query: text to search SO for
    """

    with async_timeout.timeout(2):
        # Set up the parameters and tokens/keys for grabbing a SO answer
        params = {'page': 1, 'pagesize' : 1, 'order': 'desc', 'sort': 'votes', 'site': 'stackoverflow', 'accepted' : 'true', 'q': query, 'access_token': credentials[1], 'key': credentials[0]}
        # Set up a search url & call the SE API with this url + the above parameters
        url = "https://api.stackexchange.com/2.2/search/advanced"
        async with session.get(url, params=params) as resp:
            return await resp.json()

