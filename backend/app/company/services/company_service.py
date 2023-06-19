from backend.app.company.models.company_models import Company
from backend.app.company.schemas.company_schemas import CompanyCreateScheme, CompanyUpdateScheme
from backend.core.db.session import session
from backend.core.service.base import BaseService


class CompanyService(BaseService[Company, CompanyCreateScheme, CompanyUpdateScheme]):
    def __init__(self, db_session: session=session):
        super(CompanyService, self).__init__(Company, db_session)


