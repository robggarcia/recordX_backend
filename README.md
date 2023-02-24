# RecordX API Documentation

## Introduction

The goal of recordX is to provide music lovers a space to connect with other music lovers while discovering and purchasing new music. We strive to provide you with an easy to consume API, so you can build out beautiful front end experiences and leave the Data management to us.
We have a small handful of endpoints, each documented below.

### Authentication through JSON Web Tokens

When using the API, many calls are made in the context of a registered user. The API protects itself by requiring a token string passed in the Header for requests made in that context.
A sample request with an authorization token looks like this:

```
fetch('https://recordxapi.render.com/api/users',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'x-access-token': 'TOKEN_STRING_HERE'
  },
  body: JSON.stringify({/* whatever things you need to serve*/})
})
```

The token string will be provided either by registering or logging in. Deviating from this format will result in an error.
If the token is malformed, missing, or has been revoked, you will get a
response specific to that.

```
{
  "success": False,
  "message": "You must be logged in to perform this action"
}
```

### General Return Schema

ERROR

```
{
  "success": False,
  "message": "Invalid request"
}
```

SUCCESS

```
{
  "success": True,
  "message": "User successfully updated",
  "data": {/*updated or created data entry from specific request*/}
}
```

## User Endpoints

### **POST /api/users/register**

This route is used to create a new user account. On success, you will be given a JSON Web Token to be passed to the server for requests requiring authentication.

**Request Parameters**

- username (string, required): the desired username for the new user
- email (string, required): the desired email for the new user
- password (string, required): the desired password for the new user

**Return Parameters**

- data (object)
  - \_id (ObjectId): the database identifier of the user
  - username (string): the username of the user
  - email (string): the email of the user
- message (string): the success message
- success (boolean): notification if request was successful

**Sample Call**

```
fetch('https://recordxapi.render.com/api/users/register', {
  method: "POST",
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    username: 'Robbie',
    email: 'robbie3@me.com',
    password: 'r0bb13!'
  })
})
```

**Sample Response**

If the API creates a new user, the following object will be returned:

```
{
  "data": {
    "_id": 23098sdf09s0823028,
    "email": "robbie3@me.com",
    "username": "Robbie"
  }
  "message": "User successfuly created",
  "success": True,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
}
```

### **POST /api/users/login**

This route is used for a user to login when they already have an account. On success, you will be given a JSON Web Token to be passed to the server for requests requiring authentication.

**Request Parameters**

- email (string, required): the registered email for the user
- password (string, required): the matching password for the user

**Return Parameters**

- data (object)
  - \_id (ObjectId): the database identifier of the user
  - username (string): the username of the user
  - email (string): the email of the user
- message (string): the success message
- success (boolean): notification if request was successful

**Sample Call**

```
fetch('https://recordxapi.render.com/api/users/login', {
  method: "POST",
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email: 'robbie3@me.com',
    password: 'r0bb13!'
  })
})
```

**Sample Response**

If the API authenticates the email and password, the following object
will be returned:

```
{
  "data": {
    "_id": 23098sdf09s0823028,
    "email": "robbie3@me.com",
    "username": "Robbie"
  }
  "message": "User successfuly logged in",
  "success": True,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
}
```

### **GET /api/users** \*Admin required

Returns a list of all users in the database

**Request Parameters**

There are no request parameters

**Return Parameters**

(array of objects):

- \_id (ObjectId): This is the database identifier for the user
- username (string): This is the name of the user
- email (string): This is the email of the user
- admin (boolean): This value specifies if the user is an admin or not

**Sample Call**

```
fetch('https://recordxapi.render.com/api/users', {
  headers: {
    'Content-Type': 'application/json',
  },
})
```

**Sample Response**

```
{
  "data": [
    {
      "_id": "63f56017aa62ef6e9c5f1535",
      "admin": true,
      "email": "rob@test.com",
      "username": "rob"
    },
    {
      "_id": "63f56017aa62ef6e9c5f3284",
      "email": "stanley@test.com",
      "username": "stanley"
    },
  ],
  "success": true
}
```

### **GET /api/users/:userId**

