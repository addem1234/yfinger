# zfinger
React app that talks to a RESTful-ish API written in Python/Flask.

## API endpoints:

| Path | Method | Requires Log-in | Result |
| ----- | ----- | ----- | ----- |
| `/` | `GET` | Yes | Displays index/searchbar |
| `/me` | `GET` | Yes | Displays an object with kth `uid` and wheter the user has uploaded an image to `s3`(`personal`) |
| `/user/<user>/image` | `GET` | No | Image for user, redirects to `s3` |
| `/user/<user>/image` | `POST` | Yes | Uploads image for user to `s3` |
| `/user/<user>/image` | `DELETE` | Yes | Deletes image for user from `s3` |
| `/user/<user>/image/<size>` | `GET` | No | Resized image for user |
| `/users/<query>` | `GET`| No | Redirects to `hodis`, quering all information, displaying all matching as objects in an array |
| `/ugkthid/<ugid>` | `GET` | No | Redirects to `hodis`, displaying information of `ugKthid` as an object |
| `/user/<user>` | `GET`,`POST` | No | Redirects to `hodis`, displaying information of `uid` as an object |

If log-in is required, user will be redirected to `login.kth.se` if not already.

Information displayed in `hodis` is `ugKthid`,`uid`,`cn`,`mail`,`givenName`,`displayName`,`year` and`tag`.

## Required environment variables:
```
  AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>
  AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>
  LOGIN_API_KEY=<LOGIN_API_KEY>

## Optional
  HODIS_HOST=https://hodis.datasektionen.se
  LOGIN_HOST=https://login2.datasektionen.se
```

## Dependencies
Depends on login, hodis is refered to but not integral.

## Development
With docker installed, run `docker-compose up --build`, <localhost.datasektionen.se:5000> will be the local development version.
Will look for ENV in a file called variables.env.

## Production
See development, on production machine.

## PLs permissions
None, merely checks if user can login in, not any permissions.

