import grpc
from concurrent import futures
import scraper_pb2
import scraper_pb2_grpc

class ScraperServiceServicer(scraper_pb2_grpc.ScraperServiceServicer):

    def SendTagsByCategory(self, request, context):
        for category, tags_obj in request.tags_by_category.items():
            tags = [tag.name for tag in tags_obj.tags]
            print(f"Category: {category}, Tags: {tags}")
        return scraper_pb2.TagsByCategoryResponse(status="Tags received successfully")

    def SendSubcategoriesByCategory(self, request, context):
        for category, subcategories_obj in request.subcategories_by_category.items():
            subcategories = [subcat.name for subcat in subcategories_obj.subcategories]
            print(f"Category: {category}, Subcategories: {subcategories}")
        return scraper_pb2.SubcategoriesByCategoryResponse(status="Subcategories received successfully")

    def SendParsedCSVRow(self, request, context):
        print(f"Category: {request.category}, CSV Row: {request.csv_row}")
        return scraper_pb2.ParsedCSVRowResponse(status="CSV Row received successfully")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    scraper_pb2_grpc.add_ScraperServiceServicer_to_server(ScraperServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
