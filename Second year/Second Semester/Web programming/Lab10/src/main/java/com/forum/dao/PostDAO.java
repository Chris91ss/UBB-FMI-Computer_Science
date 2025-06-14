package com.forum.dao;

import com.forum.model.Post;
import com.forum.util.DatabaseUtil;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class PostDAO {
    
    public Post create(Post post) throws SQLException {
        String query = "INSERT INTO posts (content, topic_id, user_id) VALUES (?, ?, ?)";
        try (Connection conn = DatabaseUtil.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(query, Statement.RETURN_GENERATED_KEYS)) {
            
            pstmt.setString(1, post.getContent());
            pstmt.setInt(2, post.getTopicId());
            pstmt.setInt(3, post.getUserId());
            
            int affectedRows = pstmt.executeUpdate();
            if (affectedRows == 0) {
                throw new SQLException("Creating post failed, no rows affected.");
            }
            
            try (ResultSet generatedKeys = pstmt.getGeneratedKeys()) {
                if (generatedKeys.next()) {
                    post.setId(generatedKeys.getInt(1));
                    return post;
                } else {
                    throw new SQLException("Creating post failed, no ID obtained.");
                }
            }
        }
    }
    
    public List<Post> getPostsByTopicId(int topicId) throws SQLException {
        List<Post> posts = new ArrayList<>();
        String query = "SELECT p.*, u.username FROM posts p " +
                      "JOIN users u ON p.user_id = u.id " +
                      "WHERE p.topic_id = ? " +
                      "ORDER BY p.created_at ASC";
        
        try (Connection conn = DatabaseUtil.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(query)) {
            
            pstmt.setInt(1, topicId);
            
            try (ResultSet rs = pstmt.executeQuery()) {
                while (rs.next()) {
                    Post post = new Post();
                    post.setId(rs.getInt("id"));
                    post.setContent(rs.getString("content"));
                    post.setTopicId(rs.getInt("topic_id"));
                    post.setUserId(rs.getInt("user_id"));
                    post.setCreatedAt(rs.getTimestamp("created_at"));
                    post.setUsername(rs.getString("username"));
                    posts.add(post);
                }
            }
        }
        return posts;
    }
    
    public void deletePost(int id) throws SQLException {
        String query = "DELETE FROM posts WHERE id = ?";
        try (Connection conn = DatabaseUtil.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(query)) {
            
            pstmt.setInt(1, id);
            pstmt.executeUpdate();
        }
    }
    
    public boolean isPostOwner(int postId, int userId) throws SQLException {
        String query = "SELECT COUNT(*) FROM posts WHERE id = ? AND user_id = ?";
        try (Connection conn = DatabaseUtil.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(query)) {
            
            pstmt.setInt(1, postId);
            pstmt.setInt(2, userId);
            
            try (ResultSet rs = pstmt.executeQuery()) {
                if (rs.next()) {
                    return rs.getInt(1) > 0;
                }
            }
        }
        return false;
    }
} 