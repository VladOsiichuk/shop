from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from src.shop.orders.interfaces import (
    CreateNewOrderUseCase,
    AddOrderLineUseCase,
    OrderDoesNotExists,
)
from src.shop.orders.schemas import (
    AddNewOrderResponseSchema,
    AddOrderLineRequestSchema,
    AddOrderLineResponseSchema,
)
from src.shop.products.interfaces import ProductDoesNotExists

router = APIRouter()


@router.post(path="/add/", response_model=AddNewOrderResponseSchema)
@inject
async def create_new_order(
    create_order_use_case: CreateNewOrderUseCase = Depends(
        Provide["order_use_cases.create_order"]
    ),
):
    order = await create_order_use_case()
    return order


@router.post(path="/{order_id}/lines/add/", response_model=AddOrderLineResponseSchema)
@inject
async def create_order_item(
    order_id: int,
    request_data: AddOrderLineRequestSchema,
    add_order_line_use_case: AddOrderLineUseCase = Depends(
        Provide["order_use_cases.add_order_line"]
    ),
):
    try:
        order_line = await add_order_line_use_case(
            order_id=order_id, product_id=request_data.product_id, qty=request_data.qty
        )
    except (OrderDoesNotExists, ProductDoesNotExists) as err:
        raise HTTPException(status_code=400, detail=str(err))
    else:
        return order_line
