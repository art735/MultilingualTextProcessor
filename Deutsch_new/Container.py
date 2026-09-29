# Контейнер для Dependency Injection
from dependency_injector import containers, providers

from SettingsManager import SettingsManager


class Container(containers.DeclarativeContainer):
    # deuSpaCyEngineWrapper = providers.Factory(DeuSpaCyEngineWrapper)
    # deuLemmaResolver = providers.Factory(DeuCoreLemmaResolver)
    # excelService = providers.Factory(ExcelService)
    # odtFilesService = providers.Factory(OdtFilesService)  # Фабрика для динамического создания экземпляров

    # a010_NewLemmasFinder не является ни полем класса, ни callback-функцией. Это объект, который можно вызывать как
    # функцию, и при этом он будет создавать новый экземпляр A010_NewLemmasFinder.
    # Это аналогично объявлению функции:
    # def create_A010_NewLemmasFinder():
    #    return A010_NewLemmasFinder(
    #        deuSpaCyEngineWrapper=deuSpaCyEngineWrapper,
    #        deuLemmaResolver=deuLemmaResolver,
    #        excelService=excelService,
    #        odtFilesService_factory=odtFilesService
    #    )
    # И newLemmasFinder() фактически вызывает этот код.
    # ИТОГ: newLemmasFinder — это объект-фабрика, который можно вызывать как функцию (newLemmasFinder()), чтобы
    # создавать новые экземпляры A010_NewLemmasFinder.
    # a010_NewLemmasFinder = providers.Factory(
    #     A010_NewLemmasFinder,
    #     deuSpaCyEngineWrapper=deuSpaCyEngineWrapper,
    #     deuLemmaResolver=deuLemmaResolver,
    #     excelService=excelService,
    #     odtFilesService_factory=odtFilesService
    # )

    settingsManager = providers.Singleton(SettingsManager)


################################

# Глобальный экземпляр контейнера, который используется во всех модулях проекта
CONTAINER = Container()
