macro(rosidl_candb_generator_base_extras BIN GENERATOR_FILES TEMPLATE_DIR)
    find_package(ament_cmake_core QUIET REQUIRED)

    ament_register_extension(
            "rosidl_candb_generate_interfaces"
            "rosidl_candb_generator_base"
            "rosidl_candb_generator_base_generate_interfaces.cmake"
    )

    normalize_path(BIN "${BIN}")
    set(rosidl_candb_generator_base_BIN "${BIN}")

    normalize_path(GENERATOR_FILES "${GENERATOR_FILES}")
    set(rosidl_candb_generator_base_GENERATOR_FILES "${GENERATOR_FILES}")

    normalize_path(TEMPLATE_DIR "${TEMPLATE_DIR}")
    set(rosidl_candb_generator_base_TEMPLATE_DIR "${TEMPLATE_DIR}")
endmacro()
