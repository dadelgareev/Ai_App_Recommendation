# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: scraper.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'scraper.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rscraper.proto\x12\x07scraper\"J\n\x13\x43\x61tegoryInfoRequest\x12\x10\n\x08\x63\x61tegory\x18\x01 \x01(\t\x12\x13\n\x0bsubcategory\x18\x02 \x01(\t\x12\x0c\n\x04tags\x18\x03 \x01(\t\";\n\x16SubcategoryInfoRequest\x12\x13\n\x0bsubcategory\x18\x01 \x01(\t\x12\x0c\n\x04tags\x18\x02 \x01(\t\"A\n\x1cUpdateSubcategoryTagsRequest\x12\x13\n\x0bsubcategory\x18\x01 \x01(\t\x12\x0c\n\x04tags\x18\x02 \x01(\t\"4\n\x10\x43\x61tegoryResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t2\x8b\x02\n\x0eScraperService\x12K\n\x10SendCategoryInfo\x12\x1c.scraper.CategoryInfoRequest\x1a\x19.scraper.CategoryResponse\x12Q\n\x13SendSubcategoryInfo\x12\x1f.scraper.SubcategoryInfoRequest\x1a\x19.scraper.CategoryResponse\x12Y\n\x15UpdateSubcategoryTags\x12%.scraper.UpdateSubcategoryTagsRequest\x1a\x19.scraper.CategoryResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'scraper_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_CATEGORYINFOREQUEST']._serialized_start=26
  _globals['_CATEGORYINFOREQUEST']._serialized_end=100
  _globals['_SUBCATEGORYINFOREQUEST']._serialized_start=102
  _globals['_SUBCATEGORYINFOREQUEST']._serialized_end=161
  _globals['_UPDATESUBCATEGORYTAGSREQUEST']._serialized_start=163
  _globals['_UPDATESUBCATEGORYTAGSREQUEST']._serialized_end=228
  _globals['_CATEGORYRESPONSE']._serialized_start=230
  _globals['_CATEGORYRESPONSE']._serialized_end=282
  _globals['_SCRAPERSERVICE']._serialized_start=285
  _globals['_SCRAPERSERVICE']._serialized_end=552
# @@protoc_insertion_point(module_scope)
