#
# Convert non-idl interface files into `.idl` files.
#
# The input files might be a `.arxml`, `.dbc`, `.kcd`, `.sym` or `.cdd` files.
#
# :param msg_tuples_var: the variable name to return the list of generated `.msg`
#   files, each item is a tuple separated by a colon with an absolute base path
#   and a path relative to that base path
# :type msg_tuples_var: string
# :param arguments_file: the path of the arguments file containing the paths of
#   the non-idl files.
# :type arguments_file: string
# :param TARGET: the name of the generation target
# :type TARGET: string
#
# @public
#
function(rosidl_candb_adapt_interfaces msg_tuples_var arguments_file)
    cmake_parse_arguments(ARG "" "TARGET" "" ${ARGN})

    if (ARG_UNPARSED_ARGUMENTS)
        message(FATAL_ERROR "Unknown arguments: ${ARG_UNPARSED_ARGUMENTS}")
    endif ()

    find_package(Python3 QUIET REQUIRED COMPONENTS Interpreter)
    set(msg_output "${CMAKE_CURRENT_BINARY_DIR}/rosidl_candb_adapter/${ARG_TARGET}.msgs")

    execute_process(
            COMMAND
            "${Python3_EXECUTABLE}" -m "rosidl_candb_adapter"
            --package-name "${PROJECT_NAME}"
            --arguments-file "${arguments_file}"
            --output-dir "${CMAKE_CURRENT_BINARY_DIR}/rosidl_candb_adapter/${PROJECT_NAME}"
            --msg-output-file "${msg_output}"
            OUTPUT_QUIET
            ERROR_VARIABLE error
            RESULT_VARIABLE result
    )

    if (NOT result EQUAL 0)
        message(FATAL_ERROR "Generate process return code ${result}:\n${error}")
    endif ()

    file(STRINGS "${msg_output}" msg_tuples)
    set(${msg_tuples_var} ${msg_tuples} PARENT_SCOPE)
endfunction()
