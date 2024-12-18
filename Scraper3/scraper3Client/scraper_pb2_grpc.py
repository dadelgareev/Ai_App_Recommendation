# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import scraper_pb2 as scraper__pb2

GRPC_GENERATED_VERSION = '1.67.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in scraper_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class ScraperServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SendCategoryInfo = channel.unary_unary(
                '/scraper.ScraperService/SendCategoryInfo',
                request_serializer=scraper__pb2.CategoryInfoRequest.SerializeToString,
                response_deserializer=scraper__pb2.CategoryResponse.FromString,
                _registered_method=True)
        self.SendSubcategoryInfo = channel.unary_unary(
                '/scraper.ScraperService/SendSubcategoryInfo',
                request_serializer=scraper__pb2.SubcategoryInfoRequest.SerializeToString,
                response_deserializer=scraper__pb2.CategoryResponse.FromString,
                _registered_method=True)
        self.UpdateSubcategoryTags = channel.unary_unary(
                '/scraper.ScraperService/UpdateSubcategoryTags',
                request_serializer=scraper__pb2.UpdateSubcategoryTagsRequest.SerializeToString,
                response_deserializer=scraper__pb2.CategoryResponse.FromString,
                _registered_method=True)


class ScraperServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SendCategoryInfo(self, request, context):
        """Метод 1: Передача категории, подкатегории и списка тегов
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendSubcategoryInfo(self, request, context):
        """Метод 2: Передача подкатегории и списка тегов
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateSubcategoryTags(self, request, context):
        """Метод 3: Обновление тегов для существующей подкатегории
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ScraperServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SendCategoryInfo': grpc.unary_unary_rpc_method_handler(
                    servicer.SendCategoryInfo,
                    request_deserializer=scraper__pb2.CategoryInfoRequest.FromString,
                    response_serializer=scraper__pb2.CategoryResponse.SerializeToString,
            ),
            'SendSubcategoryInfo': grpc.unary_unary_rpc_method_handler(
                    servicer.SendSubcategoryInfo,
                    request_deserializer=scraper__pb2.SubcategoryInfoRequest.FromString,
                    response_serializer=scraper__pb2.CategoryResponse.SerializeToString,
            ),
            'UpdateSubcategoryTags': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateSubcategoryTags,
                    request_deserializer=scraper__pb2.UpdateSubcategoryTagsRequest.FromString,
                    response_serializer=scraper__pb2.CategoryResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'scraper.ScraperService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('scraper.ScraperService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class ScraperService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SendCategoryInfo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/scraper.ScraperService/SendCategoryInfo',
            scraper__pb2.CategoryInfoRequest.SerializeToString,
            scraper__pb2.CategoryResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SendSubcategoryInfo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/scraper.ScraperService/SendSubcategoryInfo',
            scraper__pb2.SubcategoryInfoRequest.SerializeToString,
            scraper__pb2.CategoryResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def UpdateSubcategoryTags(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/scraper.ScraperService/UpdateSubcategoryTags',
            scraper__pb2.UpdateSubcategoryTagsRequest.SerializeToString,
            scraper__pb2.CategoryResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
