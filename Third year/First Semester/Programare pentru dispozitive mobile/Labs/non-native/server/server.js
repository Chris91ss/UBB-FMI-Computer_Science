const express = require('express');
const cors = require('cors');
const http = require('http');
const WebSocket = require('ws');
const sqlite3 = require('sqlite3').verbose();

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

const PORT = 3000;
const DB_PATH = './fitlog.db';

// Middleware
app.use(cors());
app.use(express.json());

// Initialize database
const db = new sqlite3.Database(DB_PATH, (err) => {
  if (err) {
    console.error('Failed to open database:', err);
  } else {
    console.log('Connected to SQLite database');
    initializeTables();
  }
});

function initializeTables() {
  db.serialize(() => {
    db.run(`CREATE TABLE IF NOT EXISTS foods (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      serving TEXT NOT NULL,
      kcal INTEGER NOT NULL,
      protein REAL NOT NULL,
      carbs REAL NOT NULL,
      fat REAL NOT NULL,
      category TEXT
    )`, (err) => {
      if (err) {
        console.error('Error creating foods table:', err);
      } else {
        console.log('Foods table ready');
      }
    });

    db.run(`CREATE TABLE IF NOT EXISTS logged_foods (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      food_id INTEGER NOT NULL,
      grams INTEGER NOT NULL,
      FOREIGN KEY(food_id) REFERENCES foods(id) ON DELETE CASCADE
    )`, (err) => {
      if (err) {
        console.error('Error creating logged_foods table:', err);
      } else {
        console.log('Logged foods table ready');
      }
    });

    // Seed initial data if empty
    db.get('SELECT COUNT(*) as count FROM foods', (err, row) => {
      if (!err && row.count === 0) {
        const seeds = [
          ['Chicken Breast', 'per 100 g', 165, 31, 0, 4, 'Meats'],
          ['Brown Rice', 'per 100 g', 111, 3, 23, 1, 'Grains'],
          ['Broccoli', 'per 100 g', 34, 3, 7, 0, 'Vegetables'],
        ];
        const stmt = db.prepare('INSERT INTO foods (name, serving, kcal, protein, carbs, fat, category) VALUES (?, ?, ?, ?, ?, ?, ?)');
        seeds.forEach(food => {
          stmt.run(food, (err) => {
            if (err) console.error('Error seeding food:', err);
            else console.log(`Seeded: ${food[0]}`);
          });
        });
        stmt.finalize();
      }
    });
  });
}

// Broadcast to all WebSocket clients
function broadcast(data) {
  const message = JSON.stringify(data);
  wss.clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(message);
    }
  });
}

// Helper: log with timestamp
function log(operation, details) {
  const timestamp = new Date().toISOString();
  console.log(`[${timestamp}] [${operation}] ${details}`);
}

// GET /api/foods - Fetch all foods
app.get('/api/foods', (req, res) => {
  log('GET /api/foods', 'Fetching all foods');
  db.all('SELECT * FROM foods ORDER BY id DESC', (err, rows) => {
    if (err) {
      log('GET /api/foods', `Error: ${err.message}`);
      res.status(500).json({ error: 'Failed to fetch foods' });
    } else {
      log('GET /api/foods', `Returned ${rows.length} foods`);
      res.json(rows);
    }
  });
});

// GET /api/logged-foods - Fetch all logged foods with food details
app.get('/api/logged-foods', (req, res) => {
  log('GET /api/logged-foods', 'Fetching all logged foods');
  db.all(`
    SELECT lf.id as log_id, lf.grams, f.*
    FROM logged_foods lf
    INNER JOIN foods f ON f.id = lf.food_id
    ORDER BY lf.id DESC
  `, (err, rows) => {
    if (err) {
      log('GET /api/logged-foods', `Error: ${err.message}`);
      res.status(500).json({ error: 'Failed to fetch logged foods' });
    } else {
      log('GET /api/logged-foods', `Returned ${rows.length} logged foods`);
      res.json(rows);
    }
  });
});

// POST /api/foods - Create a new food
app.post('/api/foods', (req, res) => {
  const { name, serving, kcal, protein, carbs, fat, category } = req.body;
  log('POST /api/foods', `Creating food: ${name}`);
  
  if (!name || serving === undefined || kcal === undefined || 
      protein === undefined || carbs === undefined || fat === undefined) {
    log('POST /api/foods', 'Validation failed: missing required fields');
    return res.status(400).json({ error: 'Missing required fields' });
  }

  db.run(
    'INSERT INTO foods (name, serving, kcal, protein, carbs, fat, category) VALUES (?, ?, ?, ?, ?, ?, ?)',
    [name, serving, kcal, protein, carbs, fat, category || null],
    function(err) {
      if (err) {
        log('POST /api/foods', `Error: ${err.message}`);
        res.status(500).json({ error: 'Failed to create food' });
      } else {
        log('POST /api/foods', `Created food with ID: ${this.lastID}`);
        db.get('SELECT * FROM foods WHERE id = ?', [this.lastID], (err, row) => {
          if (!err) {
            broadcast({ type: 'food_created', data: row });
            res.status(201).json(row);
          } else {
            res.status(500).json({ error: 'Failed to fetch created food' });
          }
        });
      }
    }
  );
});

