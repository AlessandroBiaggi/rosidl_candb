#
# Generate code for ROS IDL files using all available generators.
#
# Execute the extension point ``rosidl_generate_interfaces``.
#
# :param target: the _name of the generation target,
#   specific generators might use the _name as a prefix for their own
#   generation step
# :type target: string
# :param ARGN: the interface file containing message, service, and action
#   definitions where each value might be either a path relative to the
#   CMAKE_CURRENT_SOURCE_DIR or a tuple separated by a colon with an absolute
#   base path and a path relative to that base path.
#   If the interface file's parent directory is 'action', it is assumed to be
#   an action definition.
#   If an action interface is passed then you must add a depend tag for
#   'action_msgs' to your package.xml, otherwise this macro will error.
#   For backward compatibility if an interface file doesn't end in ``.idl`` it
#   is being passed to ``rosidl_candb_adapter`` to be transformed into
#   an ``.idl`` file.
# :type ARGN: list of strings
# :param LIBRARY_NAME: the base name of the library, specific generators might
#   append their own suffix
# :type LIBRARY_NAME: string
# :param SKIP_INSTALL: if set skip installing the interface files
# :type SKIP_INSTALL: option
# :param SKIP_GROUP_MEMBERSHIP_CHECK: if set, skip enforcing membership in the
#   rosidl_interface_packages group
# :type SKIP_GROUP_MEMBERSHIP_CHECK: option
# :param ADD_LINTER_TESTS: if set lint the interface files using
#   the ``ament_lint`` package
# :type ADD_LINTER_TESTS: option
#
# @public
#
macro(rosidl_candb_generate_interfaces target)
    cmake_parse_arguments(
            _ARG
            "ADD_LINTER_TESTS;SKIP_INSTALL;SKIP_GROUP_MEMBERSHIP_CHECK;STRICT"
            "LIBRARY_NAME" "NODE_TUPLES;MESSAGE_TUPLES"
            ${ARGN}
    )

    set(_output_dir "${CMAKE_CURRENT_BINARY_DIR}/rosidl_candb_adapter")
    set(_dependencies "std_msgs")

    foreach (_dep ${_dependencies})
        find_package("${_dep}" QUIET)

        if (NOT ${_dep}_FOUND)
            message(FATAL_ERROR "Could not find dependency: '${_dep}'")
        endif ()
    endforeach ()

    if (NOT _ARG_UNPARSED_ARGUMENTS)
        message(FATAL_ERROR
                "rosidl_candb_generate_interfaces() called without any "
                "interface files"
        )
    endif ()

    if (_${PROJECT_NAME}_AMENT_PACKAGE)
        message(FATAL_ERROR
                "rosidl_candb_generate_interfaces() must be called before "
                "ament_package()"
        )
    endif ()

    if (NOT _ARG_SKIP_INSTALL)
        ament_export_dependencies("${_dependencies}")
    endif ()

    list(LENGTH _ARG_UNPARSED_ARGUMENTS _interfaces_length)

    set(_interface_tuples "")
    set(_interface_files "")

    foreach (_file ${_ARG_UNPARSED_ARGUMENTS})
        if (IS_ABSOLUTE "${_file}")
            string(FIND "${_file}" ":" _index)

            if (${_index} EQUAL -1)
                message(FATAL_ERROR
                        "rosidl_candb_generate_interfaces() the passed absolute "
                        "file '${_file}' must be represented as an absolute base "
                        "path separated by a colon from the relative path to "
                        "the interface file"
                )
            endif ()

            string(REGEX REPLACE ":([^:]*)$" "/\\1" _abs_file "${_file}")

            if (NOT EXISTS "${_abs_file}")
                message(FATAL_ERROR
                        "rosidl_candb_generate_interfaces() the passed file "
                        "'${_abs_file}' doesn't exist"
                )
            endif ()

            list(APPEND _interface_tuples "${_file}")
            list(APPEND _interface_files "${_abs_file}")
        else ()
            set(_abs_file "${CMAKE_CURRENT_SOURCE_DIR}/${_file}")

            if (NOT EXISTS "${_abs_file}")
                message(FATAL_ERROR
                        "rosidl_candb_generate_interfaces() the passed file "
                        "'${_abs_file}' doesn't exist relative to the "
                        "CMAKE_CURRENT_SOURCE_DIR '${CMAKE_CURRENT_SOURCE_DIR}'"
                )
            endif ()

            list(APPEND _interface_tuples "${CMAKE_CURRENT_SOURCE_DIR}:${_file}")
            list(APPEND _interface_files "${_abs_file}")
        endif ()
    endforeach ()


    set(_node_tuples "")
    set(_message_tuples "")

    foreach (_node_tuple ${_ARG_NODE_TUPLES})
        set(_node_interface_tuple "")

        string(REPLACE ":" ";" _node_tuple_parts "${_node_tuple}")
        list(LENGTH _node_tuple_parts _length)

        if (IS_ABSOLUTE "${_node_tuple}")
            if (NOT _node_tuple_parts EQUAL 3)
                message(FATAL_ERROR
                        "rosidl_candb_generate_interfaces() the passed node "
                        "tuple '${_node_tuple}' must be represented as an absolute "
                        "base path separated by a colon from the relative path to "
                        "a passed interface file and the node name"
                )
            endif ()

            list(GET _node_tuple_parts 0 _base_path)
            list(GET _node_tuple_parts 1 _interface_file)

            set(_node_interface_tuple "${_base_path}:${_interface_file}")
        elseif (_length EQUAL 2)
            list(GET _node_tuple_parts 0 _interface_file)

            set(_node_interface_tuple "${CMAKE_CURRENT_SOURCE_DIR}:${_interface_file}")
        else ()
            if (_interfaces_length GREATER 1)
                message(FATAL_ERROR
                        "rosidl_candb_generate_interfaces() the passed node "
                        "tuple '${_node_tuple}' must be represented as a "
                        "relative path to a passed interface file and "
                        "the node name"
                )
            endif ()

            list(GET _interface_tuples 0 _interface_tuple)
            set(_node_interface_tuple "${_interface_tuple}")
        endif ()

        list(FIND _interface_tuples "${_node_interface_tuple}" _index)

        if (_index EQUAL -1)
            message(FATAL_ERROR
                    "rosidl_candb_generate_interfaces() the interface file "
                    "for tuple '${_node_tuple}' must be passed as an interface "
                    "file"
            )
        endif ()

        list(GET _node_tuple_parts -1 _node_name)
        list(APPEND _node_tuples "${_node_interface_tuple}:${_node_name}")
    endforeach ()

    foreach (_message_tuple ${_ARG_MESSAGE_TUPLES})
        set(_message_interface_tuple "")

        string(REPLACE ":" ";" _message_tuple_parts "${_message_tuple}")
        list(LENGTH _message_tuple_parts _length)

        if (IS_ABSOLUTE "${_message_tuple}")
            if (NOT _length EQUAL 2)
                message(FATAL_ERROR
                        "rosidl_candb_generate_interfaces() the passed message "
                        "tuple '${_message_tuple}' must be represented as an absolute "
                        "base path separated by a colon from the relative path to "
                        "a passed interface file and the message name"
                )
            endif ()

            list(GET _message_tuple_parts 0 _base_path)
            list(GET _message_tuple_parts 1 _interface_file)

            set(_message_interface_tuple "${_base_path}:${_interface_file}")
        elseif (_length EQUAL 2)
            list(GET _message_tuple_parts 0 _interface_file)
            set(_message_interface_tuple "${CMAKE_CURRENT_SOURCE_DIR}:${_interface_file}")
        else ()
            if (NOT _interfaces_length EQUAL 1)
                message(FATAL_ERROR
                        "rosidl_candb_generate_interfaces() the passed message "
                        "tuple '${_message_tuple}' must be represented as a base "
                        "path separated by a colon from the relative path to "
                        "a passed interface file"
                )
            endif ()

            list(GET _interface_tuples 0 _interface_tuple)
            set(_message_interface_tuple "${_interface_tuple}")
        endif ()

        list(FIND _interface_tuples "${_message_interface_tuple}" _index)

        if (_index EQUAL -1)
            message(FATAL_ERROR
                    "rosidl_candb_generate_interfaces() the interface file "
                    "for tuple '${_message_tuple}' must be passed as an interface "
                    "file"
            )
        endif ()

        list(GET _message_tuple_parts -1 _message_name)
        list(APPEND _message_tuples "${_message_interface_tuple}:${_message_name}")
    endforeach ()

    foreach (_tuple ${_interface_tuples})
        string(REGEX REPLACE ":([^:]*)$" "/\\1" _abs_interface "${_tuple}")
        stamp("${_abs_interface}")
    endforeach ()

    set(_adapter_arguments_file "${CMAKE_CURRENT_BINARY_DIR}/rosidl_candb_adapter__arguments__${target}.json")

    set(_strict "")
    if (_ARG_STRICT)
        set(_strict "STRICT")
    endif ()

    rosidl_candb_write_generator_arguments(
            "${_adapter_arguments_file}"
            PACKAGE_NAME "${PROJECT_NAME}"
            INTERFACE_TUPLES "${_interface_tuples}"
            NODE_TUPLES ${_node_tuples}
            MESSAGE_TUPLES ${_message_tuples}
            TEMPLATE_DIR "${rosidl_candb_adapter_TEMPLATE_DIR}"
            OUTPUT_DIR "${_output_dir}"
            "${_strict}"
    )

    rosidl_candb_adapt_interfaces(
            _idl_tuples
            _pkt_tuples
            _sig_tuples
            "${_adapter_arguments_file}"
            TARGET "${target}"
    )

    set(_target_dependencies
            "${rosidl_candb_adapter_TEMPLATE_DIR}/msg.idl.em"
            "${rosidl_candb_adapter_TEMPLATE_DIR}/struct.idl.em"
    )

    foreach (_dep ${_dependencies})
        foreach (_idl_file ${${_dep}_IDL_FILES})
            set(_abs_idl_file "${${_dep}_DIR}/../${_idl_file}")
            normalize_path(_abs_idl_file "${_abs_idl_file}")
            list(APPEND _dep_files "${_abs_idl_file}")
        endforeach ()
    endforeach ()

    add_custom_target(
            "${target}" ALL
            DEPENDS ${_interface_files} ${_target_dependencies}
            SOURCES ${_interface_files}
    )

    if (NOT _ARG_SKIP_INSTALL)
        if (NOT _ARG_SKIP_GROUP_MEMBERSHIP_CHECK)
            set(_group_name "rosidl_candb_interface_packages")

            if (NOT _AMENT_PACKAGE_NAME)
                ament_package_xml()
            endif ()

            if (NOT _group_name IN_LIST ${_AMENT_PACKAGE_NAME}_MEMBER_OF_GROUPS)
                message(FATAL_ERROR
                        "Packages installing interfaces must include "
                        "'<member_of_group>${_group_name}</member_of_group>' "
                        "in their package.xml"
                )
            endif ()
        endif ()

        set(_idl_file_lines "")
        set(_pkt_file_lines "")
        set(_sig_file_lines "")

        foreach (_idl_tuple ${_idl_tuples})
            string(REGEX REPLACE ":([^:]*)$" ";\\1" _idl_list "${_idl_tuple}")

            list(GET _idl_list 1 _idl_relpath)
            file(TO_CMAKE_PATH "${_idl_relpath}" _idl_relpath)

            list(APPEND _idl_file_lines "${_idl_relpath}")
        endforeach ()

        foreach (_pkt_tuple ${_pkt_tuples})
            string(REGEX REPLACE ":" ";" _pkt_list "${_pkt_tuple}")

            list(GET _pkt_list 0 _db_relpath)
            file(TO_CMAKE_PATH "${_db_relpath}" _db_relpath)

            list(GET _pkt_list 1 _pkt_message)
            file(TO_CMAKE_PATH "${_pkt_message}" _pkt_message)

            list(GET _pkt_list 2 _pkt_relpath)
            file(TO_CMAKE_PATH "${_pkt_relpath}" _pkt_relpath)

            list(GET _pkt_list 3 _spkt_relpath)
            file(TO_CMAKE_PATH "${_spkt_relpath}" _spkt_relpath)

            list(APPEND _pkt_file_lines "${_db_relpath}:${_pkt_message}:${_pkt_relpath}:${_spkt_relpath}")
        endforeach ()

        foreach (_sig_tuple ${_sig_tuples})
            string(REGEX REPLACE ":" ";" _sig_list "${_sig_tuple}")

            list(GET _sig_list 0 _db_relpath)
            file(TO_CMAKE_PATH "${_db_relpath}" _db_relpath)

            list(GET _sig_list 1 _sig_message)
            file(TO_CMAKE_PATH "${_sig_message}" _sig_message)

            list(GET _sig_list 2 _sig_name)
            file(TO_CMAKE_PATH "${_sig_name}" _sig_name)

            list(GET _sig_list 3 _sig_idl_relpath)
            file(TO_CMAKE_PATH "${_sig_idl_relpath}" _sig_idl_relpath)

            list(GET _sig_list 4 _sig_idl_field)
            file(TO_CMAKE_PATH "${_sig_idl_field}" _sig_idl_field)

            list(APPEND _sig_file_lines "${_db_relpath}:${_sig_message}:${_sig_name}:${_sig_idl_relpath}:${_sig_idl_field}")
        endforeach ()

        foreach (_non_idl_file ${_non_idl_files})
            get_filename_component(_interface_ns "${_non_idl_file}" DIRECTORY)
            get_filename_component(_interface_ns "${_interface_ns}" NAME)
            get_filename_component(_interface_name "${_non_idl_file}" NAME)

            list(APPEND _idl_files_lines "${_interface_ns}/${_interface_name}")
        endforeach ()

        list(SORT _idl_files_lines)
        string(REPLACE ";" "\n" _idl_files_lines "${_idl_files_lines}")

        ament_index_register_resource("rosidl_candb_interfaces" CONTENT "${_idl_files_lines}")
        ament_index_register_resource("rosidl_candb_packets" CONTENT "${_pkt_file_lines}")
        ament_index_register_resource("rosidl_candb_signals" CONTENT "${_sig_file_lines}")
    endif ()

    set(_recursive_dependencies "")

    foreach (_dep ${_dependencies})
        find_package("${_dep}" REQUIRED QUIET)

        if (DEFINED ${_dep}_IDL_FILES)
            list_append_unique(_recursive_dependencies "${_dep}")
        endif ()

        foreach (_dep2 ${${_dep}_RECURSIVE_DEPENDENCIES})
            if (DEFINED ${_dep2}_IDL_FILES)
                list_append_unique(_recursive_dependencies "${_dep2}")
            endif ()
        endforeach ()
    endforeach ()

    set(rosidl_generate_interfaces_TARGET "${target}")
    set(rosidl_generate_interfaces_DEPENDENCY_PACKAGE_NAMES ${_recursive_dependencies})
    set(rosidl_generate_interfaces_LIBRARY_NAME ${_ARG_LIBRARY_NAME})
    set(rosidl_generate_interfaces_SKIP_INSTALL ${_ARG_SKIP_INSTALL})
    set(rosidl_generate_interfaces_ADD_LINTER_TESTS ${_ARG_ADD_LINTER_TESTS})

    set(rosidl_generate_interfaces_IDL_TUPLES ${_idl_tuples})
    unset(rosidl_generate_interfaces_IDL_FILES)
    set(rosidl_generate_interfaces_ABS_IDL_FILES)

    set(rosidl_candb_generate_interfaces_INTERFACE_TUPLES ${_interface_tuples})
    set(rosidl_candb_generate_interfaces_NODE_TUPLES ${_node_tuples})
    set(rosidl_candb_generate_interfaces_MESSAGE_TUPLES ${_message_tuples})
    set(rosidl_candb_generate_interfaces_STRICT ${_ARG_STRICT})

    foreach (_idl_tuple ${rosidl_generate_interfaces_IDL_TUPLES})
        string(REGEX REPLACE ":([^:]*)$" "/\\1" _abs_idl_file "${_idl_tuple}")
        list(APPEND rosidl_generate_interfaces_ABS_IDL_FILES "${_abs_idl_file}")
    endforeach ()

    set(_rosidl_extension_point "rosidl_generate_idl_interfaces")
    set(_rosidl_obsolete_extension_point "rosidl_generate_interfaces")
    ament_execute_extensions("${_rosidl_extension_point}")

    set(_rosidl_candb_extension_point "rosidl_candb_generate_interfaces")
    ament_execute_extensions("${_rosidl_candb_extension_point}")

    if (AMENT_EXTENSIONS_${_obsolete_extension_point})
        foreach (_extension ${AMENT_EXTENSIONS_${_obsolete_extension_point}})
            string(REPLACE ":" ";" _extension_list "${_extension}")
            list(GET _extension_list 0 _package_name)

            message(WARNING
                    "Package '${_package_name}' registered an extension for the "
                    "obsolete extension point '${_obsolete_extension_point}'. "
                    "It is being skipped and needs to be updated to the new "
                    "extension point '${_extension_point}'."
                    "Please refer to the migration steps on the Dashing release "
                    "page for more details."
            )
        endforeach ()
    endif ()

    if (NOT _ARG_SKIP_INSTALL)
        install(
                FILES
                "${_output_dir}/${target}.idls"
                "${_output_dir}/${target}.pkts"
                "${_output_dir}/${target}.sigs"
                DESTINATION "share/${PROJECT_NAME}"
        )

        foreach (_idl_tuple ${_idl_tuples})
            string(REGEX REPLACE ":([^:]*)$" "/\\1" _idl_file "${_idl_tuple}")

            string(REGEX REPLACE ":([^:]*)$" ";\\1" _idl_parts "${_idl_tuple}")
            list(GET _idl_parts 1 _idl_relpath)
            get_filename_component(_parent_folders "${_idl_relpath}" DIRECTORY)

            install(
                    FILES "${_idl_file}"
                    DESTINATION "share/${PROJECT_NAME}/${_parent_folders}"
            )

            file(TO_CMAKE_PATH "${_idl_relpath}" _idl_relpath)
            list(APPEND _rosidl_candb_cmake_IDL_FILES "${_idl_relpath}")
        endforeach ()

        foreach (_interface_file ${_interface_files})
            get_filename_component(_parent_folder "${_interface_file}" DIRECTORY)
            get_filename_component(_parent_folder "${_parent_folder}" NAME)

            install(
                    FILES "${_interface_file}"
                    DESTINATION "share/${PROJECT_NAME}/${_parent_folder}"
            )

            get_filename_component(_name "${_interface_file}" NAME)
            list(APPEND _rosidl_candb_cmake_INTERFACE_FILES "${_parent_folder}/${_name}")
        endforeach ()
    endif ()
endmacro()
