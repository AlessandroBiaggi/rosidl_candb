set(_generated_extra_file "${CMAKE_CURRENT_BINARY_DIR}/rosidl_candb_cmake/rosidl_candb_cmake-extras.cmake")
configure_file(
        "${rosidl_candb_cmake_DIR}/rosidl_candb_cmake-extras.cmake.in"
        "${_generated_extra_file}"
        @ONLY
)
list(APPEND ${PROJECT_NAME}_CONFIG_EXTRAS "${_generated_extra_file}")