This route is used to grab an already logged in user's relevant data. It is mostly helpful for verifying the user has a valid token (and is thus logged in). You must pass a valid token with this request, or it will be rejected.

**Request Parameters**

No request parameters necessary for this route.

**Return Parameters**

- data (object)
  - \_id (ObjectId): the database identifier of the user
  - username (string): the username of the user
  - email (string): the email of the user
- message (string): the success message
- success (boolean): notification if request was successful

**Sample Call**

```
fetch('https://recordxapi.render.com/api/users/:userId', {
  method: "POST",
  headers: {
    'Content-Type': 'application/json'
    'x-access-token': 'TOKEN_STRING_HERE'
  })
})
```

**Sample Response**

```
{
  "data": {
    "_id": 23098sdf09s0823028,
    "email": "robbie3@me.com",
    "favorites": [/*an array of objects if the user has any favorites*/],
    "messages": [/*an array of objects if the user has any messages*/]
    "username": "Robbie"
  }
  "message": "User successfuly logged in",
  "success": True,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
}
```

### **PATCH /api/users/:userId**

This route is used by the user to edit their profile information. You must pass a valid token with this request, or it will be rejected.

**Request Parameters**

Any of the following request parameters can be provided for this route

- username (string): the updated username of the user
- email (string): the updated email of the user
- password (string): the updated password of the user

**Return Parameters**

- data (object)
  - \_id (ObjectId): the database identifier of the user
  - username (string): the username of the user
  - email (string): the email of the user
- message (string): the success message
- success (boolean): notification if request was successful

**Sample Call**

```
fetch('https://recordxapi.render.com/api/users/:userId', {
  method: "PATCH",
  headers: {
    'Content-Type': 'application/json'
    'x-access-token': 'TOKEN_STRING_HERE'
  },
  body: JSON.stringify({/* whatever things you want to update */})
})
```

**Sample Response**

```
{
  "data": {
    "_id": 23098sdf09s0823028,
    "email": "robbie3@me.com",
    "favorites": [/*an array of objects if the user has any favorites*/],
    "messages": [/*an array of objects if the user has any messages*/]
    "username": "Robbie"
  }
  "message": "User successfuly updated",
  "success": True,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
}
```

### **DELETE /api/users/:userId** \*Admin required

This route is used by admin to delete a specific user. You must pass a valid token with this request, or it will be rejected.

**Request Parameters**

No request parameters required.

**Return Parameters**

- message (string): the success message
- success (boolean): notification if request was successful

**Sample Call**

```
fetch('https://recordxapi.render.com/api/users/:userId', {
  method: "DELETE",
  headers: {
    'Content-Type': 'application/json'
    'x-access-token': 'TOKEN_STRING_HERE'
  },
  body: JSON.stringify({/* whatever things you want to update */})
})
```

**Sample Response**

```
{
  "message": "User successfuly deleted",
  "success": True,
}
```

### **POST /api/users/messages**

This route is used for a user to send a message to another user. A valid token must be passed with this request or it will be rejected.

**Request Parameters**

- to_user (string, required): the name of the user to send message to
- message (string, required): the message to send to the user

**Return Parameters**

- data (object)
- message (string): the success message
- success (boolean): notification if request was successful

**Sample Call**

```
fetch('https://recordxapi.render.com/api/users/messages', {
  method: "POST",
  headers: {
    'Content-Type': 'application/json',
    'x-access-token': 'TOKEN_STRING_HERE'
  },
  body: JSON.stringify({
    to_user: 'Charlie',
    message: 'This is a really awesome album'
  })
})
```

**Sample Response**

If the API sends the message to the intended user, the following object
will be returned:

```
{
  "message": "Message successfully sent to Charlie",
  "success": True,
}
```

### **POST /api/users/favorites**

This route is used for a user to add a record to their favorites list. A valid token must be passed with this request or it will be rejected.

**Request Parameters**

- title (string, required): the title of the album to favorite

**Return Parameters**

- message (string): the success message
- success (boolean): notification if request was successful

**Sample Call**

```
fetch('https://recordxapi.render.com/api/users/favorites', {
  method: "POST",
  headers: {
    'Content-Type': 'application/json',
    'x-access-token': 'TOKEN_STRING_HERE'
  },
  body: JSON.stringify({
    title: 'Duty Now For The Future',
  })
})
```

