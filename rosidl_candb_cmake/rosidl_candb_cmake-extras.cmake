find_package(ament_cmake QUIET REQUIRED)
find_package(rosidl_cmake QUIET REQUIRED)
find_package(rosidl_candb_adapter QUIET REQUIRED)

find_package(std_msgs QUIET REQUIRED)

include("${rosidl_candb_cmake_DIR}/rosidl_candb_write_generator_arguments.cmake")
include("${rosidl_candb_cmake_DIR}/rosidl_candb_generate_interfaces.cmake")
