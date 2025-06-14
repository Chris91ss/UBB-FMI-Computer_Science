<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<!DOCTYPE html>
<html>
<head>
    <title>Forum - Login</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 400px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        h1 {
            text-align: center;
            color: #333;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #666;
        }
        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 10px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        .error {
            color: red;
            margin-bottom: 15px;
        }
        .toggle-form {
            text-align: center;
            margin-top: 15px;
        }
        .toggle-form a {
            color: #4CAF50;
            text-decoration: none;
        }
        .toggle-form a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Forum Login</h1>
        
        <c:if test="${not empty error}">
            <div class="error">${error}</div>
        </c:if>

        <form id="loginForm" action="login" method="post">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit">Login</button>
        </form>

        <div class="toggle-form">
            <a href="#" onclick="toggleForms()">Don't have an account? Register here</a>
        </div>
    </div>

    <script>
        function toggleForms() {
            const form = document.getElementById('loginForm');
            const button = form.querySelector('button');
            const toggleLink = document.querySelector('.toggle-form a');
            
            if (form.action.includes('action=register')) {
                form.action = 'login';
                button.textContent = 'Login';
                toggleLink.textContent = "Don't have an account? Register here";
            } else {
                form.action = 'login?action=register';
                button.textContent = 'Register';
                toggleLink.textContent = 'Already have an account? Login here';
            }
        }
    </script>
</body>
</html> 