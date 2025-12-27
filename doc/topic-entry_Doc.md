# LgX
LgX is a Learning Log app. It's a free, ready-to-use backend API designed for frontend developers. This project exposes real-world APIs so frontend learners can build, test, and showcase applications without needing to implement a backend.

Below here is a little documentation of how the topic and entry works, for more, check [main_doc.md](https://github.com/occupythemind/lgX/doc/main_doc.md/)

# 📘 Topics & Entries (Core Data Model)

LgX is built around **Topics** and **Entries**.

Think of it like this:

* A **Topic** is a container (e.g. *“JavaScript”*, *“Daily Notes”*)
* An **Entry** is a note inside a Topic

> One Topic can have many Entries (1 → many)



## 🧠 Important Concepts (Read This Once)

### IDs (Primary Keys)

Every Topic and Entry has an `id` (also called `pk`).

Example:

```json
"id": "f47ac10b-58cc-4372-a567-0e02b2c3d479"
```

You’ll use this `id` when:

* retrieving data
* updating data
* deleting data



### Status Field

Both Topics and Entries support a `status` field:

| Value  | Meaning              |
|  | -- |
| ACTIVE | Visible / in use     |
| DRAFT  | Saved but not active |
| TRASH  | Soft-deleted         |



# 📂 TOPICS

Topics represent **categories or containers** for entries.



## 🔹 List All Topics

```http
GET /api/topics/
```

Returns all topics created by the authenticated user.

### Example Response

```json
[
  {
    "id": "uuid",
    "title": "JavaScript",
    "status": "ACTIVE",
    "created": "2025-01-01T10:00:00Z"
  }
]
```



## 🔹 Retrieve a Single Topic

```http
GET /api/topics/<topic_id>/
```

### Required

* `topic_id` → the topic’s `id`



## 🔹 Create a Topic

```http
POST /api/topics/
```

### Required Fields

```json
{
  "title": "My New Topic"
}
```

### Optional Fields

```json
{
  "status": "DRAFT"
}
```

> If `status` is not provided, it defaults to `ACTIVE`.



## 🔹 Update / Partial Update a Topic

```http
PUT /api/topics/<topic_id>/
PATCH /api/topics/<topic_id>/
```

### Example (PATCH)

```json
{
  "title": "Updated Topic Title"
}
```



## 🔹 Delete a Topic

```http
DELETE /api/topics/<topic_id>/
```

This performs a soft delete if that topic status is not set to TRASH. If it was set to trash, then a permanent delete would take place.



# 📝 ENTRIES

Entries are **notes that belong to a Topic**.

There are **two URL styles** available.



## 🧭 Entry URL Patterns (Very Important)

### 1️⃣ Global Entry URLs

```text
/api/entries/
```

Use this when:

* You want **all entries**
* You don’t care which topic they belong to



### 2️⃣ Nested Entry URLs (Recommended)

```text
/api/topics/<topic_id>/entries/
```

Use this when:

* You’re working inside a specific topic
* Creating new entries (required)



## 🔹 List Entries

### All Entries (All Topics)

```http
GET /api/entries/
```

### Entries for a Specific Topic

```http
GET /api/topics/<topic_id>/entries/
```



## 🔹 Retrieve a Single Entry

Both URLs work:

```http
GET /api/entries/<entry_id>/
```

```http
GET /api/topics/<topic_id>/entries/<entry_id>/
```

> For simplicity, frontend apps usually prefer the **first one**.



## 🔹 Create an Entry (Important)

⚠️ **You must use the nested URL**

```http
POST /api/topics/<topic_id>/entries/
```

### Required Fields

```json
{
  "text": "This is my note",
  "status": "ACTIVE"
}
```

If you try:

```http
POST /api/entries/
```

❌ You will get an error (by design).



## 🔹 Update / Partial Update an Entry

```http
PUT /api/entries/<entry_id>/
PATCH /api/entries/<entry_id>/
```

Example:

```json
{
  "text": "Updated note content"
}
```



## 🔹 Delete an Entry

```http
DELETE /api/entries/<entry_id>/
```



# 🧩 Summary for Frontend Developers

### You will mostly use:

* `GET /api/topics/`
* `POST /api/topics/`
* `GET /api/topics/<id>/entries/`
* `POST /api/topics/<id>/entries/`
* `PATCH /api/entries/<id>/`
* `DELETE /api/entries/<id>/`

### Mental Model

> **Topics = folders**
> **Entries = files inside folders**