# LgX API v1.0 Documentation (How to?)

## AUTHENTICATION
You would be obtaining 2 tokens from the server, namely the `Access` and `Refresh` token. The access token is meant to grant you access to your resources and enable you perform authorized actions on them and it is short lived ie. 15 minutes; while the refresh token is what you use to redeem your access token when it expires. By default, refresh tokens last a day unless you set the remember_me field at login to true, which will make it live up to 2 weeks (14 days).

lgX uses the email-based login (but soon, username would be added as an optional relacement for email).

### Sign Up
```http
POST /auth/signup/
```
required fields: `email`, `password`

As for properties like: first_name, last_name, they can be used on the profile, concatenated to form the name as a whole as saved afterwards.

### Login
```HTTP
POST /auth/token/
```
required fields: `email`, `password`
optional fields: `remember_me` (Values are true or false. If set to true, will cause your refresh tokens to last 2 weeks maximum)

### Refresh Token
```HTTP
POST /auth/token/refresh/
```
No required fields, as refresh token is gotten from the cookie.

### Change Password

### Delete User

### Managing Profiles (create, update, delete)

## TOPICS
>NOTE: The `pk` of any data is the `id` of that data (topic/entry). Use this in retrieve, update or delete operations. The id of any data may look like this `f47ac10b-58cc-4372-a567-0e02b2c3d479`, which is a uuid4 value.

### List

### Retrieve
```HTTP
GET /api/topics/<topic_id>/
```
required paramters: `topic_id` (That of the topic, not any of the entries. The topic id, found in the JSON object you may have obtained.)

### Create
```HTTP
POST /api/topics/
```
required fields: `title`

optional fields: `status`(This tells if a topic is either active or is a draft or is a trash)

### Update & Partial Update
### Delete
### Categorize
### Trash

## ENTRIES
These are related to the topic such that 1 topic can have many entry objects (1:N). There are 2 url patterns you can use for this:
1. `/api/entries/` and another is a  
2. `/api/topics/<topic_id>/entries/` (This is nested url from the entry's topic)
But each have its strength and weeknesses.

### List
Say you wanted a list of all the entries you ever made (for all topics, not just one), you would likely be using the first url pattern:
```HTTP
GET /api/entries/
```
Then you wanted entries specific to a topic, you would likely be using this:
```HTTP
GET /api/topics/<topic_id>/entries/
```

### Retrieve
The 2 url pattern work fine for retrieving entry objects:
```HTTP
GET /api/entries/<entry_id>/
```
```HTTP
GET /api/topics/<topic_id>/entries/<entry_id>/
```
for convenience, you may prefer the first one.

### Create
You can only use the second url pattern, the first will give you an error
```HTTP
POST /api/topics/<topic_id>/entries/
```
required field: `text` (This is the entry text), `status` (value: ACTIVE, DRAFT or TRASH)

### Update & Partial Update
### Delete
### Categorize
### Trash

## Practical Examples (using JS)
