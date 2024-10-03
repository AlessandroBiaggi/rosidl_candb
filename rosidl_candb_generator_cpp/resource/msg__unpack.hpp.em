@{
from rosidl_candb_pycommon import to_snake_case

header_guard = naming_convention.header_guard(database_name, 'detail', message.name, 'unpack')

namespace = naming_convention.namespace()
struct_name = naming_convention.struct(message.name)
length_name = naming_convention.length(struct_name)
unpack_decl_name = naming_convention.unpack_decl()
}@
#ifndef @(header_guard)
#define @(header_guard)

#include <@(package_name)/@(naming_convention.struct_header_path(message.name))>
#include <@(package_name)/@(naming_convention.base_header_path())>
#include <@(package_name)/rosidl_candb_generator_cpp__visibility_control.hpp>

namespace @(package_name)::@(namespace) {

    template<const std::size_t N, typename AllocatorT>
    @(naming_convention.visibility_control_public())
    int @(unpack_decl_name)(
            const std::uint8_t src[N],
            @(struct_name)_<AllocatorT> &dst,
            std::enable_if_t<(N >= @(length_name)), int> = 0
    ) noexcept {
        struct @(naming_convention.base_struct(message.name)) pkt{};
        int r = -EINVAL;

        r = @(naming_convention.base_unpack(message.name))(&pkt, src, @(length_name));
@[if message.signals]@
        if (r >= 0) {
@[  for signal in message.signals]@
@{      base_field_name = naming_convention.base_field(message.name, signal.name) }@
@{      field_name = naming_convention.field(message.name, signal.name) }@
@{      scale = naming_convention.scale(struct_name, signal.name) }@
@{      offset = naming_convention.offset(struct_name, signal.name) }@
            dst.@(field_name) = @(scale) * pkt.@(base_field_name) + @(offset);
@[  end for]@
        }

@[end if]@
        return r;
    }

    template<typename AllocatorT>
    @(naming_convention.visibility_control_public())
    int @(unpack_decl_name)(
            const std::uint8_t src[],
            const std::size_t length,
            @(struct_name)_<AllocatorT> &dst
    ) noexcept {
        if (length < @(length_name)) {
            return -EINVAL;
        }
        return @(unpack_decl_name)<@(length_name)>(src, dst);
    }

} // namespace @(package_name)::@(namespace)

#endif  // @(header_guard)
