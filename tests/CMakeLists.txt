include(GoogleTest)

if(DEFINED TESTS)
    set(TEST_RUNNER TestRunner.cpp)
    set(SOURCES)
    foreach(path IN LISTS TESTS)
        file(RELATIVE_PATH relpath "${CMAKE_CURRENT_SOURCE_DIR}/tests" "${CMAKE_CURRENT_SOURCE_DIR}/${path}")
        if(NOT ${relpath} MATCHES ${TEST_RUNNER})
            list(APPEND SOURCES ${relpath})
        endif()
    endforeach()
else()
    set(TEST_RUNNER rltests/TestRunner.cpp)

    set(SOURCES
        rltests/Defs.h
        rltests/StorageValueType.h

        rltests/animatedmaps/AnimatedMapFixtures.cpp
        rltests/animatedmaps/AnimatedMapFixtures.h
        rltests/animatedmaps/TestAnimatedMaps.cpp

        rltests/blendshapes/BlendShapeFixtures.cpp
        rltests/blendshapes/BlendShapeFixtures.h
        rltests/blendshapes/TestBlendShapes.cpp

        rltests/conditionaltable/ConditionalTableFixtures.cpp
        rltests/conditionaltable/ConditionalTableFixtures.h
        rltests/conditionaltable/TestConditionalTable.cpp

        rltests/controls/ControlFixtures.cpp
        rltests/controls/ControlFixtures.h
        rltests/controls/TestControls.cpp

        rltests/dna/DNAFixtures.cpp
        rltests/dna/DNAFixtures.h
        rltests/dna/FakeReader.cpp
        rltests/dna/FakeReader.h

        rltests/joints/Helpers.h
        rltests/joints/TestJointsFactory.cpp
        rltests/joints/bpcm/Assertions.h
        rltests/joints/bpcm/BPCMFixturesBlock4.cpp
        rltests/joints/bpcm/BPCMFixturesBlock4.h
        rltests/joints/bpcm/BPCMFixturesBlock8.cpp
        rltests/joints/bpcm/BPCMFixturesBlock8.h
        rltests/joints/bpcm/Helpers.h
        rltests/joints/bpcm/TestBlock4CalculationStrategy.cpp
        rltests/joints/bpcm/TestBlock4StorageBuilder.cpp
        rltests/joints/bpcm/TestBlock8CalculationStrategy.cpp
        rltests/joints/bpcm/TestBlock8StorageBuilder.cpp
        rltests/joints/quaternions/QuaternionFixtures.cpp
        rltests/joints/quaternions/QuaternionFixtures.h
        rltests/joints/quaternions/TestQuaternionEvaluator.cpp
        rltests/joints/quaternions/TestQuaternionStorageBuilder.cpp
        rltests/joints/twistswing/TwistSwingFixtures.cpp
        rltests/joints/twistswing/TwistSwingFixtures.h
        rltests/joints/twistswing/TestTwistSwingEvaluator.cpp
        rltests/joints/twistswing/TestTwistSwingStorageBuilder.cpp
        rltests/joints/utils/TestLODRegion.cpp

        rltests/ml/cpu/FixturesBlock4.cpp
        rltests/ml/cpu/FixturesBlock4.h
        rltests/ml/cpu/FixturesMLBChained.cpp
        rltests/ml/cpu/FixturesMLBChained.h
        rltests/ml/cpu/TestInference.cpp
        rltests/ml/cpu/TestMLBChained.cpp
        rltests/ml/cpu/TestStorageBuilder.cpp

        rltests/psdnet/TestPSDNet.cpp

        rltests/rbf/cpu/RBFFixtures.cpp
        rltests/rbf/cpu/RBFFixtures.h
        rltests/rbf/cpu/TestRBFEvaluator.cpp
        rltests/rbf/cpu/TestRBFSolver.cpp
        rltests/rbf/cpu/TestRBFStorageBuilder.cpp

        rltests/riglogic/TestRigLogic.cpp)
endif()

source_group(TREE ${CMAKE_CURRENT_SOURCE_DIR} FILES ${SOURCES})

add_library(${RL_TEST_LIB} OBJECT ${SOURCES})
add_library(RigLogic::tests ALIAS ${RL_TEST_LIB})
get_target_property(RL_SOURCE_ROOT ${RL} SOURCE_ROOT)
target_include_directories(${RL_TEST_LIB} PRIVATE ${RL_SOURCE_ROOT})
target_include_directories(${RL_TEST_LIB} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(${RL_TEST_LIB} PRIVATE ${RL} ${RL_PRIVATE_DEPENDENCIES} gtest)

add_executable(${RL_TEST_RUNNER} $<TARGET_OBJECTS:${RL_TEST_LIB}> ${TEST_RUNNER})
target_include_directories(${RL_TEST_RUNNER} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(${RL_TEST_RUNNER} PRIVATE ${RL} gtest)
add_test(NAME unittests COMMAND ${CMAKE_COMMAND} -E env "PATH=$ENV{PATH}" $<TARGET_FILE:${RL_TEST_RUNNER}>)

set_target_properties(${RL_TEST_LIB} ${RL_TEST_RUNNER} PROPERTIES
                      CXX_STANDARD ${CMAKE_CXX_STANDARD}
                      CXX_STANDARD_REQUIRED NO
                      CXX_EXTENSIONS NO
                      FOLDER tests
                      SOURCE_ROOT "${CMAKE_CURRENT_SOURCE_DIR}")
