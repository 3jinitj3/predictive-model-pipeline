from app.schemas.services import ServiceData
from app.schemas.users import UserObject
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.services import Services
from app.db.models.sales_orders import SalesOrderHeaders, SalesOrderLines
from fastapi import HTTPException
from app.schemas.orders import SalesReceipt, SalesLineItems
from datetime import UTC, datetime, timedelta



class SalesService:

    async def get_service(self, service_id: int, db:AsyncSession) -> ServiceData:
        result = await db.execute(
            select(Services).where(Services.service_id == service_id)
        )
        service_type = result.scalar_one_or_none()
        if not service_type:
            raise HTTPException(status_code=404, detail='Invalid service id')
        return ServiceData(
            service_id=service_type.service_id,
            service=service_type.service,
            description=service_type.description,
            price=service_type.price
        )


    async def request_quote(self):
        pass


    async def create_sales_order(self, service_data:list[ServiceData], user_object:UserObject,  db:AsyncSession) -> SalesReceipt:
        if not user_object.role_id == 4:
            raise HTTPException(status_code=401, detail='Permission denied, user is not a buyer')
        receipt_line_items: list[SalesOrderLines] = []
        line_items: list[tuple[int, Services]] = []
        for line_number, sales_order_line in enumerate(service_data, start=1):
            result = await db.execute(
                select(Services).where(Services.service_id == sales_order_line.service_id)
            )
            service_ordered = result.scalar_one_or_none()
            if not service_ordered:
                raise HTTPException(status_code=404, detail='Invalid service id')
            line_items.append((line_number, service_ordered))
        gross_total = sum([item.price for _, item in line_items])            
        due_date = datetime.now(UTC) + timedelta(days=30)
        tax_rate = 0.06
        tax_amount = gross_total * tax_rate
        total = gross_total + tax_amount
        header = SalesOrderHeaders(
            org_id=user_object.org_id,
            user_id=user_object.user_id,
            buyer_name=f'{user_object.first_name} {user_object.last_name}',
            gross_total=gross_total,
            tax_rate=tax_rate,
            tax_amount=tax_amount,
            total=total,
            due_date=due_date
        )
        try:
            db.add(header)
            await db.flush()
            for line_item_number, item in line_items:
                order_line = SalesOrderLines(
                    sales_id=header.sales_id,
                    line_number=line_item_number,
                    service_id=item.service_id,
                    service=item.service,
                    description=item.description,
                    price=item.price
                )
                db.add(order_line)
                receipt_line_items.append(order_line)
            await db.flush()
            await db.commit()
            return SalesReceipt(
                sales_id=header.sales_id,
                items=receipt_line_items,
                gross_total=gross_total,
                tax_rate=tax_rate,
                tax_amount=tax_amount,
                total=gross_total + tax_amount
            )
        except Exception:
            await db.rollback()
            raise



sales_service = SalesService()