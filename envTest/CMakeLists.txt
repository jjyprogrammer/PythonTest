cmake_minimum_required(VERSION 3.0.0)
project(CppProject VERSION 0.1.0)

include(CTest)
enable_testing()

add_executable(CppProject main.cpp)

if(DEFINED ENV{Build_Type})
    message(STATUS  "123")
    if($ENV{Build_Type} STREQUAL "CI")
        message(STATUS "456")
    endif()
endif()
if(TRUE AND NOT DEFINED ENV{Build_Type})
    message("888")
endif()

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
