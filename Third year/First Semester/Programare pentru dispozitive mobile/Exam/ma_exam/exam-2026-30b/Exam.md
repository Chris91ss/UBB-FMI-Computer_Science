# Exam Requirement: Restaurant Order App
A group of users is managing their restaurant order budget using a mobile application. Users can track dine-in, takeout, and delivery expenses.

On the server side, at least the following details are maintained:
- `id`: The unique identifier for the transaction. Integer value greater than zero.
- `date`: The date when the transaction occurred. A string in the format "YYYY-MM-DD".
- `amount`: The total cost of the order. A decimal value.
- `type`: The type of transaction (e.g., dine-in, takeout, delivery). A string of characters.
- `category`: The category of the food (e.g., pizza, sushi, burger). A string of characters.
- `description`: A description of the order. A string of characters.

The application should provide at least the following features:

## Main Section (Separate Screen/Activity)
> **Note:** Each feature in this section should be implemented in a separate screen unless otherwise specified.

- A. **(1p) View the list of orders**: Using the `GET /orders` call, users can retrieve all their order records. If offline, the app will display an offline message and provide a retry option. Once retrieved, the data should be available on the device, regardless of whether online or offline.
- B. **(2p) View Order Details**: By selecting an order from the list, the user can view its details. The `GET /order/:id` call will retrieve specific details. Once retrieved, the data should be available on the device, regardless of whether online or offline.
- C. **(1p) Add a new order**: Users can create a new order transaction using the `POST /order` call by specifying all details. This feature is available online only.
- D. **(1p) Delete an order**: Users can delete an order record using the `DELETE /order/:id` call by selecting it from the list. This feature is available online only.

## Reports Section (Separate Screen/Activity)
> **Note:** This section uses different API endpoints than the Main section.

**(1p) Monthly Dining Analysis**: Using the `GET /allOrders` call, the app will retrieve all records and compute the list of monthly totals, displayed in descending order.

## Insights Section (Separate Screen/Activity)
> **Note:** This section uses different API endpoints than the Main section.

**(1p) Top Food Categories**: View the top 3 food categories by spending. Using the same `GET /allOrders` call, the app will compute and display the top 3 categories and their total amounts in descending order.

## Additional Features
- **(1p) WebSocket Notifications**: When a new order is added, the server will use a WebSocket channel to send the details to all connected clients. The app will display the received data in human-readable form (e.g., as a toast, snackbar, or dialog).
- **(0.5p) Progress Indicator**: A progress indicator will be displayed during server operations.
- **(0.5p) Error Handling & Logging**: Any server interaction errors will be displayed using a toast or snackbar, and all interactions (server or DB) will log a message.

## Server Info
- Location: `./server`
- Install: `npm install`
- Run: `npm start`
- Port: 2625
