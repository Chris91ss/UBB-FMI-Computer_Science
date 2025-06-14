<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>
<!DOCTYPE html>
<html>
<head>
    <title>Forum - Topics</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        h1 {
            margin: 0;
            color: #333;
        }
        .new-topic {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            text-decoration: none;
        }
        .new-topic:hover {
            background-color: #45a049;
        }
        .topic-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        .topic-item {
            padding: 15px;
            border-bottom: 1px solid #eee;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .topic-item:last-child {
            border-bottom: none;
        }
        .topic-title {
            color: #333;
            text-decoration: none;
            font-weight: bold;
        }
        .topic-title:hover {
            color: #4CAF50;
        }
        .topic-meta {
            color: #666;
            font-size: 0.9em;
        }
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.5);
        }
        .modal-content {
            background-color: white;
            margin: 15% auto;
            padding: 20px;
            border-radius: 5px;
            width: 50%;
            max-width: 500px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #666;
        }
        input[type="text"] {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        .modal-buttons {
            text-align: right;
        }
        .modal-buttons button {
            padding: 8px 15px;
            margin-left: 10px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        .cancel {
            background-color: #f44336;
            color: white;
        }
        .submit {
            background-color: #4CAF50;
            color: white;
        }
        .user-info {
            text-align: right;
            margin-bottom: 20px;
        }
        .logout {
            color: #666;
            text-decoration: none;
        }
        .logout:hover {
            color: #333;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="user-info">
            Welcome, ${sessionScope.user.username} | 
            <a href="${pageContext.request.contextPath}/logout" class="logout">Logout</a>
        </div>

        <div class="header">
            <h1>Forum Topics</h1>
            <button class="new-topic" onclick="showNewTopicModal()">New Topic</button>
        </div>

        <ul class="topic-list">
            <c:forEach items="${topics}" var="topic">
                <li class="topic-item">
                    <div>
                        <a href="topics/${topic.id}" class="topic-title">${topic.title}</a>
                        <div class="topic-meta">
                            Posted by ${topic.username} on 
                            <fmt:formatDate value="${topic.createdAt}" pattern="MMM dd, yyyy HH:mm"/>
                        </div>
                    </div>
                </li>
            </c:forEach>
        </ul>
    </div>

    <!-- New Topic Modal -->
    <div id="newTopicModal" class="modal">
        <div class="modal-content">
            <h2>Create New Topic</h2>
            <form action="topics" method="post">
                <input type="hidden" name="action" value="create">
                <div class="form-group">
                    <label for="title">Title:</label>
                    <input type="text" id="title" name="title" required>
                </div>
                <div class="modal-buttons">
                    <button type="button" class="cancel" onclick="hideNewTopicModal()">Cancel</button>
                    <button type="submit" class="submit">Create</button>
                </div>
            </form>
        </div>
    </div>

    <script>
        function showNewTopicModal() {
            document.getElementById('newTopicModal').style.display = 'block';
        }

        function hideNewTopicModal() {
            document.getElementById('newTopicModal').style.display = 'none';
        }

        // Close modal when clicking outside
        window.onclick = function(event) {
            const modal = document.getElementById('newTopicModal');
            if (event.target == modal) {
                modal.style.display = 'none';
            }
        }
    </script>
</body>
</html> 