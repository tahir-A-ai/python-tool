from fastapi import APIRouter,Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List
from app.db import models
from app.schemas import review
from app.db.database import get_db
from app.routers.auth import get_current_user

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)

# POST: Creating a Review (Anyone logged in can post a review)
@router.post("/", response_model=review.ReviewResponse)
def create_review(
    review: review.ReviewCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # We don't trust the user to send their own ID. 
    # We take it from the token (current_user.id).
    new_review = models.Review(
        title=review.title,
        content=review.content,
        rating=review.rating,
        owner_id=current_user.id
    )
    
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    
    return new_review

# GET: Read Reviews (The Admin Logic)
@router.get("/", response_model=List[review.ReviewResponse])
def read_reviews(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Start with a generic query
    query = db.query(models.Review)
    
    # If they are NOT an admin, hiding the unapproved stuff.
    if not current_user.is_admin:
        query = query.filter(models.Review.is_approved == True)
    
    # If they ARE an admin, the filter is skipped, so they see everything.
    
    return query.all()


# PUT: endpoint to approve review by id (admin-restricted only)
@router.put("/{review_id}/approve", response_model=review.ReviewResponse)
def approve_review(
    review_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    # Security Check: Only Admins allowed
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to approve reviews")

    # Finding teh Review
    review_query = db.query(models.Review).filter(models.Review.id == review_id)
    review = review_query.first()

    # if not found , return error, else set approved=True and save review to db
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    review.is_approved = True
    db.commit()
    db.refresh(review)
    
    return review


# DELETE - REVIEW (Admin or Owner)
@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)):
    # 1. Find the review
    review_query = db.query(models.Review).filter(models.Review.id == review_id)
    review = review_query.first()

    # 2. Check if exists
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    # 3. Check Permissions (Admin OR Author)
    if review.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")

    # 4. Delete
    review_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# UPDATE - REVIEW (Author only, also must be unapproved, if it is approved, can't be edited)
@router.put("/{review_id}", response_model=review.ReviewResponse)
def update_review(
    review_id: int, 
    updated_post: review.ReviewCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    review_query = db.query(models.Review).filter(models.Review.id == review_id)
    review = review_query.first()

    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    # 3. check Ownership (Only Author can edit content)
    if review.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")

    # Lock if Approved
    if review.is_approved:
         raise HTTPException(
             status_code=403, 
             detail="Cannot edit a review after it has been approved. Please delete and repost."
         )

    # Update the fields
    # query object is used to update efficiently
    review_query.update(updated_post.model_dump(), synchronize_session=False)
    
    db.commit()
    
    # Return the updated object
    return review_query.first()