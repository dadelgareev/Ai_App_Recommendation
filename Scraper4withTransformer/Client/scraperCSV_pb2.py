# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: scraperCSV.proto
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
    'scraperCSV.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10scraperCSV.proto\"8\n\rUploadRequest\x12\x14\n\x0c\x66ile_content\x18\x01 \x01(\x0c\x12\x11\n\tfile_name\x18\x02 \x01(\t\"!\n\x0eUploadResponse\x12\x0f\n\x07message\x18\x01 \x01(\t2<\n\x0c\x46ileTransfer\x12,\n\tUploadCSV\x12\x0e.UploadRequest\x1a\x0f.UploadResponseB\x13\xaa\x02\x10GrpcFileTransferb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'scraperCSV_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\252\002\020GrpcFileTransfer'
  _globals['_UPLOADREQUEST']._serialized_start=20
  _globals['_UPLOADREQUEST']._serialized_end=76
  _globals['_UPLOADRESPONSE']._serialized_start=78
  _globals['_UPLOADRESPONSE']._serialized_end=111
  _globals['_FILETRANSFER']._serialized_start=113
  _globals['_FILETRANSFER']._serialized_end=173
# @@protoc_insertion_point(module_scope)
