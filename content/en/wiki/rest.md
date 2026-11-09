---
title: REST
category: Web
description: A style of API design where a client names a resource and an HTTP method states the action.
tags: [web, http, api]
---

# REST

REST is a style of API design. A client names a resource, and an HTTP method states the action.

| Method | Action |
|---|---|
| GET | Read |
| POST | Create |
| PATCH | Update part of a resource |
| DELETE | Remove |

A REST API names resources, not actions. `DELETE /api/tasks/7` deletes the resource at `/api/tasks/7`. The path does not contain a verb.

Mentioned in: [[four-hats/episodes/ep04-add-a-feature-with-a-test|Episode 4]].
