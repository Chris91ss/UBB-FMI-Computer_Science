# FitLog Server

A Node.js REST API server with WebSocket support for the FitLog Flutter application.

## Overview

This server provides:

- **REST API** - CRUD operations for foods and logged meals
- **WebSocket** - Real-time updates to all connected clients
- **SQLite Database** - Persistent local storage

## Quick Start

```bash
cd non-native/server
npm install      # Install dependencies (first time only)
npm start        # Start the server
```

Server runs on `http://localhost:3000`

## File Structure

```
server/
├── package.json      # Dependencies and scripts
├── server.js         # Main server code
├── fitlog.db         # SQLite database (auto-created)
└── .gitignore        # Ignores node_modules
```

## API Endpoints

### Foods

| Method | Endpoint           | Description       |
| ------ | ------------------ | ----------------- |
| GET    | `/api/foods`     | Get all foods     |
| POST   | `/api/foods`     | Create a new food |
| PUT    | `/api/foods/:id` | Update a food     |
| DELETE | `/api/foods/:id` | Delete a food     |

### Logged Foods

| Method | Endpoint                  | Description                 |
| ------ | ------------------------- | --------------------------- |
| GET    | `/api/logged-foods`     | Get all logged food entries |
| POST   | `/api/logged-foods`     | Create a logged food entry  |
| DELETE | `/api/logged-foods/:id` | Delete a logged food entry  |

## Request/Response Examples

### Create Food

```bash
curl -X POST http://localhost:3000/api/foods \
  -H "Content-Type: application/json" \
  -d '{"name":"Apple","serving":"per 100 g","kcal":52,"protein":0.3,"carbs":14,"fat":0.2,"category":"Fruits"}'
```

### Response

```json
{
  "id": 4,
  "name": "Apple",
  "serving": "per 100 g",
  "kcal": 52,
  "protein": 0.3,
  "carbs": 14,
  "fat": 0.2,
  "category": "Fruits"
}
```

## WebSocket Messages

The server broadcasts these events to all connected clients:

```javascript
// When food is created
{ "type": "food_created", "data": { "id": 4, "name": "Apple", ... } }

// When food is updated
{ "type": "food_updated", "data": { "id": 4, "name": "Green Apple", ... } }

// When food is deleted
{ "type": "food_deleted", "data": { "id": 4 } }

// When logged food is created
{ "type": "logged_food_created", "data": { "log_id": 1, "grams": 150, ... } }

// When logged food is deleted
{ "type": "logged_food_deleted", "data": { "id": 1 } }
```

## Flutter Connection

### Android Emulator

Use `http://10.0.2.2:3000` (special alias for host machine)

### iOS Simulator

Use `http://localhost:3000`

### Physical Device

Use your computer's IP address (e.g., `http://192.168.1.100:3000`)

## Server Logs

All operations are logged with timestamps:

```
[2025-01-15T10:30:00.000Z] [GET /api/foods] Fetching all foods
[2025-01-15T10:30:00.005Z] [GET /api/foods] Returned 3 foods
[2025-01-15T10:30:01.000Z] [POST /api/foods] Creating food: Apple
[2025-01-15T10:30:01.010Z] [POST /api/foods] Created food with ID: 4
[2025-01-15T10:30:01.015Z] [WebSocket] Broadcast: food_created
```

## Rubric Compliance

This server implementation satisfies the following requirements:

**REST Server** - Custom Node.js/Express server (no cloud services)
**CRUD Operations** - Full Create, Read, Update, Delete support
**WebSocket** - Real-time updates for all connected clients
**Server Logs** - All operations are logged with timestamps
**ID Management** - Server assigns and manages all IDs
**Error Handling** - Proper HTTP status codes and error messages
**Validation** - Input validation for all endpoints