**Sample Response**

If the API adds the album to the users favorites list, the following object will be returned:

```
{
  "message": "Album successfully added to favorites",
  "success": True,
}
```

## Record Endpoints

### **GET /api/records**

Returns a list of all records in the database

**Request Parameters**

There are no request parameters

**Return Parameters**

(array of objects):

- \_id (ObjectId): This is the database identifier for the record
- artist (string): This is the name of the band
- album (string): This is the title of the record
- genre (string): This is the genre of the music
- cost (number): This is the cost of the record in dollars
- quantity (number): This is the number of records available for sale
- image_url (string): This is the url for a jpeg image of the album cover

**Sample Call**

```
fetch('https://recordxapi.render.com/api/records', {
  headers: {
    'Content-Type': 'application/json',
  },
})
```

**Sample Response**

```
{
  "data": [
    {
      "_id": "63f56015aa62ef6e9c5f722f",
      "album": "Freedom Of Choice",
      "artist": "Devo",
      "cost": 12.99,
      "format": "LP",
      "genre": [
        "new_wave",
        "electronic"
      ],
      "image_url": "https://upload.wikimedia.org/wikipedia/en/7/70/DevoFreedomofChoice.jpg",
      "quantity": 200
    },
    {
      "_id": "63f56015aa62ef6e9c5f7231",
      "album": "Loaded",
      "artist": "The Velvet Underground",
      "cost": 12.99,
      "format": "LP",
      "genre": [
        "psychedelic",
        "pop"
      ],
      "image_url": "https://upload.wikimedia.org/wikipedia/en/7/71/Loadedalbum.jpg",
      "quantity": 78
    },
  ],
  "success": true
}
```

### **PATCH /api/users/records/:recordId** \*Admin required

This route is used for an admin to update a record entry. A valid token must be passed with this request or it will be rejected.

**Request Parameters**

- artist (string): This is the name of the band to update
- album (string): This is the title of the record to update
- genre (string): This is the genre of the music to update
- cost (number): This is the cost of the record in dollars to update
- quantity (number): This is the number of records available for sale to update
- image_url (string): This is the url for a jpeg image of the album cover to update

**Return Parameters**

- \_id (ObjectId): This is the database identifier for the record
- artist (string): This is the name of the updated band
- album (string): This is the title of the updated record
- genre (string): This is the updated genre of the music
- cost (number): This is the updated cost of the record in dollars
- quantity (number): This is the updated number of records available for sale
- image_url (string): This is the updated url for a jpeg image of the album cover
- message (string): the success message
- success (boolean): notification if request was successful

**Sample Call**

```
fetch('https://recordxapi.render.com/api/records/:recordId', {
  method: "PATCH",
  headers: {
    'Content-Type': 'application/json',
    'x-access-token': 'TOKEN_STRING_HERE'
  },
  body: JSON.stringify({
    quantity: 5,
  })
})
```

**Sample Response**

```
{
  "data": {
    "_id": "63f56015aa62ef6e9c5f7232",
    "album": "Empire",
    "artist": "Unwound",
    "cost": 12.99,
    "format": "LP",
    "genre": [
      "rock",
      "post_rock"
    ],
    "image_url":
    "https://media.pitchfork.com/photos/5929b0a2b1335d7bf169a158/1:1/w_600/b9d0b258.jpg",
    "quantity": 5
  },
  "message": "Record updated successfully",
  "success": True
```

### **DELETE /api/users/records/:recordId** \*Admin required

This route is used for an admin to delete a record entry. A valid token must be passed with this request or it will be rejected.

**Request Parameters**

No Request parameters needed

**Return Parameters**

- message (string): the success message
- success (boolean): notification if request was successful

**Sample Call**

```
fetch('https://recordxapi.render.com/api/records/:recordId', {
  method: "DELETE",
  headers: {
    'Content-Type': 'application/json',
    'x-access-token': 'TOKEN_STRING_HERE'
  },
})
```

**Sample Response**

```
{
  "message": "Record deleted successfully",
  "success": True
```
