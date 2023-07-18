macro(GENERATE_THRIFT_LIB LIB_NAME FILENAME OUTPUTDIR SOURCES)
    file(MAKE_DIRECTORY ${OUTPUTDIR})
    detect_maadeps_triplet(MAADEPS_HOST_ARCH)
    if(EXISTS ${PROJECT_SOURCE_DIR}/MaaDeps/vcpkg/installed/${MAADEPS_HOST_ARCH}/tools/thrift/thrift${CMAKE_EXECUTABLE_SUFFIX})
        set(THRIFT_COMPILER ${PROJECT_SOURCE_DIR}/MaaDeps/vcpkg/installed/${MAADEPS_HOST_ARCH}/tools/thrift/thrift${CMAKE_EXECUTABLE_SUFFIX})
    else()
        find_program(THRIFT_COMPILER thrift)
    endif()
    execute_process(COMMAND ${THRIFT_COMPILER} --gen cpp:no_skeleton -out ${OUTPUTDIR} ${FILENAME}
                    RESULT_VARIABLE CMD_RESULT)
    if(CMD_RESULT)
        message(FATAL_ERROR "Error generating ${FILENAME} with generator ${GENERATOR}")
    endif()
    file(GLOB_RECURSE GENERATED_SOURCES ${OUTPUTDIR}/*.cpp)
    add_library(${LIB_NAME} STATIC ${GENERATED_SOURCES})
    set_target_properties(${LIB_NAME} PROPERTIES POSITION_INDEPENDENT_CODE ON)
    target_link_libraries(${LIB_NAME} ${THRIFT_LIBRARIES})
    set(${LIB_NAME}_INCLUDE_DIRS ${OUTPUTDIR} PARENT_SCOPE)
    set(${SOURCES} ${GENERATED_SOURCES})
endmacro(GENERATE_THRIFT_LIB)
