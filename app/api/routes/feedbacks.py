from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, status, Body
from fastapi.exceptions import HTTPException

from app.api.dependencies.database import get_repository
from app.db.errors.common import EntityDoesNotExistError, EntityCreateError
from app.db.repositories.feedbacks import FeedbacksRepository
from app.models.feedback import Feedback, InsertFeedback, UpdateFeedback

router = APIRouter()


@router.get("/", response_model=List[Feedback])
async def get_all(
        title: Optional[str] = None,
        user_id: Optional[UUID] = None,
        product_id: Optional[UUID] = None,
        only_products: bool = False,
        shop_id: Optional[UUID] = None,
        only_shops: bool = False,
        date: Optional[date] = None,
        before_date: Optional[date] = None,
        after_date: Optional[date] = None,
        sorted_by: Optional[str] = None,
        reverse: bool = False,
        feedbacks_repo: FeedbacksRepository = Depends(get_repository(FeedbacksRepository))
) -> List[Feedback]:
    feedbacks = await feedbacks_repo.get_all()

    filtered_feedbacks = []
    for feedback in feedbacks:
        is_fit = feedback.filter(
            title=title,
            user_id=user_id,
            product_id=product_id,
            only_products=only_products,
            shop_id=shop_id,
            only_shops=only_shops,
            date=date,
            before_date=before_date,
            after_date=after_date
        )
        if is_fit:
            filtered_feedbacks.append(feedback)

    if sorted_by is not None and filtered_feedbacks:
        print(filtered_feedbacks[0].__dict__.keys())
        if sorted_by not in filtered_feedbacks[0].__dict__.keys():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str('Model Feedback has no attribute: ' + sorted_by))
        else:
            filtered_feedbacks.sort(key=lambda feedback: getattr(feedback, sorted_by), reverse=reverse)

    return filtered_feedbacks


@router.post("/", response_model=Feedback, status_code=status.HTTP_201_CREATED)
async def create(
        feedback_body: InsertFeedback = Body(..., embed=False),
        feedbacks_repo: FeedbacksRepository = Depends(get_repository(FeedbacksRepository))
) -> Feedback:
    try:
        title = feedback_body.title
        positive_msg = feedback_body.positive_msg
        negative_msg = feedback_body.negative_msg
        message = feedback_body.message
        user_id = feedback_body.user_id
        product_id = feedback_body.product_id
        shop_id = feedback_body.shop_id

        feedback = await feedbacks_repo.create(
            title=title,
            positive_msg=positive_msg,
            negative_msg=negative_msg,
            message=message,
            user_id=user_id,
            product_id=product_id,
            shop_id=shop_id
        )
    except EntityCreateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return feedback


@router.get("/{id}", response_model=Feedback)
async def get_by_id(
        id: UUID,
        feedbacks_repo: FeedbacksRepository = Depends(get_repository(FeedbacksRepository))
) -> Feedback:
    try:
        feedback = await feedbacks_repo.get_by_id(id)
    except EntityDoesNotExistError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return feedback


@router.put("/{id}", response_model=Feedback)
async def update(
        id: UUID,
        feedback_body: UpdateFeedback = Body(..., embed=False),
        feedbacks_repo: FeedbacksRepository = Depends(get_repository(FeedbacksRepository))
) -> Feedback:
    try:
        feedback = await feedbacks_repo.get_by_id(id=id)

        title = feedback_body.title
        positive_msg = feedback_body.positive_msg
        negative_msg = feedback_body.negative_msg
        message = feedback_body.message

        if title is None:
            title = feedback.title
        if positive_msg is None:
            positive_msg = feedback.positive_msg
        if negative_msg is None:
            negative_msg = feedback.negative_msg
        if message is None:
            message = feedback.message
        updated_feedback = await feedbacks_repo.update_by_id(id=id, title=title, positive_msg=positive_msg,
                                                             negative_msg=negative_msg, message=message)
    except EntityCreateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return updated_feedback


@router.delete("/{id}", response_model=Feedback)
async def delete(
        id: UUID,
        feedbacks_repo: FeedbacksRepository = Depends(get_repository(FeedbacksRepository))
) -> Feedback:
    try:
        feedback = await feedbacks_repo.delete_by_id(id)
    except EntityDoesNotExistError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return feedback
