cmake_minimum_required(VERSION 3.8)
project(rosidl_candb_adapter NONE)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

ament_python_install_package("${PROJECT_NAME}")

if(BUILD_TESTING)
  find_package(ament_cmake_pytest REQUIRED)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
  ament_add_pytest_test(pytest test)
endif()

ament_package(
        CONFIG_EXTRAS "rosidl_candb_adapter-extras.cmake.in"
)

install(
        DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/cmake" "${CMAKE_CURRENT_SOURCE_DIR}/resource"
        DESTINATION "share/${PROJECT_NAME}"
)

install(
        PROGRAMS "${CMAKE_CURRENT_SOURCE_DIR}/bin/${PROJECT_NAME}"
        DESTINATION "lib/${PROJECT_NAME}"
)
