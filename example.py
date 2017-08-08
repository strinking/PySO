"""
Author: Alpha-V
An Example Program That Shows The Usage Of PySO
"""

import asyncio
import pyso

def main():
    """
    Main body of code - asks for a query to search SO for and attempts to find the answer.
    """

    query = input("Please enter a search query: ")
    # Allows asynchronous code to be called from synchronous code.
    # Use the show_output function as a callback & query as the search query
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_result(show_output, query))

async def fetch_result(callback, query):
    """
    Fetches The Answer To The Provided Query And Calls The Callback With The Result.
    """

    # Creates a PySo instance with a token and the default key.
    # A PySo instance will allow you to search Stack Overflow
    search_module = pyso.PySo('YOUR TOKEN HERE')

    # Attempt to fetch the result by calling the search(some_query) method of our PySo instance
    result = await search_module.search(query)

    # Run the callback passing in the search result
    callback(result)

def show_output(result):
    """
    Prints The Question's Result Out To The User
    """

    # Was the answer fetched successfully?
    if result is None:
        print("Unable To Find An Answer!")
    else:
        # Print out the title, body & answerer's name.
        # View the documentation to see which (other) keys the result dictionary contains.
        print("{}\n{}\nAnswered by {}".format(result['title'], result['body'], result['answerer']))

if __name__ == '__main__':
    main()
