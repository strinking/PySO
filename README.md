# PySO
A small python module that helps you search Stack Overflow!

## Requirements
* asyncio (allows for asynchronous operation)
* asynciohttp (for async HTTP requests)
* ujson (for JSON parsing)

## Setup
To set up PySO please open https://stackexchange.com/oauth/dialog?client_id=9997&scope=no_expiry&redirect_uri=https://stackexchange.com/oauth/login_success and log in with your stack overflow account. Authorize the app and once it's done you should see a token appear in your url bar. Copy this to the _access_token_ field. You should now be ready to go!

## Usage
Call _Search(someSearchStringHere)_ to search Stack Overflow using PySO. _someSearchStringHere_ can be any string you wish to search Stack Overflow for. It'll return the best answer to the best question with an accepted answer.
