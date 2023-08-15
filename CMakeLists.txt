cmake_minimum_required(VERSION 3.16 FATAL_ERROR)

project(foobar VERSION 0.0.1 LANGUAGES CXX)

if(DEFINED ENV{CONDA_PREFIX})
  set(CMAKE_PREFIX_PATH "$ENV{CONDA_PREFIX};${CMAKE_PREFIX_PATH}")
  message(STATUS "Detected Conda environment, CMAKE_PREFIX_PATH set to: ${CMAKE_PREFIX_PATH}")
  if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT OR USING_CONDA_INSTALL_PREFIX)
    message(STATUS "No CMAKE_INSTALL_PREFIX argument detected, setting to: $ENV{CONDA_PREFIX}")
    set(CMAKE_INSTALL_PREFIX $ENV{CONDA_PREFIX})
    set(USING_CONDA_INSTALL_PREFIX ON CACHE BOOL "Installing into Conda prefix")
  endif()
else()
  message(STATUS "No Conda environment detected")
endif()

find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)
find_package(pybind11 CONFIG REQUIRED)

add_library(objfoobar OBJECT src/foobar.cc include/foobar/foobar.h)
target_include_directories(objfoobar PUBLIC
  $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
  $<BUILD_INTERFACE:${PROJECT_BINARY_DIR}/include>
  $<INSTALL_INTERFACE:$<INSTALL_PREFIX>/include>)

add_library(foobar SHARED)
target_link_libraries(foobar PRIVATE objfoobar)

python_add_library(_ext MODULE python/ext.cpp WITH_SOABI)
target_link_libraries(_ext PRIVATE pybind11::headers objfoobar)
target_compile_definitions(_ext PRIVATE VERSION_INFO=${PROJECT_VERSION})

include(GNUInstallDirs)
include(CMakePackageConfigHelpers)
if(SKBUILD)
  install(
    TARGETS _ext
    DESTINATION foobar
  )
#install(DIRECTORY python/foobar
#    DESTINATION foobar)
else()
  install(
    TARGETS foobar objfoobar
    EXPORT FoobarTargets
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    INCLUDES DESTINATION include
  )
  install(DIRECTORY include/foobar
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
endif()
