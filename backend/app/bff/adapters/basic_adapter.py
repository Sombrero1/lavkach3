from core.fastapi.adapters import BaseAdapter

class BasicAdapter(BaseAdapter):
    module = 'basic'


    async def refresh_token(self, refresh_schema):
        path = f'/api/basic/user/refresh'
        body = {
            'token': refresh_schema.token,
            'refresh_token': refresh_schema.refresh_token
        }
        responce = await self.client.post(self.domain + path, json=body, params=None)
        return responce.json()

    async def user_company_change(self, user_id, company_id):
        path = '/api/basic/user/company_change'
        body = {
            'user_id': user_id,
            'company_id': company_id
        }
        responce = await self.client.post(self.domain + path, json=body, params=None)
        return responce.json()

    async def login(self, username, password):
        path = f'/api/basic/user/login'
        body = {
            'email': username,
            'password': password
        }
        responce = await self.client.post(self.domain + path, json=body, params=None)
        return responce.json()

    async def dropdown_ids(self, model: str, id: str, itemlink: str, is_named=False, message=None):
        """
            Виджет на вход получает модуль-модель-ид- и обратную ссылку если нужно, если нет будет /module/model/{id}
            _named означает, что так же будет отдат name для отрисовки на тайтле кнопки
        """
        data = await self.list(model=model)
        items = []
        title = False
        for i in data.get('data'):
            if i['id'] == id:
                title = i['title']
            items.append({
                'title': i['title'],
                'url': f'{itemlink}/{i["id"]}' if itemlink else f'/{self.module}/{model}/{i["id"]}'
                # Если нет ссылки то отдаем ссылку на обьекты по умолчанию (form)
            })
        return {
            'model': model,
            'module': self.module,
            'title': title,
            'message': message,
            'items': items
        }