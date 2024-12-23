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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rscraper.proto\x12\x07scraper\"\x13\n\x03Tag\x12\x0c\n\x04name\x18\x01 \x01(\t\"\xab\x01\n\x15TagsByCategoryRequest\x12L\n\x10tags_by_category\x18\x01 \x03(\x0b\x32\x32.scraper.TagsByCategoryRequest.TagsByCategoryEntry\x1a\x44\n\x13TagsByCategoryEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x1c\n\x05value\x18\x02 \x01(\x0b\x32\r.scraper.Tags:\x02\x38\x01\"\"\n\x04Tags\x12\x1a\n\x04tags\x18\x01 \x03(\x0b\x32\x0c.scraper.Tag\"(\n\x16TagsByCategoryResponse\x12\x0e\n\x06status\x18\x01 \x01(\t\"\x1b\n\x0bSubcategory\x12\x0c\n\x04name\x18\x01 \x01(\t\"\xe1\x01\n\x1eSubcategoriesByCategoryRequest\x12g\n\x19subcategories_by_category\x18\x01 \x03(\x0b\x32\x44.scraper.SubcategoriesByCategoryRequest.SubcategoriesByCategoryEntry\x1aV\n\x1cSubcategoriesByCategoryEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12%\n\x05value\x18\x02 \x01(\x0b\x32\x16.scraper.Subcategories:\x02\x38\x01\"<\n\rSubcategories\x12+\n\rsubcategories\x18\x01 \x03(\x0b\x32\x14.scraper.Subcategory\"1\n\x1fSubcategoriesByCategoryResponse\x12\x0e\n\x06status\x18\x01 \x01(\t\"8\n\x13ParsedCSVRowRequest\x12\x10\n\x08\x63\x61tegory\x18\x01 \x01(\t\x12\x0f\n\x07\x63sv_row\x18\x02 \x01(\t\"&\n\x14ParsedCSVRowResponse\x12\x0e\n\x06status\x18\x01 \x01(\t2\xaa\x02\n\x0eScraperService\x12U\n\x12SendTagsByCategory\x12\x1e.scraper.TagsByCategoryRequest\x1a\x1f.scraper.TagsByCategoryResponse\x12p\n\x1bSendSubcategoriesByCategory\x12\'.scraper.SubcategoriesByCategoryRequest\x1a(.scraper.SubcategoriesByCategoryResponse\x12O\n\x10SendParsedCSVRow\x12\x1c.scraper.ParsedCSVRowRequest\x1a\x1d.scraper.ParsedCSVRowResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'scraper_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_TAGSBYCATEGORYREQUEST_TAGSBYCATEGORYENTRY']._loaded_options = None
  _globals['_TAGSBYCATEGORYREQUEST_TAGSBYCATEGORYENTRY']._serialized_options = b'8\001'
  _globals['_SUBCATEGORIESBYCATEGORYREQUEST_SUBCATEGORIESBYCATEGORYENTRY']._loaded_options = None
  _globals['_SUBCATEGORIESBYCATEGORYREQUEST_SUBCATEGORIESBYCATEGORYENTRY']._serialized_options = b'8\001'
  _globals['_TAG']._serialized_start=26
  _globals['_TAG']._serialized_end=45
  _globals['_TAGSBYCATEGORYREQUEST']._serialized_start=48
  _globals['_TAGSBYCATEGORYREQUEST']._serialized_end=219
  _globals['_TAGSBYCATEGORYREQUEST_TAGSBYCATEGORYENTRY']._serialized_start=151
  _globals['_TAGSBYCATEGORYREQUEST_TAGSBYCATEGORYENTRY']._serialized_end=219
  _globals['_TAGS']._serialized_start=221
  _globals['_TAGS']._serialized_end=255
  _globals['_TAGSBYCATEGORYRESPONSE']._serialized_start=257
  _globals['_TAGSBYCATEGORYRESPONSE']._serialized_end=297
  _globals['_SUBCATEGORY']._serialized_start=299
  _globals['_SUBCATEGORY']._serialized_end=326
  _globals['_SUBCATEGORIESBYCATEGORYREQUEST']._serialized_start=329
  _globals['_SUBCATEGORIESBYCATEGORYREQUEST']._serialized_end=554
  _globals['_SUBCATEGORIESBYCATEGORYREQUEST_SUBCATEGORIESBYCATEGORYENTRY']._serialized_start=468
  _globals['_SUBCATEGORIESBYCATEGORYREQUEST_SUBCATEGORIESBYCATEGORYENTRY']._serialized_end=554
  _globals['_SUBCATEGORIES']._serialized_start=556
  _globals['_SUBCATEGORIES']._serialized_end=616
  _globals['_SUBCATEGORIESBYCATEGORYRESPONSE']._serialized_start=618
  _globals['_SUBCATEGORIESBYCATEGORYRESPONSE']._serialized_end=667
  _globals['_PARSEDCSVROWREQUEST']._serialized_start=669
  _globals['_PARSEDCSVROWREQUEST']._serialized_end=725
  _globals['_PARSEDCSVROWRESPONSE']._serialized_start=727
  _globals['_PARSEDCSVROWRESPONSE']._serialized_end=765
  _globals['_SCRAPERSERVICE']._serialized_start=768
  _globals['_SCRAPERSERVICE']._serialized_end=1066
# @@protoc_insertion_point(module_scope)
