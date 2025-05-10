# Caravan Articles API

Welcome to the Caravan Articles API!  

This API is designed for easy, read-only access to articles hosted by caravanwellness.com.  

All endpoints are GET-only and return JSON. This API is available on [api.caravanwellness.com](https://api.caravanwellness.com).

---

## Quick Start

All endpoints are public and require no authentication.

```http
GET https://api.caravanwellness.com/accounts/{account_id}/articles.json
```

---

## API Reference

### List Articles

Retrieve a list of all articles.

**Request**

```http
GET /accounts/{account_id}/articles.json
```

**Response**

```json
{
  "data": [
    {
      "id": "ff172e62a230360472111cced8db4a9b",
      "name": "What is Gut Microbiome Health",
      "language": "en",
      "thumbnail": "assets/what-is-gut-microbiome-health.jpg"
    }
  ],
  "status": 200
}
```

---

### Retrieve an Article

Get the full details for a single article.

**Request**

```http
GET /accounts/{account_id}/articles/{article_id}.json
```

**Response**

```json
{
  "data": [
    {
      "id": "ff172e62a230360472111cced8db4a9b",
      "name": "What is Gut Microbiome Health",
      "description": "This is a test description",
      "language": "en",
      "thumbnail": "assets/what-is-gut-microbiome-health.jpg",
      "html": "Example article text..."
      "content": "Example article text..."
    }
  ],
  "status": 200
}
```

---

## Example Usage

**List all articles:**

```bash
curl -k https://api.caravanwellness.com/accounts/39061852/articles.json
```

**Get a specific article:**

```bash
curl -k https://api.caravanwellness.com/accounts/39061852/articles/ff172e62a230360472111cced8db4a9b.json
```

---

## Status Codes

- `200 OK` – Successful GET request
- `404 Not Found` – Resource does not exist

---

## Support

If you have questions or need help, please contact info@caravanwellness.com

---
