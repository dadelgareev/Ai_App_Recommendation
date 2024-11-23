import grpc
from concurrent import futures
import scraper_pb2
import scraper_pb2_grpc

class ScraperService(scraper_pb2_grpc.ScraperServiceServicer):

    # Метод 1: Передача категории, подкатегории и списка тегов
    def SendCategoryInfo(self, request, context):
        print(f"Получена категория: {request.category}, подкатегория: {request.subcategory}, теги: {(request.tags)}")
        return scraper_pb2.CategoryResponse(success=True, message="Категория получена")

    # Метод 2: Передача подкатегории и списка тегов
    def SendSubcategoryInfo(self, request, context):
        print(f"Получена подкатегория: {request.subcategory}, теги: {(request.tags)}")
        return scraper_pb2.CategoryResponse(success=True, message="Подкатегория получена")

    # Метод 3: Обновление тегов для существующей подкатегории
    def UpdateSubcategoryTags(self, request, context):
        print(f"Обновление тегов для подкатегории: {request.subcategory}, новые теги: {(request.tags)}")
        return scraper_pb2.CategoryResponse(success=True, message="Теги обновлены")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    scraper_pb2_grpc.add_ScraperServiceServicer_to_server(ScraperService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Сервер запущен на порту 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
