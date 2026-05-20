cmake_minimum_required(VERSION 3.8)
project(rosidl_candb_cmake NONE)

find_package(ament_cmake REQUIRED)

ament_package(CONFIG_EXTRAS "rosidl_candb_cmake-extras.cmake")

install(
        DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/cmake"
        DESTINATION "share/${PROJECT_NAME}"
)
