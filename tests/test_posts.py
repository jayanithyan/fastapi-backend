import pytest
from fastapi import status
from schemas.post import PostCreate, PostResponse


class TestPostCreate:
    """Test post creation."""
    
    def test_create_post_success(self, client, db):
        """Test successful post creation."""
        post_data = {
            "title": "Test Post",
            "content": "This is a test post",
            "published": True,
            "rating": 4.5,
        }
        response = client.post("/api/v1/posts", json=post_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == "Test Post"
        assert data["content"] == "This is a test post"
        assert data["published"] is True
        assert data["rating"] == 4.5
        assert "id" in data
        assert "created_at" in data
    
    def test_create_post_missing_title(self, client, db):
        """Test post creation with missing title."""
        post_data = {
            "content": "This is a test post",
            "published": True,
        }
        response = client.post("/api/v1/posts", json=post_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestPostRead:
    """Test post reading."""
    
    def test_get_posts_empty(self, client, db):
        """Test getting posts when database is empty."""
        response = client.get("/api/v1/posts")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 0
        assert data["items"] == []
    
    def test_get_posts_with_data(self, client, db):
        """Test getting posts with data."""
        # Create a post first
        post_data = {
            "title": "Test Post",
            "content": "Content",
            "published": True,
        }
        client.post("/api/v1/posts", json=post_data)
        
        response = client.get("/api/v1/posts")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 1
        assert len(data["items"]) == 1
    
    def test_get_post_by_id_success(self, client, db):
        """Test getting a post by ID."""
        # Create a post
        post_data = {
            "title": "Test Post",
            "content": "Content",
            "published": True,
        }
        create_response = client.post("/api/v1/posts", json=post_data)
        post_id = create_response.json()["id"]
        
        # Get the post
        response = client.get(f"/api/v1/posts/{post_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == post_id
        assert data["title"] == "Test Post"
    
    def test_get_post_by_id_not_found(self, client, db):
        """Test getting a post that doesn't exist."""
        response = client.get("/api/v1/posts/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestPostUpdate:
    """Test post updates."""
    
    def test_update_post_success(self, client, db):
        """Test successful post update."""
        # Create a post
        post_data = {
            "title": "Original Title",
            "content": "Original Content",
            "published": True,
        }
        create_response = client.post("/api/v1/posts", json=post_data)
        post_id = create_response.json()["id"]
        
        # Update the post
        update_data = {
            "title": "Updated Title",
            "rating": 5.0,
        }
        response = client.put(f"/api/v1/posts/{post_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["rating"] == 5.0
        assert data["content"] == "Original Content"  # Should remain unchanged


class TestPostDelete:
    """Test post deletion."""
    
    def test_delete_post_success(self, client, db):
        """Test successful post deletion."""
        # Create a post
        post_data = {
            "title": "Test Post",
            "content": "Content",
        }
        create_response = client.post("/api/v1/posts", json=post_data)
        post_id = create_response.json()["id"]
        
        # Delete the post
        response = client.delete(f"/api/v1/posts/{post_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify it's deleted
        get_response = client.get(f"/api/v1/posts/{post_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND


class TestPostFiltering:
    """Test post filtering."""
    
    def test_filter_published_posts(self, client, db):
        """Test filtering published posts."""
        # Create posts
        client.post("/api/v1/posts", json={"title": "Published", "content": "C", "published": True})
        client.post("/api/v1/posts", json={"title": "Unpublished", "content": "C", "published": False})
        
        response = client.get("/api/v1/posts?published=true")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["published"] is True
    
    def test_filter_by_rating(self, client, db):
        """Test filtering posts by rating."""
        # Create posts
        client.post("/api/v1/posts", json={"title": "High Rated", "content": "C", "rating": 4.5})
        client.post("/api/v1/posts", json={"title": "Low Rated", "content": "C", "rating": 2.0})
        
        response = client.get("/api/v1/posts?min_rating=3")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["title"] == "High Rated"


class TestHealthCheck:
    """Test health check endpoint."""
    
    def test_health_check(self, client):
        """Test health check."""
        response = client.get("/api/health")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
