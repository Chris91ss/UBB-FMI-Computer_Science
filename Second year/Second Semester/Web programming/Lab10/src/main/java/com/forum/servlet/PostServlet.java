package com.forum.servlet;

import com.forum.dao.PostDAO;
import com.forum.model.Post;
import com.forum.model.User;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;
import java.sql.SQLException;

@WebServlet("/posts/*")
public class PostServlet extends HttpServlet {
    private PostDAO postDAO;

    @Override
    public void init() throws ServletException {
        postDAO = new PostDAO();
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
                String content = request.getParameter("content");
                int topicId = Integer.parseInt(request.getParameter("topicId"));
                Post post = new Post(content, topicId, user.getId());
                postDAO.create(post);
                response.sendRedirect(request.getContextPath() + "/topics/" + topicId);
            } else if ("delete".equals(action)) {
                int postId = Integer.parseInt(request.getParameter("postId"));
                int topicId = Integer.parseInt(request.getParameter("topicId"));
                
                if (postDAO.isPostOwner(postId, user.getId())) {
                    postDAO.deletePost(postId);
                }
                response.sendRedirect(request.getContextPath() + "/topics/" + topicId);
            } else {
                response.sendError(HttpServletResponse.SC_BAD_REQUEST);
            }
        } catch (SQLException e) {
            throw new ServletException("Database error", e);
        }
    }
} 