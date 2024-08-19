"""
Food endpoints.py
"""

from __future__ import annotations

from typing import Annotated

import fastapi
import httpx

from vitaltrack import config

from . import schemas

router = fastapi.APIRouter()
user_router = fastapi.APIRouter()


@router.get(
    "/search",
    response_model=schemas.FoodsInSearchResponse,
    response_model_by_alias=False,
)
async def search(ingredient="", brand=""):
    # TODO: Error handling
    # TODO: Add validation to make sure ingredient of brand exists
    res = httpx.get(
        config.EDAMAM_PARSER_URL,
        params={
            "ingr": ingredient,
            "brand": brand,
            "nutrition-type": "logging",
        },
    )
    res_dict = res.json()

    all_food_list = []

    for food in res_dict["parsed"]:
        all_food_list.append(schemas.FoodEdamam(**food["food"]).model_dump())

    for food in res_dict["hints"]:
        all_food_list.append(schemas.FoodEdamam(**food["food"]).model_dump())

    return {
        "message": f"food search returned {len(res_dict['parsed']) + len(res_dict['hints']) } items",
        "data": {"suggested": [], "all": all_food_list},
    }


@router.post(
    "/nutrients",
    response_model=schemas.NutrientsInResponse,
    response_model_by_alias=False,
)
async def nutrients(ingredients: schemas.IngredientsInRequest):
    # TODO: Error handling

    res = httpx.post(
        config.EDAMAM_NUTRIENTS_URL,
        # TODO: Edamam doesn't allow multiple ingredients in request?
        json=ingredients.model_dump(by_alias=True),
    )
    res_dict = res.json()

    return {
        "message": "nutrients queried",
        "data": res_dict,
    }
