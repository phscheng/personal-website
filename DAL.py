import sqlite3
import os
from datetime import datetime

class DataAccessLayer:
    def __init__(self, db_name="projects.db"):
        """Initialize the Data Access Layer with database connection"""
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        """Get a database connection"""
        return sqlite3.connect(self.db_name)
    
    def init_database(self):
        """Initialize the database and create tables if they don't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create projects table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                image_filename TEXT NOT NULL,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_project(self, title, description, image_filename):
        """Add a new project to the database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO projects (title, description, image_filename)
                VALUES (?, ?, ?)
            ''', (title, description, image_filename))
            
            conn.commit()
            project_id = cursor.lastrowid
            return project_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_all_projects(self):
        """Get all projects from the database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, description, image_filename, created_date, updated_date
            FROM projects
            ORDER BY created_date DESC
        ''')
        
        projects = cursor.fetchall()
        conn.close()
        return projects
    
    def get_project_by_id(self, project_id):
        """Get a specific project by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, description, image_filename, created_date, updated_date
            FROM projects
            WHERE id = ?
        ''', (project_id,))
        
        project = cursor.fetchone()
        conn.close()
        return project
    
    def update_project(self, project_id, title, description, image_filename):
        """Update an existing project"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE projects
                SET title = ?, description = ?, image_filename = ?, updated_date = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (title, description, image_filename, project_id))
            
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def delete_project(self, project_id):
        """Delete a project by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def search_projects(self, search_term):
        """Search projects by title or description"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, description, image_filename, created_date, updated_date
            FROM projects
            WHERE title LIKE ? OR description LIKE ?
            ORDER BY created_date DESC
        ''', (f'%{search_term}%', f'%{search_term}%'))
        
        projects = cursor.fetchall()
        conn.close()
        return projects



