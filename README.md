# pyndico
Very basic python wrapper for the Indico conferencing and organisation tool

## Usage

### Setup:
```
import pyndico
pyndico = pyndico.Pyndico(
                  'my.indico-server.com', 
                  api_key = API_KEY, 
                  secret_key = SECRET_KEY)
 ```
 The url to the indico server is required, but the key arguments are optional. For most queries, the `api_key` will be required.
 
 ### Getting data:
 There are three methods, `Pyndico.get_event()`, `Pyndico.get_category()` and `Pyndico.get_room()`. These are abstractions of the method `Pyndico.get()` which can be used for general calls where the type of data is set manually, with the key word argument `qtype`. e.g `Pyndico.get(qtype = 'room', ...)`
 **Example queries:**
 ```
 response = pyndico.get_category(
                          qtype_id: '6734', #category ID
                          from = 'today'
                          to = 'tomorrow'
                          )
 ```
 `response` will be a json response where `response['result']` will be a list of all the events in the time range specified.
 
 **Typical event structure:**
 ```
 >> response['results'][0]'keys()
 [u'startDate',
 u'endDate',
 u'creator',
 u'hasAnyProtection',
 u'roomFullname',
 u'references',
 u'modificationDate',
 u'timezone',
 u'id',
 u'category',
 u'title',
 u'note',
 u'location',
 u'_fossil',
 u'type',
 u'categoryId',
 u'folders',
 u'_type',
 u'description',
 u'roomMapURL',
 u'material',
 u'visibility',
 u'address',
 u'creationDate',
 u'room',
 u'url',
 u'chairs']
```
## Common parameters
from https://indico.readthedocs.io/en/latest/http_api/common/
| **Param**  | **Short** | **Description**                                                                                                                                      |
|------------:|-----------:|------------------------------------------------------------------------------------------------------------------------------------------------------:|
| from/to    | f/t       | YYYY-MM-DD[THH:MM], ‘today’, ‘yesterday’, ‘tomorrow’ ‘now’, days in the future/past: ‘[+/-]DdHHhMMm’  |
| pretty     | p         | Pretty-print the output. When exporting as JSON it will include whitespace to make the json more human-readable.                                     |
| onlypublic | op        | Only return results visible to unauthenticated users when set to yes.                                                                                |
| onlyauthed | oa        | Fail if the request is unauthenticated for any reason when this is set to yes.                                                                       |
| cookieauth | ca        | Use the Indico session cookie to authenticate instead of an API key.                                                                                 |
| limit      | n         | Return no more than the X results.                                                                                                                   |
| offset     | O         | Skip the first X results.                                                                                                                            |
| detail     | d         | Specify the detail level (values depend on the exported element)                                                                                     |
| order      | o         | Sort the results. Must be one of id, start, end, title.                                                                                              |
| descending | c         | Sort the results in descending order when set to yes.                                                                                                |
| tz         | -         | Assume given timezone (default UTC) for specified dates. Example: Europe/Lisbon.  
 
