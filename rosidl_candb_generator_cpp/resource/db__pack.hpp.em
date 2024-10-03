@{
header_guard = naming_convention.header_guard(database_name, 'pack')
namespace = naming_convention.namespace()
pack_decl_name = naming_convention.pack_decl()

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
#include <@(package_name)/@(naming_convention.message_pack_header_path(message.name))>
@[end for]@

namespace @(package_name)::@(namespace) {

    template<typename @(message_template_name), const std::size_t N>
    int @(pack_decl_name)(
            const @(message_template_name) &src,
            std::array<std::uint8_t, N> &dst,
            std::enable_if_t<(N >= @(length_name)), int> = 0
    ) noexcept {
        return @(pack_decl_name)<N>(src, dst.data());
    }

    template<typename @(message_template_name), typename AllocatorT>
    int @(pack_decl_name)(
            const @(message_template_name) &src,
            std::vector<std::uint8_t, AllocatorT> &dst
    ) {
        src.resize(@(length_name));
        return @(pack_decl_name)<@(length_name)>(src, dst.data());
    }

#if __cplusplus >= 202002L
    template<typename @(message_template_name)>
    int @(pack_decl_name)(
            const @(message_template_name) &src,
            std::span<std::uint8_t, @(length_name)> dst
    ) noexcept {
        return @(pack_decl_name)<@(length_name)>(src, dst.data());
    }
#endif // __cplusplus >= 202002L

}  // namespace @(package_name)::@(namespace)

#endif  // @(header_guard)
