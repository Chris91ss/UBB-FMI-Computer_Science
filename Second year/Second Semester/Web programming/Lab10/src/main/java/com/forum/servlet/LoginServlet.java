package com.forum.servlet;

import com.forum.dao.UserDAO;
import com.forum.model.User;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;
import java.sql.SQLException;

@WebServlet("/login")
public class LoginServlet extends HttpServlet {
    private UserDAO userDAO;

    @Override
    public void init() throws ServletException {
        userDAO = new UserDAO();
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String username = request.getParameter("username");
        String password = request.getParameter("password");
        String action = request.getParameter("action");

        try {
            if ("register".equals(action)) {
                if (userDAO.isUsernameExists(username)) {
                    request.setAttribute("error", "Username already exists");
                    request.getRequestDispatcher("/login.jsp").forward(request, response);
                    return;
                }
                User user = userDAO.register(username, password);
                HttpSession session = request.getSession();
                session.setAttribute("user", user);
                response.sendRedirect("topics");
            } else {
                User user = userDAO.authenticate(username, password);
                if (user != null) {
                    HttpSession session = request.getSession();
                    session.setAttribute("user", user);
                    response.sendRedirect("topics");
                } else {
                    request.setAttribute("error", "Invalid username or password");
                    request.getRequestDispatcher("/login.jsp").forward(request, response);
                }
            }
        } catch (SQLException e) {
            throw new ServletException("Database error", e);
        }
    }

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        request.getRequestDispatcher("/login.jsp").forward(request, response);
    }
} 