# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: mom.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'mom.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tmom.proto\x12\x03mom\",\n\x08Response\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"\x07\n\x05\x45mpty\"4\n\x12\x43reateTopicRequest\x12\x10\n\x08topic_id\x18\x01 \x01(\t\x12\x0c\n\x04user\x18\x02 \x01(\t\"J\n\x15PublishMessageRequest\x12\x10\n\x08topic_id\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\t\x12\x0e\n\x06sender\x18\x03 \x01(\t\";\n\x10SubscribeRequest\x12\x10\n\x08topic_id\x18\x01 \x01(\t\x12\x15\n\rsubscriber_id\x18\x02 \x01(\t\"=\n\x12UnsubscribeRequest\x12\x10\n\x08topic_id\x18\x01 \x01(\t\x12\x15\n\rsubscriber_id\x18\x02 \x01(\t\"(\n\x05Topic\x12\x10\n\x08topic_id\x18\x01 \x01(\t\x12\r\n\x05\x61utor\x18\x02 \x01(\t\"(\n\x05Queue\x12\x10\n\x08topic_id\x18\x01 \x01(\t\x12\r\n\x05\x61utor\x18\x02 \x01(\t\"0\n\x12ListTopicsResponse\x12\x1a\n\x06topics\x18\x01 \x03(\x0b\x32\n.mom.Topic\">\n\x13PullMessagesRequest\x12\x10\n\x08topic_id\x18\x01 \x01(\t\x12\x15\n\rsubscriber_id\x18\x02 \x01(\t\"P\n\x10MessagesResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x1a\n\x04\x64\x61ta\x18\x03 \x03(\x0b\x32\x0c.mom.Message\"4\n\x12\x43reateQueueRequest\x12\x10\n\x08queue_id\x18\x01 \x01(\t\x12\x0c\n\x04user\x18\x02 \x01(\t\"0\n\x12ListQueuesResponse\x12\x1a\n\x06queues\x18\x01 \x03(\x0b\x32\n.mom.Queue\"\x17\n\x05Group\x12\x0e\n\x06queues\x18\x01 \x03(\t\"G\n\x12PushMessageRequest\x12\x10\n\x08queue_id\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\t\x12\x0e\n\x06sender\x18\x03 \x01(\t\"&\n\x12PullMessageRequest\x12\x10\n\x08queue_id\x18\x01 \x01(\t\"O\n\x0fMessageResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x1a\n\x04\x64\x61ta\x18\x03 \x01(\x0b\x32\x0c.mom.Message\"a\n\x07Message\x12\x12\n\nmessage_id\x18\x01 \x01(\t\x12\x0e\n\x06parent\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\x12\x0e\n\x06sender\x18\x04 \x01(\t\x12\x11\n\ttimestamp\x18\x05 \x01(\t\"4\n\x12\x44\x65leteTopicRequest\x12\x10\n\x08topic_id\x18\x01 \x01(\t\x12\x0c\n\x04user\x18\x02 \x01(\t2\x97\x03\n\x0cTopicService\x12\x35\n\x0b\x43reateTopic\x12\x17.mom.CreateTopicRequest\x1a\r.mom.Response\x12;\n\x0ePublishMessage\x12\x1a.mom.PublishMessageRequest\x1a\r.mom.Response\x12\x31\n\tSubscribe\x12\x15.mom.SubscribeRequest\x1a\r.mom.Response\x12\x35\n\x0bUnsubscribe\x12\x17.mom.UnsubscribeRequest\x1a\r.mom.Response\x12\x31\n\nListTopics\x12\n.mom.Empty\x1a\x17.mom.ListTopicsResponse\x12?\n\x0cPullMessages\x12\x18.mom.PullMessagesRequest\x1a\x15.mom.MessagesResponse\x12\x35\n\x0b\x44\x65leteTopic\x12\x17.mom.DeleteTopicRequest\x1a\r.mom.Response2\xed\x01\n\x0cQueueService\x12\x35\n\x0b\x43reateQueue\x12\x17.mom.CreateQueueRequest\x1a\r.mom.Response\x12\x31\n\nListQueues\x12\n.mom.Empty\x1a\x17.mom.ListQueuesResponse\x12\x35\n\x0bPushMessage\x12\x17.mom.PushMessageRequest\x1a\r.mom.Response\x12<\n\x0bPullMessage\x12\x17.mom.PullMessageRequest\x1a\x14.mom.MessageResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mom_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_RESPONSE']._serialized_start=18
  _globals['_RESPONSE']._serialized_end=62
  _globals['_EMPTY']._serialized_start=64
  _globals['_EMPTY']._serialized_end=71
  _globals['_CREATETOPICREQUEST']._serialized_start=73
  _globals['_CREATETOPICREQUEST']._serialized_end=125
  _globals['_PUBLISHMESSAGEREQUEST']._serialized_start=127
  _globals['_PUBLISHMESSAGEREQUEST']._serialized_end=201
  _globals['_SUBSCRIBEREQUEST']._serialized_start=203
  _globals['_SUBSCRIBEREQUEST']._serialized_end=262
  _globals['_UNSUBSCRIBEREQUEST']._serialized_start=264
  _globals['_UNSUBSCRIBEREQUEST']._serialized_end=325
  _globals['_TOPIC']._serialized_start=327
  _globals['_TOPIC']._serialized_end=367
  _globals['_QUEUE']._serialized_start=369
  _globals['_QUEUE']._serialized_end=409
  _globals['_LISTTOPICSRESPONSE']._serialized_start=411
  _globals['_LISTTOPICSRESPONSE']._serialized_end=459
  _globals['_PULLMESSAGESREQUEST']._serialized_start=461
  _globals['_PULLMESSAGESREQUEST']._serialized_end=523
  _globals['_MESSAGESRESPONSE']._serialized_start=525
  _globals['_MESSAGESRESPONSE']._serialized_end=605
  _globals['_CREATEQUEUEREQUEST']._serialized_start=607
  _globals['_CREATEQUEUEREQUEST']._serialized_end=659
  _globals['_LISTQUEUESRESPONSE']._serialized_start=661
  _globals['_LISTQUEUESRESPONSE']._serialized_end=709
  _globals['_GROUP']._serialized_start=711
  _globals['_GROUP']._serialized_end=734
  _globals['_PUSHMESSAGEREQUEST']._serialized_start=736
  _globals['_PUSHMESSAGEREQUEST']._serialized_end=807
  _globals['_PULLMESSAGEREQUEST']._serialized_start=809
  _globals['_PULLMESSAGEREQUEST']._serialized_end=847
  _globals['_MESSAGERESPONSE']._serialized_start=849
  _globals['_MESSAGERESPONSE']._serialized_end=928
  _globals['_MESSAGE']._serialized_start=930
  _globals['_MESSAGE']._serialized_end=1027
  _globals['_DELETETOPICREQUEST']._serialized_start=1029
  _globals['_DELETETOPICREQUEST']._serialized_end=1081
  _globals['_TOPICSERVICE']._serialized_start=1084
  _globals['_TOPICSERVICE']._serialized_end=1491
  _globals['_QUEUESERVICE']._serialized_start=1494
  _globals['_QUEUESERVICE']._serialized_end=1731
# @@protoc_insertion_point(module_scope)