// PUT /api/foods/:id - Update a food
app.put('/api/foods/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const { name, serving, kcal, protein, carbs, fat, category } = req.body;
  log('PUT /api/foods/:id', `Updating food ID: ${id}`);
  
  if (!name || serving === undefined || kcal === undefined || 
      protein === undefined || carbs === undefined || fat === undefined) {
    log('PUT /api/foods/:id', 'Validation failed: missing required fields');
    return res.status(400).json({ error: 'Missing required fields' });
  }

  db.run(
    'UPDATE foods SET name = ?, serving = ?, kcal = ?, protein = ?, carbs = ?, fat = ?, category = ? WHERE id = ?',
    [name, serving, kcal, protein, carbs, fat, category || null, id],
    function(err) {
      if (err) {
        log('PUT /api/foods/:id', `Error: ${err.message}`);
        res.status(500).json({ error: 'Failed to update food' });
      } else if (this.changes === 0) {
        log('PUT /api/foods/:id', `Food not found: ${id}`);
        res.status(404).json({ error: 'Food not found' });
      } else {
        log('PUT /api/foods/:id', `Updated food ID: ${id}`);
        db.get('SELECT * FROM foods WHERE id = ?', [id], (err, row) => {
          if (!err) {
            broadcast({ type: 'food_updated', data: row });
            res.json(row);
          } else {
            res.status(500).json({ error: 'Failed to fetch updated food' });
          }
        });
      }
    }
  );
});

// DELETE /api/foods/:id - Delete a food
app.delete('/api/foods/:id', (req, res) => {
  const id = parseInt(req.params.id);
  log('DELETE /api/foods/:id', `Deleting food ID: ${id}`);
  
  db.run('DELETE FROM foods WHERE id = ?', [id], function(err) {
    if (err) {
      log('DELETE /api/foods/:id', `Error: ${err.message}`);
      res.status(500).json({ error: 'Failed to delete food' });
    } else if (this.changes === 0) {
      log('DELETE /api/foods/:id', `Food not found: ${id}`);
      res.status(404).json({ error: 'Food not found' });
    } else {
      log('DELETE /api/foods/:id', `Deleted food ID: ${id}`);
      broadcast({ type: 'food_deleted', data: { id } });
      res.status(204).send();
    }
  });
});

// POST /api/logged-foods - Create a logged food entry
app.post('/api/logged-foods', (req, res) => {
  const { food_id, grams } = req.body;
  log('POST /api/logged-foods', `Creating logged food: food_id=${food_id}, grams=${grams}`);
  
  if (!food_id || grams === undefined) {
    log('POST /api/logged-foods', 'Validation failed: missing food_id or grams');
    return res.status(400).json({ error: 'Missing food_id or grams' });
  }

  db.run(
    'INSERT INTO logged_foods (food_id, grams) VALUES (?, ?)',
    [food_id, grams],
    function(err) {
      if (err) {
        log('POST /api/logged-foods', `Error: ${err.message}`);
        res.status(500).json({ error: 'Failed to create logged food' });
      } else {
        log('POST /api/logged-foods', `Created logged food with ID: ${this.lastID}`);
        db.get(`
          SELECT lf.id as log_id, lf.grams, f.*
          FROM logged_foods lf
          INNER JOIN foods f ON f.id = lf.food_id
          WHERE lf.id = ?
        `, [this.lastID], (err, row) => {
          if (!err) {
            broadcast({ type: 'logged_food_created', data: row });
            res.status(201).json(row);
          } else {
            res.status(500).json({ error: 'Failed to fetch created logged food' });
          }
        });
      }
    }
  );
});

// DELETE /api/logged-foods/:id - Delete a logged food entry
app.delete('/api/logged-foods/:id', (req, res) => {
  const id = parseInt(req.params.id);
  log('DELETE /api/logged-foods/:id', `Deleting logged food ID: ${id}`);
  
  db.run('DELETE FROM logged_foods WHERE id = ?', [id], function(err) {
    if (err) {
      log('DELETE /api/logged-foods/:id', `Error: ${err.message}`);
      res.status(500).json({ error: 'Failed to delete logged food' });
    } else if (this.changes === 0) {
      log('DELETE /api/logged-foods/:id', `Logged food not found: ${id}`);
      res.status(404).json({ error: 'Logged food not found' });
    } else {
      log('DELETE /api/logged-foods/:id', `Deleted logged food ID: ${id}`);
      broadcast({ type: 'logged_food_deleted', data: { id } });
      res.status(204).send();
    }
  });
});

// WebSocket connection handler
wss.on('connection', (ws) => {
  log('WebSocket', 'Client connected');
  
  ws.on('close', () => {
    log('WebSocket', 'Client disconnected');
  });
  
  ws.on('error', (error) => {
    log('WebSocket', `Error: ${error.message}`);
  });
});

// Start server
server.listen(PORT, () => {
  log('Server', `REST API listening on http://localhost:${PORT}`);
  log('Server', `WebSocket server ready on ws://localhost:${PORT}`);
});

// Graceful shutdown
process.on('SIGINT', () => {
  log('Server', 'Shutting down...');
  db.close((err) => {
    if (err) {
      console.error('Error closing database:', err);
    } else {
      console.log('Database closed');
    }
    process.exit(0);
  });
});

