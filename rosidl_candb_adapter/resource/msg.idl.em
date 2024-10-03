module @(package_name) {
    module msg {

@TEMPLATE(
    'struct__constants.idl.em',
    message=message,
    struct_name=naming_convention.struct(message.name),
)

@TEMPLATE(
    'struct.idl.em',
    message=message,
)

    };
};
