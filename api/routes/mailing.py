from fastapi import APIRouter, Depends
from api.services.mailing import MailingService
from api.schemas.mailing import MailingCreateSchema, MailingUpdateSchema, MailingSchema


router = APIRouter(prefix="/api/mailing", tags=["Mailing"])


@router.post('', response_model=MailingSchema, status_code=201)
async def create_mailing(schema: MailingCreateSchema, service: MailingService = Depends()):
    return await service.create(schema)


@router.get('', response_model=list[MailingSchema])
async def list_mailings(service: MailingService = Depends()):
    return await service.list()


@router.get('/{mailing_id}', response_model=MailingSchema)
async def get_mailing(mailing_id: int, service: MailingService = Depends()):
    return await service.get(mailing_id)


@router.delete("/{mailing_id}", status_code=204)
async def delete_mailing(mailing_id: int, service: MailingService = Depends()):
    await service.delete(mailing_id)


@router.patch("/{mailing_id}", response_model=MailingSchema)
async def update_mailing(mailing_id: int, schema: MailingUpdateSchema, service: MailingService = Depends()):
    return await service.update(mailing_id, schema)


@router.post("/{mailing_id}/send")
async def send_mailing(mailing_id: int, service: MailingService = Depends()):
    await service.send(mailing_id)

