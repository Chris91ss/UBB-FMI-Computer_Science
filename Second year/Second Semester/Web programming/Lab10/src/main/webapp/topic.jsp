<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>
<!DOCTYPE html>
<html>
<head>
    <title>Forum - ${topic.title}</title>
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
            margin-bottom: 20px;
        }
        .back-link {
            color: #666;
            text-decoration: none;
            margin-bottom: 10px;
            display: inline-block;
        }
        .back-link:hover {
            color: #333;
        }
        h1 {
            margin: 0 0 10px 0;
            color: #333;
        }
        .topic-meta {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 20px;
        }
        .post-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        .post-item {
            padding: 15px;
            border-bottom: 1px solid #eee;
        }
        .post-item:last-child {
            border-bottom: none;
        }
        .post-content {
            margin: 10px 0;
            line-height: 1.5;
        }
        .post-meta {
            color: #666;
            font-size: 0.9em;
        }
        .post-actions {
            margin-top: 10px;
        }
        .delete-post {
            color: #f44336;
            text-decoration: none;
            font-size: 0.9em;
        }
        .delete-post:hover {
            text-decoration: underline;
        }
        .new-post {
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #666;
        }
        textarea {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
            min-height: 100px;
            resize: vertical;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
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
            <a href="${pageContext.request.contextPath}/topics" class="back-link">← Back to Topics</a>
            <h1>${topic.title}</h1>
            <div class="topic-meta">
                Posted by ${topic.username} on 
                <fmt:formatDate value="${topic.createdAt}" pattern="MMM dd, yyyy HH:mm"/>
            </div>
        </div>

        <ul class="post-list">
            <c:forEach items="${posts}" var="post">
                <li class="post-item">
                    <div class="post-content">${post.content}</div>
                    <div class="post-meta">
                        Posted by ${post.username} on 
                        <fmt:formatDate value="${post.createdAt}" pattern="MMM dd, yyyy HH:mm"/>
                    </div>
                    <c:if test="${post.userId == sessionScope.user.id}">
                        <div class="post-actions">
                            <form action="${pageContext.request.contextPath}/posts" method="post" style="display: inline;">
                                <input type="hidden" name="action" value="delete">
                                <input type="hidden" name="postId" value="${post.id}">
                                <input type="hidden" name="topicId" value="${topic.id}">
                                <a href="#" onclick="if(confirm('Are you sure you want to delete this post?')) this.parentElement.submit(); return false;"
                                   class="delete-post">Delete</a>
                            </form>
                        </div>
                    </c:if>
                </li>
            </c:forEach>
        </ul>

        <div class="new-post">
            <h2>Add a Reply</h2>
            <form action="${pageContext.request.contextPath}/posts" method="post">
                <input type="hidden" name="action" value="create">
                <input type="hidden" name="topicId" value="${topic.id}">
                <div class="form-group">
                    <label for="content">Your Reply:</label>
                    <textarea id="content" name="content" required></textarea>
                </div>
                <button type="submit">Post Reply</button>
            </form>
        </div>
    </div>
</body>
</html> 