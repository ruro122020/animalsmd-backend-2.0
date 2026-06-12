# API Endpoints

Base URL: `http://localhost:8000`

---

## Public Routes (No Auth Required)

### Authentication

### POST `/signup`
Create a new user account and start a session.

**Request Body:**
```json
{
  "name": "Jane Doe",
  "username": "janedoe",
  "email": "janedoe@email.com",
  "password": "testpassword123"
}
```

**Response (201):**
```json
{
  "id": 2,
  "name": "Jane Doe",
  "email": "janedoe@email.com",
  "username": "janedoe",
  "cart_products": []
}
```

---

### POST `/login`
Login with existing credentials and start a session.

**Request Body:**
```json
{
  "username": "jsmith",
  "password": "testpassword123"
}
```

**Response (200):**
```json
{
  "id": 1,
  "name": "John Smith",
  "email": "jsmith@email.com",
  "username": "jsmith",
  "cart_products": []
}
```

---

### DELETE `/logout`
End the current session. No request body needed.

**Response (200):**
```json
{}
```

---

### GET `/check_session`
Check if the user is currently logged in.

**Response (200) — logged in:**
```json
{
  "id": 1,
  "name": "John Smith",
  "email": "jsmith@email.com",
  "username": "jsmith",
  "cart_products": []
}
```

**Response (401) — not logged in:**
```json
{
  "error": "Not logged in"
}
```

---

### Species

### GET `/species`
Get all species.

**Response (200):**
```json
[
  {
    "id": 1,
    "type_name": "dog",
    "species_classification": {}
  },
  {
    "id": 2,
    "type_name": "cat",
    "species_classification": {}
  }
]
```

---

### GET `/species/<type_name>`
Get a species' classification and available symptoms.

**Example:** `/species/dog`

**Response (200):**
```json
{
  "classification": "mammal",
  "symptoms": [
    "skin lesions",
    "loss of appetite",
    "lethargy",
    "sneezing",
    "coughing",
    "runny nose",
    "difficulty breathing",
    "fever",
    "excessive salivation",
    "paralysis",
    "muscle weakness",
    "nasal discharge",
    "eye discharge",
    "seizures"
  ],
  "classification_id": 1
}
```

---

### Products

### GET `/products`
Get all products.

**Response (200):**
```json
[
  {
    "id": 1,
    "name": "enrofloxacin (baytril)",
    "price": 25,
    "description": "Enrofloxacin, known by the brand name Baytril...",
    "prescription": true
  },
  {
    "id": 3,
    "name": "amoxicillin",
    "price": 15,
    "description": "Amoxicillin is a broad-spectrum antibiotic...",
    "prescription": false
  }
]
```

---

### GET `/products/<id>`
Get a single product by ID.

**Example:** `/products/1`

**Response (200):**
```json
{
  "id": 1,
  "name": "enrofloxacin (baytril)",
  "price": 25,
  "description": "Enrofloxacin, known by the brand name Baytril...",
  "prescription": true
}
```

---

## Protected Routes (Auth Required)

### Pets

### GET `/user/pets`
Get all pets belonging to the logged-in user.

**Response (200):**
```json
[
  {
    "id": 1,
    "name": "earl",
    "age": 7,
    "weight": 12,
    "user_id": 1,
    "species_id": 1,
    "symptoms": [
      {
        "id": 2,
        "name": "loss of appetite"
      }
    ]
  }
]
```

---

### POST `/user/pets`
Create a new pet with symptoms for the logged-in user.

**Request Body:**
```json
{
  "name": "rex",
  "age": 5,
  "weight": 30,
  "type": "dog",
  "symptoms": ["coughing", "sneezing"]
}
```

**Response (200):**
```json
{
  "id": 4,
  "name": "rex",
  "age": 5,
  "weight": 30,
  "user_id": 1,
  "species_id": 1,
  "symptoms": [
    {
      "id": 5,
      "name": "coughing"
    },
    {
      "id": 4,
      "name": "sneezing"
    }
  ]
}
```

---

