from abc import ABCMeta, abstractmethod
from typing import Optional, Protocol, List

from pydantic import Field, BaseModel

from src.shop.interfaces import DomainError


class Order(BaseModel):
    id: Optional[int]
    status: Optional[str] = Field(default="new")
    receiver_phone_number: Optional[str] = None

    class Config:
        orm_mode = True
        validate_assignment = True


class OrderLine(BaseModel):
    id: Optional[int]
    order_id: int
    product_id: int
    qty: int

    class Config:
        orm_mode = True
        validate_assignment = True


class OrderIsEmptyError(DomainError):
    pass


class OrderDoesNotExists(DomainError):
    pass


class CheckoutOrderService(metaclass=ABCMeta):
    @abstractmethod
    async def checkout(self, order: Order, receiver_phone_number: str) -> Order:
        """
        Checkout order
        Args:
            order: Order instance
            receiver_phone_number: receiver phone number

        Returns:
            Updated order instance
        """


class OrderRepository(metaclass=ABCMeta):
    @abstractmethod
    async def get(self, order_id) -> Optional[Order]:
        """
        Args:
            order_id: ID of the order
        Returns:
            Order if present else None
        """
        pass

    @abstractmethod
    async def persist(self, order: Order) -> Order:
        """
        Create a new order
        Returns:
            Order instance
        """
        pass


class OrderLineRepository(metaclass=ABCMeta):
    @abstractmethod
    async def get_by_order_id(self, order_id: int) -> List[OrderLine]:
        """
        Args:
            order_id: Order id

        Returns:
            OrderLines
        """
        pass

    @abstractmethod
    async def persist(self, order_line: OrderLine) -> OrderLine:
        """
        Persist order
        Args:
            order_line: OrderLine instance

        Returns:
            OrderLine instance
        """
        pass


class AddOrderLineUseCase(Protocol):
    async def __call__(
        self, order_id: int, product_id: int, qty: Optional[int] = 1
    ) -> OrderLine:
        """
        As a customer user, I want to add a new item to my order
        Args:
            order_id: Order id
            product_id: Product id
            qty: quantity
        Returns:
            OrderLine
        """


class CreateNewOrderUseCase(Protocol):
    async def __call__(self) -> Order:
        """
        As a shop customer, I want to create a new order
        Returns: Order instance
        """
        pass


class CheckoutOrderUseCase(Protocol):
    async def __call__(self, *, order_id: int, receiver_phone_number: str) -> Order:
        """
        As a shop customer, I want to checkout my order
        Args:
            order_id: Order
            receiver_phone_number: customer phone number
        Returns:
            Updated order instance
        """


class ViewFullOrderUseCase(Protocol):
    def __call__(self, order_id: int) -> None:
        """
        As a shop customer, I want to view the whole my order, including order lines and products
        """
