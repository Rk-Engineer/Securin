
```markdown
# 🥘 Recipe Upload API with FastAPI & SQLite

This is a simple backend API built using **FastAPI** that allows you to:

1. Upload a `.json` file containing recipe data
2. Store the data in a **SQLite** database
3. Retrieve all recipes or filter them based on cuisine, country, or continent

---

## 📁 Project Structure

```
📦 recipe-api/
├── main.py               # FastAPI app with 3 endpoints
├── recipes.db            # SQLite database (auto-created)
└── README.md             # Project documentation
```

---

## 🚀 Getting Started

### 🔧 Requirements

- Python 3.7+
- FastAPI
- Uvicorn

Install the dependencies:

```bash
pip install fastapi uvicorn python-multipart aiofiles
```

---

### ▶️ Running the App

```bash
uvicorn main:app --reload
```

Visit the interactive API docs at:

📍 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📤 API Endpoints

### 1. `POST /upload`

Upload a `.json` file of recipes in a specific format.

- **Request**: Multipart/form-data with file input
- **Response**: Success message or error

### 2. `GET /recipes`

Returns all stored recipes.

- **Response**: List of recipes with full details

### 3. `GET /recipes/filter`

Filter recipes by any of the following query parameters:
- `cuisine`
- `country_state`
- `continent`

**Example**:
```
GET /recipes/filter?cuisine=Southern Recipes
```

---

## 📦 Sample JSON Format

```json
{
  "0": {
    "Contient": "North America",
    "Country_State": "US",
    "cuisine": "Southern Recipes",
    "title": "Sweet Potato Pie",
    "URL": "https://example.com",
    "rating": 4.8,
    "total_time": 115,
    "prep_time": 15,
    "cook_time": 100,
    "description": "Homemade Southern-style sweet potato pie.",
    "ingredients": ["1 sweet potato", "0.5 cup butter", "..."],
    "instructions": ["Boil potato", "Mix ingredients", "..."],
    "nutrients": {
      "calories": "389 kcal",
      "carbohydrateContent": "48 g",
      "proteinContent": "5 g"
    },
    "serves": "8 servings"
  }
}
```

---

## 🛠 Future Improvements

- Add authentication (JWT)
- Add pagination for GET endpoints
- Export recipes to JSON/CSV
- Frontend integration with Streamlit or React

---

## 📃 License

This project is licensed under the MIT License.

---

## 🙌 Acknowledgements

Built with ❤️ using [FastAPI](https://fastapi.tiangolo.com/) and [SQLite](https://sqlite.org).
```
