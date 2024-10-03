@{
struct_name = naming_convention.struct(message.name)
length_name = naming_convention.length(message.name)
unpack_name = naming_convention.unpack(message.name)
}@
#include <assert.h>

#include <@(package_name)/@(naming_convention.header_path(message.name))>
#include <@(package_name)/@(naming_convention.base_header_path())>

int @(unpack_name)(
        const uint8_t src[static @(length_name)],
        struct @(struct_name) dst[static 1]
) {
    struct @(naming_convention.base_struct(message.name)) pkt = {0};
    int r = -EINVAL;

    r = @(naming_convention.base_unpack(message.name))(&pkt, src, @(length_name));
    assert(r == @(length_name));

@[if message.signals]@
@[  for signal in message.signals]@
@{      base_field_name = naming_convention.base_field(struct_name, signal.name) }@
@{      field_name = naming_convention.field(struct_name, signal.name) }@
@{      scale = naming_convention.scale(struct_name, signal.name) }@
@{      offset = naming_convention.offset(struct_name, signal.name) }@
    dst->@(field_name) = @(scale) * pkt.@(base_field_name) + @(offset);
@[  end for]@

@[end if]@
    return r;
}
