from enum import Enum


class PutawayStrategy(str, Enum):
    FEFO: str = 'fefo'
    FIFO: str = 'fifo'
    LIFO: str = 'lifo'
    LEFO: str = 'lefo'


class LocationClass(str, Enum):
    """
    **Классификация** типов местоположения, обозначающий свойства типов местоположения
    - partner - Зона внешняя (например поставщика товаров)
    - place - Статичный класс местоположения в пространстве, например ячейка на складе или магазине
    - zone - Зона, которая отвечает за агрегацию свойств местоположений, например стратегия приемки или отгрузки
    - resource - Статически/динамическое местоположение означающее ресурс с помощью которого происзодит перемещение, например Тележка, или штабелер или что то иное
    - package - Динамическое местоположение, например паллета коробка
    - lost - класс типа местоположения отвечающий аккумулирование расхождений в рамках набора локаций, может быть ограничен зоной, магазином или компанией
    - inventory - класс типов ячеек, которы аккумулирует расхождения при легальной инвентаризации
    - scrap - класс хранение некондиционного товара
    - scraped - списанный товар (уже утиилизарованный)
    - buffer - класс типов ячеек отвечающий за буфер приемки например за зону приемки или зону отгрузки
    -
    """
    PARTNER:    str = "partner"
    PLACE:      str = "place"
    RESOURCE:   str = "resource"
    PACKAGE:    str = "package"
    ZONE:       str = "zone"
    LOST:       str = "lost"
    INVENTORY:  str = "inventory"
    SCRAP:      str = "scrap"
    SCRAPPED:   str = "scrapped"
    BUFFER:     str = "buffer"


class VirtualLocationClass(str, Enum):
    PARTNER: str = "partner"
    LOST: str = "lost"
    INVENTORY: str = "inventory"
    SCRAPPED: str = "scrapped"
