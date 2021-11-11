from starlette.exceptions import HTTPException
from dependency_injector.wiring import inject, Provide
from fastapi import Depends

from src.shop.products.interfaces import (
    AddProductUseCase,
    ProductAlreadyExistsError,
    ViewAllProductsUseCase,
    ViewCategoryProducts,
)
from src.shop.products.schemas import (
    ProductResponseSchema,
    AddProductRequestSchema,
    ProductListResponseSchema,
)
from fastapi.routing import APIRouter


router = APIRouter()


@router.post(response_model=ProductResponseSchema, path="/add/")
@inject
async def add_product(
    data: AddProductRequestSchema,
    add_product_use_case: AddProductUseCase = Depends(
        Provide["product_use_cases.add_product"]
    ),
):
    data = data.dict()
    try:
        product = await add_product_use_case(
            name=data["name"],
            category=data.get("category"),
            price=data.get("price"),
            discount=data.get("discount"),
        )
    except ProductAlreadyExistsError as err:
        raise HTTPException(status_code=400, detail=str(err))
    else:
        return product


@router.get(path="/categories/{category}/", response_model=ProductListResponseSchema)
@inject
async def list_category_products(
    category: str,
    view_category_products_use_case: ViewCategoryProducts = Depends(
        Provide["product_use_cases.view_category_products"]
    ),
):
    products = await view_category_products_use_case(category=category)
    return {"results": products}


@router.get(path="/", response_model=ProductListResponseSchema)
@inject
async def list_products(
    list_all_products_use_case: ViewAllProductsUseCase = Depends(
        Provide["product_use_cases.view_all_products"]
    ),
):
    products = await list_all_products_use_case()
    return {"results": products}
