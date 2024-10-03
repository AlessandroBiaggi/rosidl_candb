macro(rosidl_candb_generator_c_extras BIN GENERATOR_FILES TEMPLATE_DIR)
    find_package(ament_cmake_core QUIET REQUIRED)

    ament_register_extension(
            "rosidl_candb_generate_interfaces"
            "rosidl_candb_generator_c"
            "rosidl_candb_generator_c_generate_interfaces.cmake"
    )

    normalize_path(BIN "${BIN}")
    set(rosidl_candb_generator_c_BIN "${BIN}")

    normalize_path(GENERATOR_FILES "${GENERATOR_FILES}")
    set(rosidl_candb_generator_c_GENERATOR_FILES "${GENERATOR_FILES}")

    normalize_path(TEMPLATE_DIR "${TEMPLATE_DIR}")
    set(rosidl_candb_generator_c_TEMPLATE_DIR "${TEMPLATE_DIR}")
endmacro()
