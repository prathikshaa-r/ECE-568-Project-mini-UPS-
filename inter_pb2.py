# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: inter.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='inter.proto',
  package='',
  serialized_pb=_b('\n\x0binter.proto\":\n\x07Product\x12\n\n\x02id\x18\x01 \x02(\x05\x12\x13\n\x0b\x64\x65scription\x18\x02 \x02(\t\x12\x0e\n\x06\x61mount\x18\x03 \x02(\x05\"{\n\x05Order\x12\x0c\n\x04whid\x18\x01 \x02(\x05\x12\t\n\x01x\x18\x02 \x02(\x05\x12\t\n\x01y\x18\x03 \x02(\x05\x12\x11\n\tpackageid\x18\x04 \x02(\x03\x12\x13\n\x0bupsusername\x18\x05 \x02(\t\x12\x16\n\x04item\x18\x06 \x03(\x0b\x32\x08.Product\x12\x0e\n\x06seqnum\x18\x07 \x02(\x03\",\n\x07\x44\x65liver\x12\x11\n\tpackageid\x18\x01 \x02(\x03\x12\x0e\n\x06seqnum\x18\x03 \x02(\x03\">\n\nAWarehouse\x12\n\n\x02id\x18\x01 \x02(\x05\x12\t\n\x01x\x18\x02 \x02(\x05\x12\t\n\x01y\x18\x03 \x02(\x05\x12\x0e\n\x06seqnum\x18\x04 \x02(\x03\"k\n\nAUCommands\x12\x15\n\x05order\x18\x01 \x03(\x0b\x32\x06.Order\x12\x1b\n\ttodeliver\x18\x02 \x03(\x0b\x32\x08.Deliver\x12\x1b\n\x06whinfo\x18\x03 \x03(\x0b\x32\x0b.AWarehouse\x12\x0c\n\x04\x61\x63ks\x18\x04 \x03(\x03\"I\n\x05Truck\x12\x0c\n\x04whid\x18\x01 \x02(\x05\x12\x0f\n\x07truckid\x18\x02 \x02(\x05\x12\x11\n\tpackageid\x18\x03 \x02(\x03\x12\x0e\n\x06seqnum\x18\x04 \x02(\x03\".\n\tDelivered\x12\x11\n\tpackageid\x18\x01 \x02(\x03\x12\x0e\n\x06seqnum\x18\x02 \x02(\x03\"O\n\nUACommands\x12\x17\n\x07\x61rrived\x18\x01 \x03(\x0b\x32\x06.Truck\x12\x1a\n\x06\x66inish\x18\x02 \x03(\x0b\x32\n.Delivered\x12\x0c\n\x04\x61\x63ks\x18\x03 \x03(\x03')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_PRODUCT = _descriptor.Descriptor(
  name='Product',
  full_name='Product',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='Product.id', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='description', full_name='Product.description', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='amount', full_name='Product.amount', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=15,
  serialized_end=73,
)


_ORDER = _descriptor.Descriptor(
  name='Order',
  full_name='Order',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='whid', full_name='Order.whid', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='x', full_name='Order.x', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='y', full_name='Order.y', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='packageid', full_name='Order.packageid', index=3,
      number=4, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='upsusername', full_name='Order.upsusername', index=4,
      number=5, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='item', full_name='Order.item', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seqnum', full_name='Order.seqnum', index=6,
      number=7, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=75,
  serialized_end=198,
)


_DELIVER = _descriptor.Descriptor(
  name='Deliver',
  full_name='Deliver',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='packageid', full_name='Deliver.packageid', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seqnum', full_name='Deliver.seqnum', index=1,
      number=3, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=200,
  serialized_end=244,
)


_AWAREHOUSE = _descriptor.Descriptor(
  name='AWarehouse',
  full_name='AWarehouse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='AWarehouse.id', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='x', full_name='AWarehouse.x', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='y', full_name='AWarehouse.y', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seqnum', full_name='AWarehouse.seqnum', index=3,
      number=4, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=246,
  serialized_end=308,
)


_AUCOMMANDS = _descriptor.Descriptor(
  name='AUCommands',
  full_name='AUCommands',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='order', full_name='AUCommands.order', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='todeliver', full_name='AUCommands.todeliver', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='whinfo', full_name='AUCommands.whinfo', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='acks', full_name='AUCommands.acks', index=3,
      number=4, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=310,
  serialized_end=417,
)


