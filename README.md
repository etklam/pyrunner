# Simple Python API

## Installation

```bash
pip install -r requirements.txt
```

## Running the API

```bash
python app.py
```

The API will be available at http://localhost:5000

## Endpoints

- `GET /` - Welcome message
- `GET /items` - Get all items
- `GET /items/<id>` - Get a specific item
- `POST /items` - Create a new item (JSON body with `name`)
