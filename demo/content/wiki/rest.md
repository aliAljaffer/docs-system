# REST

REST is a style of API design. A client names a resource, and an HTTP method states the action.

| Method | Action |
|---|---|
| GET | Read |
| POST | Create |
| PATCH | Update part of a resource |
| DELETE | Remove |

A REST API names resources, not actions. `DELETE /api/tasks/7` deletes the resource at `/api/tasks/7`. The path does not contain a verb.

Mentioned in: [[four-hats/ep04]].
