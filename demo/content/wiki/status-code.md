# Status code

A status code is the first fact a client reads from a response. It states what happened, before the client parses the body.

| Code | Meaning |
|---|---|
| 200 | OK |
| 201 | Created |
| 400 | The client sent invalid data |
| 404 | The resource does not exist |
| 500 | The server failed |

The status code is part of the API contract. A missing resource returns 404, not 200.