### GET `/user/pets/<id>`
Get a single pet by ID.

**Example:** `/user/pets/4`

**Response (200):**
```json
{
  "id": 4,
  "name": "rex",
  "age": 5,
  "weight": 30,
  "user_id": 1,
  "species_id": 1,
  "symptoms": [
    {
      "id": 5,
      "name": "coughing"
    },
    {
      "id": 4,
      "name": "sneezing"
    }
  ]
}
```

---

### PATCH `/user/pets/<id>`
Update a pet's attributes.

**Example:** `/user/pets/4`

**Request Body:**
```json
{
  "name": "buddy jr",
  "weight": 22
}
```

**Response (200):**
```json
{
  "id": 4,
  "name": "buddy jr",
  "age": 5,
  "weight": 22,
  "user_id": 1,
  "species_id": 1,
  "symptoms": [
    {
      "id": 5,
      "name": "coughing"
    },
    {
      "id": 4,
      "name": "sneezing"
    }
  ]
}
```

---

### DELETE `/user/pets/<id>`
Delete a pet by ID.

**Example:** `/user/pets/4`

**Response (200):**
```json
{}
```

---

### Pet Results

### GET `/user/pets/<id>/results`
Get illness diagnosis results for a pet based on its symptoms and species classification.

**Example:** `/user/pets/4/results` (dog with symptoms: coughing, sneezing)

**Response (200):**
```json
[
  {
    "id": 2,
    "name": "respiratory infection",
    "description": "Respiratory infections are illnesses that affect the respiratory system...",
    "remedy": "To manage respiratory infections, maintain a clean and well-ventilated living area...",
    "symptoms": [
      { "id": 4, "name": "sneezing" },
      { "id": 5, "name": "coughing" },
      { "id": 6, "name": "runny nose" }
    ],
    "medications": [
      { "id": 4, "name": "amoxicillin", "description": "..." },
      { "id": 3, "name": "doxycycline", "description": "..." },
      { "id": 1, "name": "enrofloxacin (baytril)", "description": "..." }
    ],
    "products": [
      { "id": 1, "name": "enrofloxacin (baytril)", "price": 25, "description": "...", "prescription": true },
      { "id": 3, "name": "amoxicillin", "price": 15, "description": "...", "prescription": false }
    ]
  }
]
```

**Response (404) — no matching illnesses:**
```json
{
  "error": "No Results found"
}
```

---

### Cart

### GET `/user/cart`
Get all items in the logged-in user's cart.

**Response (200):**
```json
[
  {
    "id": 2,
    "quantity": 2,
    "product": {
      "id": 1,
      "name": "enrofloxacin (baytril)",
      "price": 25,
      "description": "Enrofloxacin, known by the brand name Baytril...",
      "prescription": true
    }
  }
]
```

---

### POST `/user/cart`
Add a product to the logged-in user's cart.

**Request Body:**
```json
{
  "user_id": 1,
  "product_id": 1,
  "quantity": 2
}
```

**Response (200):**
```json
{
  "id": 2,
  "quantity": 2,
  "product": {
    "id": 1,
    "name": "enrofloxacin (baytril)",
    "price": 25,
    "description": "Enrofloxacin, known by the brand name Baytril...",
    "prescription": true
  }
}
```

---

### PATCH `/user/cart/<id>`
Update a cart item (e.g. change quantity).

**Example:** `/user/cart/2`

**Request Body:**
```json
{
  "quantity": 5
}
```

**Response (200):**
```json
{
  "id": 2,
  "quantity": 5,
  "product": {
    "id": 1,
    "name": "enrofloxacin (baytril)",
    "price": 25,
    "description": "Enrofloxacin, known by the brand name Baytril...",
    "prescription": true
  }
}
```

---

### DELETE `/user/cart/<id>`
Delete a single cart item by ID.

**Example:** `/user/cart/2`

**Response (200):**
```json
{}
```

---

### DELETE `/user/cart`
Delete all items in the logged-in user's cart.

**Response (200):**
```json
{}
```
