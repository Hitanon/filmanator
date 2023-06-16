# **Backend Filmanator Documentation**

## How to run:

### Manual

1. Create virtual enviroment
   `python3 -m venv backend/venv`
2. Activate virtual enviroment
   - Linux:
     `source backend/venv/bin/activate`
   - Windows(PowerShell):
     `.\backend\venv\Scripts\activate.ps1`
3. Install dependencies
   `pip install -r requirements/requerements.txt`
4. Fill .env file
5. Change to root backend app directory
   `cd ./backend/app`
6. Make migrations(Optional)
   `python manage.py makemigrations`
7. Apply migrations (Optional)
   `python manage.py migrate`
8. Run kinopoisk parser (Optional)
   `python manage.py runparser`
9. Run chatgpt parser (Optional)
   `python manage.py runchatgpt`
10. Run backend server
    `python manage.py runserver`

### With docker

...

## API Documentation

### Users

#### Url: api/v1/token/

* Description: Get jwt tokens: access, refresh. Authorize user
* Methods: Post
* Request body:
  ```
  {
    'email': email,
    'password': password,
  }
  ```
* Response:
  ```
  {
    'access': access,
    'refresh': fefresh,
  }
  ```

#### Url: api/v1/token/refresh/

* Description: Refresh access by refresh token
* Method: Post
* Request body:
  ```
  {
    'refresh': refresh,
  }
  ```
* Response:
  ```
  {
    'access': access,
  }
  ```

#### Url: api/v1/token/verify/

* Description: Verify token
* Method: Post
* Request body:
  ```
  {
    'token': token,
  }
  ```

#### Url: api/v1/users/

* Description: Create, delete users
* Method: Post, Delete

###### Post

* Request body:
  ```
  {
    'email': email,
    'username': username,
    'password': password,
  }
  ```

###### Delete

* Headers:
* Authorization: Bearer `token`

---

### Questionnaire

#### Url: api/v1/questionnaire/

Description: Start, Update session
Methods: Get, Post

###### Get

* Start session
  * Response:
    ```
    {
      'id': session_id,
      'question': {
        'body': body,
        'answers': [
          {
            'id': id,
            'body': body
          }
        ]
      }
    }
    ```

* Get session state
  * Request body:
    ```
    {
      'session': session_id
    }
    ```
  * Response:
    ```
    {
      'question': {
        'body': body,
        'answers':[
          {
            'id': id,
            'body': body
          }
        ]
      }
    }
    ```

###### Post

* Request body:
  ```
  {
    'session': session_id,
    'answer': answer_id,
  }
  ```
  Questionnaire is over:
  * Response:
    ```
    [
      {
        'match_percentage': match_percentage,
        'length': length,
        'titles': [
          {...}
        ]
      }
    ]
    ```
  Questionnaire is not over:
  * Response:
    ```
    {
      'question': {
        'body': body,
        'answers':[
          {
            'id': id,
            'body': body
          }
        ]
      }
    }
    ```

#### Url: api/v1/questionnaire/`session_id`/

* Description: Delete session
* Methods: Delete
