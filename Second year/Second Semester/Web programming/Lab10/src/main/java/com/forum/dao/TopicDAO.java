package com.forum.dao;

import com.forum.model.Topic;
import com.forum.util.DatabaseUtil;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class TopicDAO {
    
    public Topic create(Topic topic) throws SQLException {
        String query = "INSERT INTO topics (title, user_id) VALUES (?, ?)";
        try (Connection conn = DatabaseUtil.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(query, Statement.RETURN_GENERATED_KEYS)) {
            
            pstmt.setString(1, topic.getTitle());
            pstmt.setInt(2, topic.getUserId());
            
            int affectedRows = pstmt.executeUpdate();
            if (affectedRows == 0) {
                throw new SQLException("Creating topic failed, no rows affected.");
            }
            
            try (ResultSet generatedKeys = pstmt.getGeneratedKeys()) {
                if (generatedKeys.next()) {
                    topic.setId(generatedKeys.getInt(1));
                    return topic;
                } else {
                    throw new SQLException("Creating topic failed, no ID obtained.");
                }
            }
        }
    }
    
    public List<Topic> getAllTopics() throws SQLException {
        List<Topic> topics = new ArrayList<>();
        String query = "SELECT t.*, u.username FROM topics t " +
                      "JOIN users u ON t.user_id = u.id " +
                      "ORDER BY t.created_at DESC";
        
        try (Connection conn = DatabaseUtil.getConnection();
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(query)) {
            
            while (rs.next()) {
                Topic topic = new Topic();
                topic.setId(rs.getInt("id"));
                topic.setTitle(rs.getString("title"));
                topic.setUserId(rs.getInt("user_id"));
                topic.setCreatedAt(rs.getTimestamp("created_at"));
                topic.setUsername(rs.getString("username"));
                topics.add(topic);
            }
        }
        return topics;
    }
    
    public Topic getTopicById(int id) throws SQLException {
        String query = "SELECT t.*, u.username FROM topics t " +
                      "JOIN users u ON t.user_id = u.id " +
                      "WHERE t.id = ?";
        
        try (Connection conn = DatabaseUtil.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(query)) {
            
            pstmt.setInt(1, id);
            
            try (ResultSet rs = pstmt.executeQuery()) {
                if (rs.next()) {
                    Topic topic = new Topic();
                    topic.setId(rs.getInt("id"));
                    topic.setTitle(rs.getString("title"));
                    topic.setUserId(rs.getInt("user_id"));
                    topic.setCreatedAt(rs.getTimestamp("created_at"));
                    topic.setUsername(rs.getString("username"));
                    return topic;
                }
            }
        }
        return null;
    }
    
    public void deleteTopic(int id) throws SQLException {
        String query = "DELETE FROM topics WHERE id = ?";
        try (Connection conn = DatabaseUtil.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(query)) {
            
            pstmt.setInt(1, id);
            pstmt.executeUpdate();
        }
    }
} 