@{
header_guard = naming_convention.header_guard(database_name, 'unpack')
namespace = naming_convention.namespace()
unpack_decl_name = naming_convention.unpack_decl()

message_template_name = 'MsgT'
length_name = naming_convention.length(message_template_name)
}@
#ifndef @(header_guard)
#define @(header_guard)

#include <cstddef>
#include <cstdint>

#include <array>
#include <span>
#include <type_traits>
#include <vector>

@TEMPLATE('einval.h.em')

@[for message in messages]@
#include <@(package_name)/@(naming_convention.message_unpack_header_path(message.name))>
@[end for]@

namespace @(package_name)::@(namespace) {

    template<typename @(message_template_name), const std::size_t N>
    int @(unpack_decl_name)(
            const std::array<std::uint8_t, N> &src,
            @(message_template_name) &dst,
            std::enable_if_t<(N >= @(length_name)), int> = 0
    ) noexcept {
        return @(unpack_decl_name)<N>(src.data(), dst);
    }

    template<typename @(message_template_name), typename AllocatorT>
    int @(unpack_decl_name)(
            const std::vector<std::uint8_t, AllocatorT> &src,
            @(message_template_name) &dst
    ) {
        return @(unpack_decl_name)<@(length_name)>(src.data(), dst);
    }

#if __cplusplus >= 202002L
    template<typename @(message_template_name)>
    int @(unpack_decl_name)(
            const std::span<std::uint8_t, @(length_name)> src,
            @(message_template_name) &dst
    ) noexcept {
        return @(unpack_decl_name)<@(length_name)>(src.data(), dst);
    }
#endif // __cplusplus >= 202002L

}  // namespace @(package_name)::@(namespace)

#endif  // @(header_guard)