_TRUCK = _descriptor.Descriptor(
  name='Truck',
  full_name='Truck',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='whid', full_name='Truck.whid', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='truckid', full_name='Truck.truckid', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='packageid', full_name='Truck.packageid', index=2,
      number=3, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seqnum', full_name='Truck.seqnum', index=3,
      number=4, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=419,
  serialized_end=492,
)


_DELIVERED = _descriptor.Descriptor(
  name='Delivered',
  full_name='Delivered',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='packageid', full_name='Delivered.packageid', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seqnum', full_name='Delivered.seqnum', index=1,
      number=2, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=494,
  serialized_end=540,
)


_UACOMMANDS = _descriptor.Descriptor(
  name='UACommands',
  full_name='UACommands',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='arrived', full_name='UACommands.arrived', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='finish', full_name='UACommands.finish', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='acks', full_name='UACommands.acks', index=2,
      number=3, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=542,
  serialized_end=621,
)

_ORDER.fields_by_name['item'].message_type = _PRODUCT
_AUCOMMANDS.fields_by_name['order'].message_type = _ORDER
_AUCOMMANDS.fields_by_name['todeliver'].message_type = _DELIVER
_AUCOMMANDS.fields_by_name['whinfo'].message_type = _AWAREHOUSE
_UACOMMANDS.fields_by_name['arrived'].message_type = _TRUCK
_UACOMMANDS.fields_by_name['finish'].message_type = _DELIVERED
DESCRIPTOR.message_types_by_name['Product'] = _PRODUCT
DESCRIPTOR.message_types_by_name['Order'] = _ORDER
DESCRIPTOR.message_types_by_name['Deliver'] = _DELIVER
DESCRIPTOR.message_types_by_name['AWarehouse'] = _AWAREHOUSE
DESCRIPTOR.message_types_by_name['AUCommands'] = _AUCOMMANDS
DESCRIPTOR.message_types_by_name['Truck'] = _TRUCK
DESCRIPTOR.message_types_by_name['Delivered'] = _DELIVERED
DESCRIPTOR.message_types_by_name['UACommands'] = _UACOMMANDS

Product = _reflection.GeneratedProtocolMessageType('Product', (_message.Message,), dict(
  DESCRIPTOR = _PRODUCT,
  __module__ = 'inter_pb2'
  # @@protoc_insertion_point(class_scope:Product)
  ))
_sym_db.RegisterMessage(Product)

Order = _reflection.GeneratedProtocolMessageType('Order', (_message.Message,), dict(
  DESCRIPTOR = _ORDER,
  __module__ = 'inter_pb2'
  # @@protoc_insertion_point(class_scope:Order)
  ))
_sym_db.RegisterMessage(Order)

Deliver = _reflection.GeneratedProtocolMessageType('Deliver', (_message.Message,), dict(
  DESCRIPTOR = _DELIVER,
  __module__ = 'inter_pb2'
  # @@protoc_insertion_point(class_scope:Deliver)
  ))
_sym_db.RegisterMessage(Deliver)

AWarehouse = _reflection.GeneratedProtocolMessageType('AWarehouse', (_message.Message,), dict(
  DESCRIPTOR = _AWAREHOUSE,
  __module__ = 'inter_pb2'
  # @@protoc_insertion_point(class_scope:AWarehouse)
  ))
_sym_db.RegisterMessage(AWarehouse)

AUCommands = _reflection.GeneratedProtocolMessageType('AUCommands', (_message.Message,), dict(
  DESCRIPTOR = _AUCOMMANDS,
  __module__ = 'inter_pb2'
  # @@protoc_insertion_point(class_scope:AUCommands)
  ))
_sym_db.RegisterMessage(AUCommands)

Truck = _reflection.GeneratedProtocolMessageType('Truck', (_message.Message,), dict(
  DESCRIPTOR = _TRUCK,
  __module__ = 'inter_pb2'
  # @@protoc_insertion_point(class_scope:Truck)
  ))
_sym_db.RegisterMessage(Truck)

Delivered = _reflection.GeneratedProtocolMessageType('Delivered', (_message.Message,), dict(
  DESCRIPTOR = _DELIVERED,
  __module__ = 'inter_pb2'
  # @@protoc_insertion_point(class_scope:Delivered)
  ))
_sym_db.RegisterMessage(Delivered)

UACommands = _reflection.GeneratedProtocolMessageType('UACommands', (_message.Message,), dict(
  DESCRIPTOR = _UACOMMANDS,
  __module__ = 'inter_pb2'
  # @@protoc_insertion_point(class_scope:UACommands)
  ))
_sym_db.RegisterMessage(UACommands)


# @@protoc_insertion_point(module_scope)
