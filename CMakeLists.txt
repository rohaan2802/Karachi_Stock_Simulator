cmake_minimum_required(VERSION 3.20)
project(Karachi_Stock_Simulator LANGUAGES CXX)

if(NOT WIN32)
    message(FATAL_ERROR "Karachi Stock Simulator uses the Windows console API.")
endif()

add_executable(Karachi_Stock_Simulator src/market_simulator.cpp)
target_compile_features(Karachi_Stock_Simulator PRIVATE cxx_std_17)
target_link_libraries(Karachi_Stock_Simulator PRIVATE user32)
if(MSVC)
    target_compile_options(Karachi_Stock_Simulator PRIVATE /W4 /utf-8)
else()
    target_compile_options(Karachi_Stock_Simulator PRIVATE -Wall -Wextra -Wpedantic)
endif()

file(MAKE_DIRECTORY "${CMAKE_BINARY_DIR}/session")
configure_file(data/companies.csv "${CMAKE_BINARY_DIR}/session/companies.csv" COPYONLY)
set_target_properties(Karachi_Stock_Simulator PROPERTIES
    VS_DEBUGGER_WORKING_DIRECTORY "${CMAKE_BINARY_DIR}/session")
