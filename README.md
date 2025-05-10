# Gut Microbiome Health API

Welcome to the Gut Microbiome Health API!  
This API is designed for easy, read-only access to gut microbiome health articles and data.  
All endpoints are **GET-only** and return JSON.  
This project is hosted on [api.caravanwellness.com](https://api.caravanwellness.com), so there is no authentication or POST/PUT/PATCH/DELETE support.

---

## Quick Start

All endpoints are public and require no authentication.

```http
GET https://api.caravanwellness.com/accounts/39061852/articles.json
```

---

## API Reference

### List Articles

Retrieve a list of all articles.

**Request**

```http
GET /accounts/39061852/articles.json
```

**Response**

```json
[
  {
    "id": "ff172e62a230360472111cced8db4a9b",
    "title": "What is Gut Microbiome Health?",
    "summary": "A brief overview of gut microbiome health.",
    "published_at": "2024-05-01T12:00:00Z"
  },
  ...
]
```

---

### Retrieve an Article

Get the full details for a single article.

**Request**

```http
GET /accounts/39061852/articles/ff172e62a230360472111cced8db4a9b.json
```

**Response**

```json
{
  "id": "ff172e62a230360472111cced8db4a9b",
  "title": "What is Gut Microbiome Health?",
  "body": "Gut microbiome health refers to...",
  "author": "Jane Doe",
  "published_at": "2024-05-01T12:00:00Z"
}
```

---

## Example Usage

**List all articles:**

```bash
curl https://api.caravanwellness.com/accounts/39061852/articles.json
```

**Get a specific article:**

```bash
curl https://api.caravanwellness.com/accounts/39061852/articles/ff172e62a230360472111cced8db4a9b.json
```

---

## Status Codes

- `200 OK` – Successful GET request
- `404 Not Found` – Resource does not exist

---

## Support

If you have questions or need help, please open an issue on this repository.

---

© 2025 Gut Microbiome Health API
