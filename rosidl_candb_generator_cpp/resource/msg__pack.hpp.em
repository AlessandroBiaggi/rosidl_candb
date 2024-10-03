@{
from rosidl_candb_pycommon import to_snake_case

header_guard = naming_convention.header_guard(database_name, 'detail', message.name, 'pack')

namespace = naming_convention.namespace()
struct_name = naming_convention.struct(message.name)
length_name = naming_convention.length(struct_name)
pack_decl_name = naming_convention.pack_decl()
}@
#ifndef @(header_guard)
#define @(header_guard)

#include <@(package_name)/@(naming_convention.struct_header_path(message.name))>
#include <@(package_name)/@(naming_convention.base_header_path())>
#include <@(package_name)/rosidl_candb_generator_cpp__visibility_control.hpp>

namespace @(package_name)::@(namespace) {

    template<const std::size_t N, typename AllocatorT>
    @(naming_convention.visibility_control_public())
    int @(pack_decl_name)(
            const @(struct_name)_<AllocatorT> &src,
            std::uint8_t dst[N],
            std::enable_if_t<(N >= @(length_name)), int> = 0
    ) noexcept {
        struct @(naming_convention.base_struct(message.name)) pkt{};

@[if message.signals]@
@[  for signal in message.signals]@
@{      base_field_name = naming_convention.base_field(message.name, signal.name) }@
@{      field_name = naming_convention.field(message.name, signal.name) }@
@{      scale = naming_convention.scale(struct_name, signal.name) }@
@{      offset = naming_convention.offset(struct_name, signal.name) }@
        pkt.@(base_field_name) = (src.@(field_name) - @(offset)) / @(scale);
@[  end for]@

@[end if]@
        return @(naming_convention.base_pack(message.name))(dst, &pkt, @(length_name));
    }

    template<typename AllocatorT>
    @(naming_convention.visibility_control_public())
    int @(pack_decl_name)(
            const @(struct_name)_<AllocatorT> &src,
            std::uint8_t dst[],
            std::size_t size
    ) noexcept {
        if (size < @(length_name)) {
            return -EINVAL;
        }
        return @(pack_decl_name)<@(length_name)>(src, dst);
    }

} // namespace @(package_name)::@(namespace)

#endif  // @(header_guard)
