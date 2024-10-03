@{
header_guard = naming_convention.header_guard(message.name)
struct_name = naming_convention.struct(message.name)

length_name = naming_convention.length(message.name)

pack_name = naming_convention.pack(message.name)
unpack_name = naming_convention.unpack(message.name)
}@
#ifndef @(header_guard)
#define @(header_guard)

#ifdef __cplusplus
extern "C" {
#endif

#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>

#include <@(package_name)/@(naming_convention.struct_header_path(message.name))>
#include <@(package_name)/@(naming_convention.visibility_control_header())>

@(naming_convention.visibility_control_public())
int @(pack_name)(
        const struct @(struct_name) [static 1],
        uint8_t [static @(length_name)]
);

@(naming_convention.visibility_control_public())
int @(unpack_name)(
        const uint8_t [static @(length_name)],
        struct @(struct_name) [static 1]
);

#ifdef __cplusplus
}
#endif

#endif // @(header_guard)
