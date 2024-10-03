@{
from rosidl_candb_pycommon import to_snake_case

struct_name = naming_convention.struct(message.name)
length_name = naming_convention.length(message.name)
pack_name = naming_convention.pack(message.name)
}@
#include <assert.h>

#include <@(package_name)/@(naming_convention.header_path(message.name))>
#include <@(package_name)/@(naming_convention.base_header_path())>

int @(pack_name)(
        const struct @(struct_name) src[static 1],
        uint8_t dst[static @(length_name)]
) {
    struct @(naming_convention.base_struct(message.name)) pkt = {0};
    int r = -EINVAL;

@[if message.signals]@
@[  for signal in message.signals]@
@{      base_field_name = naming_convention.base_field(message.name, signal.name) }@
@{      field_name = naming_convention.field(message.name, signal.name) }@
@{      scale = naming_convention.scale(struct_name, signal.name) }@
@{      offset = naming_convention.offset(struct_name, signal.name) }@
    pkt.@(base_field_name) = (src->@(field_name) / @(scale)) - @(offset);
@[  end for]@

@[end if]@
    r = @(naming_convention.base_pack(message.name))(dst, &pkt, @(length_name));
    assert(r == @(length_name));

    return r;
}
