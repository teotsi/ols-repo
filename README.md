# Mono-repo for OLS Project

## Contents

- [How to run](#how-to-run)
  - [Backend](#backend)
  - [Frontend](#frontend)
- [Insert data](#insert-data)
- [Backend Endpoints](#backend-endpoints)

## How to run

### Backend

Since this is a Python project, you will need to create a [virtual environment](https://docs.python.org/3/library/venv.html).

You can store it wherever, in this case we'll move in the project directory and keep it there.

Linux example:

```
cd backend/ols_repo
python3 -m venv venv
```

Then we need to activate it:

```
source ./venv/bin/activate
```

Next, we need to install dependencies/requirements. We can use the included `requirements.txt` file for this.

```
pip install -r requirements.txt
```

Next up, we need to configure our database. This project uses `postgres` as its DBMS, so go ahead and install it on your system, while also creating a database for the project.

After you've done that, you can rename rename the included `.env.default` file to `.env`, and configure it with the DB credentials required.

```
cp .env.default .env
```

The default settings are as following. Make sure to set the values that apply to your DB instance.

```
NAME=api
DB_USER=apiuser
PASSWORD=123456
HOST=localhost
PORT=5432
```

Once you've done that, you can run the following command:

```
python3 manage.py migrate
```

This will create the necessary schemas and tables on the DB by using the migration files present in the project.

Now you can run the project with

```
python3 manage.py runserver
```

And you're all set!

### Frontend

TODO

## Insert data

You can insert data from https://www.ebi.ac.uk/ols/api/ontologies/efo/terms using the `addterms` management command.

You can specify an upper limit of terms to add. Keep in mind that if you choose to do so, certain relationships won't be generated, as some parent nodes might not have been fetched at first.

Examples:

```
### This will load the first 500 terms
python3 manage.py addterms 500
```

To load all terms:

```
# This will load ALL terms - slow!
python3 manage.py addterms
```

## Backend endpoints

The following endpoints and methods are available:

`GET /terms`: This endpoint can be used to fetch all terms. You can pass the page parameter to get all terms as needed.

Example:

```
GET /terms?page=1

  Response: {
    "terms": [
        {
            "label": "Bacteroides infectious disease",
            "description": "Infections with bacteria of the genus BACTEROIDES.Infections with bacteria of the genus bacteroides.",
            "id": "EFO_1000832",
            "synonyms": [
                "Bacteroides Infections",
                "Bacteroides disease or disorder",
                "Bacteroides caused disease or disorder",
                "Bacteroides infectious disease",
                "infection due to Bacteroides"
            ],
            "parents": [
                "EFO_1000872",
                "MONDO_0024389"
            ]
        },
      ...
    ]
  }

```

`POST /terms/` : You can use this endpoint to RESTfully create a new term. You can optionally pass synonyms and parent term IDs on your request.

If the parent ID does not currently exist, a new term will be created with placeholder label and description, so that it can be updated later on.

```
POST /terms/
Body:
  {
    "id": "FAKE-0001",
    "label": "Test term",
    "description": "Test description",
    "synonyms": [
        "trial",
        "dummy"
    ],
    "parents": [
        "FAKE-0002"
    ]
  }

Response:
{
  "new_term": {
      "label": "Test term",
      "description": "Test description",
      "id": "FAKE-0001",
      "synonyms": [
          "trial",
          "dummy"
      ],
      "parents": [
          "FAKE-0002"
      ]
  }
}
```

`GET /terms/<id>`: You can use this endpoint to RESTfully fetch a specific term by its ID.

```
GET /terms/FAKE-0001

Response:
{
  "term": {
      "label": "Test term",
      "description": "Test description",
      "id": "FAKE-0001",
      "synonyms": [
          "trial",
          "dummy"
      ],
      "parents": [
          "FAKE-0002"
      ]
  }
}
```

`PUT /terms/<id>`: You can use this endpoint to RESTfully update an existing term. Note that any new synonyms and parents will be added to the existing ones, they won't overwrite them.

```
PUT /terms/FAKE-0001
Body:
{
  "label": "New test label",
  "description": "Test description",
  "synonyms": [
      "fake"
  ],
  "parents": [
      "FAKE-0002"
  ]
}

Response:
{
  "updated_term": {
      "label": "New test label",
      "description": "Test description",
      "id": "FAKE-0001",
      "synonyms": [
          "trial",
          "dummy",
          "fake"
      ],
      "parents": [
          "FAKE-0002"
      ]
  }
}
```

`DELETE /terms/<id>`: You can use this endpoint to RESTfully delete an existing term.

```
DELETE /terms/FAKE-0001
Response:
{
  "deleted": true
}
```
