# Deutsch-Lernen
[![Build Status](https://travis-ci.com/Leidenschaft/DeutschLernen_server.svg?branch=master)](https://travis-ci.com/Leidenschaft/DeutschLernen_server)

This is the server side code of the project. Complete description of the project can be found under manual/Introduction.pdf with url https://github.com/Leidenschaft/Deutsch-Lernen


## Requirement
Python >= 3.6 with packages listed in `requirements.txt`.
The frontend code is organized as submodule. Use `git submodule --init update` to get the submodule contents.

# Development
* run `python3 manage.py runserver`

## Deployment
* (settings.py) Add `Word_edit` to installed app and add the absolute path of frontend code to the first of `settings.STATICFILES_DIRS`.
* (urls.py) Add `Word_edit.urls`.

## API
### Create or Update a word
url endpoint: `/Word_edit/create_new_word`

method: POST

data: using html form, ie `Stichwort=Absclussarbeit&explanation_1=thesis`.

Required field: `Stichwort` and `explanation_1`;

Suggested field: `category`, i.e. part of speech like **Substantiv**.
For the complete list of `category`, see `frontend/Wort/AdjModel.dtd`.

Optional field: `wordAddr`, the saved file path, relative the the server code.
If `wordAddr` is not provided,
the file name is computed from `category` and the number of current words automatically.

### Frontend
url endpoint: `/Word_edit/create_new_word`

method: GET

This frontend can create new words of Noun, Verben and Adjectiv for selected language. Indeed it has limitations.

Returned: HTTP Code and HTTP string. If the code is 200, the corresponding xml is created or updated; otherwise there is some failure. The error message can be checked from the returned string.
