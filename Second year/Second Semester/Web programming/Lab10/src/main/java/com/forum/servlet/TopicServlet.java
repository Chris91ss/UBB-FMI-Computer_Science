package com.forum.servlet;

import com.forum.dao.TopicDAO;
import com.forum.dao.PostDAO;
import com.forum.model.Topic;
import com.forum.model.User;
import com.forum.model.Post;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;
import java.sql.SQLException;
import java.util.List;

@WebServlet("/topics/*")
public class TopicServlet extends HttpServlet {
    private TopicDAO topicDAO;

    @Override
    public void init() throws ServletException {
        topicDAO = new TopicDAO();
    }

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("user") == null) {
            response.sendRedirect("login");
            return;
        }

        String pathInfo = request.getPathInfo();
        if (pathInfo == null || pathInfo.equals("/")) {
            try {
                List<Topic> topics = topicDAO.getAllTopics();
                request.setAttribute("topics", topics);
                request.getRequestDispatcher("/topics.jsp").forward(request, response);
            } catch (SQLException e) {
                throw new ServletException("Database error", e);
            }
        } else {
            try {
                int topicId = Integer.parseInt(pathInfo.substring(1));
                Topic topic = topicDAO.getTopicById(topicId);
                if (topic != null) {
                    PostDAO postDAO = new PostDAO();
                    List<Post> posts = postDAO.getPostsByTopicId(topicId);
                    request.setAttribute("topic", topic);
                    request.setAttribute("posts", posts);
                    request.getRequestDispatcher("/topic.jsp").forward(request, response);
                } else {
                    response.sendError(HttpServletResponse.SC_NOT_FOUND);
                }
            } catch (NumberFormatException | SQLException e) {
                response.sendError(HttpServletResponse.SC_BAD_REQUEST);
            }
        }
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("user") == null) {
            response.sendRedirect("login");
            return;
        }

        User user = (User) session.getAttribute("user");
        String action = request.getParameter("action");

        try {
            if ("create".equals(action)) {
                String title = request.getParameter("title");
                Topic topic = new Topic(title, user.getId());
                topicDAO.create(topic);
                response.sendRedirect("topics");
            } else if ("delete".equals(action)) {
                int topicId = Integer.parseInt(request.getParameter("topicId"));
                topicDAO.deleteTopic(topicId);
                response.sendRedirect("topics");
            } else {
                response.sendError(HttpServletResponse.SC_BAD_REQUEST);
            }
        } catch (SQLException e) {
            throw new ServletException("Database error", e);
        }
    }
} 