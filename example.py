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
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_result(show_output, query))

async def fetch_result(callback, query):
    """
    Fetches The Answer To The Provided Query And Calls The Callback With The Result.
    """

    search_module = pyso.PySo('YOUR TOKEN HERE')
    result = await search_module.search(query)
    callback(result)

def show_output(result):
    """
    Prints The Question's Result Out To The User
    """

    if result is None:
        print("Unable To Find An Answer!")
    else:
        print("{}\n{}\nAnswered by {}".format(result['title'], result['body'], result['answerer']))

if __name__ == '__main__':
    main()
