import datetime
import typing
import uuid

from pydantic import BaseModel
from enum import Enum
from inspect import isclass
from app.bff.bff_config import config
from core.types import TypeLocale, TypePhone, TypeCountry, TypeCurrency


def get_module_by_model(model):
    for k, v in config.services.items():
        if v['schema'].get(model):
            return k

def get_types(annotation, _class = []):
    """
        Рекурсивно берем типы в типах
    """
    if isclass(annotation):
        _class.append(annotation)
        return _class
    else:
        annotate = typing.get_args(annotation)
        origin = typing.get_origin(annotate)
        if origin:
            _class.append(origin)
        get_types(annotate[0], _class)
    return _class
def recognize_type(module: str, model: str, k: str, fielinfo):
    """
    Для шаблонизатора распознаем тип для удобства HTMX (универсальные компоненты)
    """
    res = ''
    enums = []
    class_types = get_types(fielinfo.annotation, [])
    for i, c in enumerate(class_types):
        if i > 0:
            res += '_'
        if issubclass(c, Enum):
            res += 'enum'
            enums = class_types[0]
        elif issubclass(class_types[0], dict):
            res += 'dict'
        elif issubclass(class_types[0], str):
            res += 'str'
        elif issubclass(class_types[0], int):
            res += 'number'
        elif issubclass(class_types[0], uuid.UUID):
            model_name = k.replace('_id', '')
            res += 'model_id'
            module = get_module_by_model(model_name)
            model = model_name
        elif issubclass(class_types[0], datetime.datetime):
            res += 'datetime'
        elif issubclass(class_types[0], BaseModel):
            model_name = k.replace('_rel', '')
            res += 'model_rel'
            module = get_module_by_model(model_name)
            model = model_name
        elif issubclass(class_types[0], TypeLocale):
            res += 'locale'
            model = 'locale'
        elif issubclass(class_types[0], TypeCurrency):
            res += 'currency'
            model = 'currency'
        elif issubclass(class_types[0], TypeCountry):
            res += 'country'
            model = 'country'
        elif issubclass(class_types[0], TypePhone):
            res += 'phone'
            model = 'phone'
    return {
        'type': res,
        'module': module,
        'model': model,
        'required': fielinfo.is_required(),
        'title': fielinfo.title,
        'enums': enums,
        # в какие UI виджеты поле доступно filter, card, table, form
        'widget': fielinfo.json_schema_extra or {},

    }


def get_columns(module: str, model: str, schema: BaseModel, data: list = None, exclude: list[str] = []):
    """
        Метод отдает типы полей для того, что бы строить фронтенд
    """
    columns = {}
    for k, v in schema.model_fields.items():
        if k in exclude: continue
        columns.update({
            k: recognize_type(module, model, k, v)
        })
    if data:
        for row in data:
            for col, val in row.items():
                if col in exclude: continue
                row[col] = {
                    **columns.get(col, {}),
                    'val': datetime.datetime.fromisoformat(val) if columns.get(col, {}).get('type') == 'datetime' else val
                }
    return columns, data