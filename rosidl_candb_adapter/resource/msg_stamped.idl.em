#include <std_msgs/msg/Header.idl>
#include <@(package_name)/@(naming_convention.idl_path(message.name))>

module @(package_name) {
    module msg {

@TEMPLATE(
    'struct__constants.idl.em',
    message=message,
    struct_name=naming_convention.stamped_struct(message.name),
)

@TEMPLATE(
    'struct__stamped.idl.em',
    message=message,
)

    };
};
