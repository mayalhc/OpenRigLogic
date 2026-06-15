set(SOURCES
    Advanced.cpp
    Basic.cpp
    Sample.cpp)

source_group(TREE ${CMAKE_CURRENT_SOURCE_DIR} FILES ${SOURCES})

foreach(example IN LISTS SOURCES)
    get_filename_component(filename ${example} NAME_WE)
    string(TOLOWER ${filename} example_target_name)
    add_executable(${example_target_name} ${example})
    target_link_libraries(${example_target_name} PRIVATE ${RL})
    set_target_properties(${example_target_name} PROPERTIES
                          CXX_STANDARD ${CMAKE_CXX_STANDARD}
                          CXX_STANDARD_REQUIRED NO
                          CXX_EXTENSIONS NO
                          FOLDER examples)
    list(APPEND EXAMPLE_TARGETS ${example_target_name})
endforeach()

set(RL_EXAMPLES ${EXAMPLE_TARGETS} PARENT_SCOPE)
