// Copyright Epic Games, Inc. All Rights Reserved.

// *INDENT-OFF*
#include <riglogic/RigLogic.h>

#include <cmath>
#include <iostream>
#include <memory>
#include <string>

class CustomMemoryResource : public rl4::MemoryResource {
public:
    void* allocate(std::size_t size, std::size_t alignment) override {
        return std::malloc(size);
    }

    void deallocate(void* ptr, std::size_t size, std::size_t alignment) override {
        std::free(ptr);
    }
};

int main(int argc, char** argv) {
    CustomMemoryResource memRes{};
    auto stream = rl4::makeScoped<rl4::FileStream>("character.dna",
                                                   rl4::FileStream::AccessMode::Read,
                                                   rl4::FileStream::OpenMode::Binary,
                                                   &memRes);
    dna::Configuration dnacfg = {};
    dnacfg.layer = rl4::DataLayer::All;
    dnacfg.unknownLayerPolicy = rl4::UnknownLayerPolicy::Ignore;
    dnacfg.maxLOD = 2;
    auto reader = rl4::makeScoped<rl4::BinaryStreamReader>(stream.get(), dnacfg, &memRes);
    reader->read();
    if (!rl4::Status::isOk()) {
        auto status = rl4::Status::get();
        std::cout << status.message << std::endl;
        if (status == rl4::FileStream::OpenError) {
            // Handle file open error
        } else if (status == rl4::FileStream::ReadError) {
            // Handle file read error
        } else if (status == rl4::BinaryStreamReader::SignatureMismatchError) {
            // Handle dna signature mismatch error
        } else if (status == rl4::BinaryStreamReader::VersionMismatchError) {
            // Handle dna version mismatch error
        }
        return -1;
    }

    rl4::Configuration config{};
    // Further refine which data to load from DNA and possibly additionally reduce the runtime compute
    config.loadJoints = true;
    config.loadBlendShapes = true;
    config.loadAnimatedMaps = true;
    config.loadMachineLearnedBehavior = true;
    config.loadRBFBehavior = true;
    config.loadTwistSwingBehavior = true;
    // Causes 4 attributes to be present per joint rotation in both neutral joint values and calculated joint deltas
    config.rotationType = rl4::RotationType::Quaternions;

    auto rigLogic = rl4::makeScoped<rl4::RigLogic>(reader.get(), config, &memRes);
    auto rigInstance = rl4::makeScoped<rl4::RigInstance>(rigLogic.get(), &memRes);

    std::uint32_t controlToManipulate = 4u;
    std::uint64_t frame = 0u;

    // Bind pose joint attribute values in the following format:
    // [j0.tx, j0.ty, j0.tz, j0.qx, j0.qy, j0.qz, j0.qw, j0.sx, j0.sy, j0.sz, j1.tx, j1.ty, j1.tz, j1.qx, j1.qy, j1.qz, j1.qw,
    // j1.sx, j1.sy, j1.sz, ...] where: tx, ty tz are the translation attributes qx, qy, qz, qw are the rotation quaternion
    // attributes sx, sy, sz are the scale attributes
    rl4::ConstArrayView<float> bindPoseJoints = rigLogic->getNeutralJointValues();

    while (true) {
        const std::uint16_t currentLOD = frame % 4ul;
        rigInstance->setLOD(currentLOD);

        rl4::ArrayView<float> rawControlBuffer = rigInstance->getRawControlValues();
        for (std::uint16_t ctrlIndex = 0u; ctrlIndex < rigInstance->getRawControlCount(); ++ctrlIndex) {
            if (ctrlIndex == controlToManipulate) {
                const float val = std::fabs(std::sin(frame / 1000.0f));
                rawControlBuffer[ctrlIndex] = val;
            }
        }

        // Makes sense if ML layer exists in DNA and `config.loadMachineLearnedBehavior` was set
        rigLogic->calculateMLControls(rigInstance.get());
        // Makes sense if RBF layer exists in DNA and `config.loadRBFBehavior` was set
        rigLogic->calculateRBFControls(rigInstance.get());

        rigLogic->calculatePSDControls(rigInstance.get());
        rigLogic->calculateJoints(rigInstance.get());
        rigLogic->calculateBlendShapes(rigInstance.get());
        rigLogic->calculateAnimatedMaps(rigInstance.get());

        // These indices point to only those individual joint attributes of both getJointOutputs() and getNeutralJointValues()
        // arrays which are changing when computing joint transforms for the current LOD
        rl4::ConstArrayView<std::uint16_t> jointVariableAttributeIndices = rigLogic->getJointVariableAttributeIndices(currentLOD);

        // Joint deltas need to be combined with the bind pose (neutral values), and they follow the exact same format as the bind
        // pose values
        rl4::ConstArrayView<float> jointDeltas = rigInstance->getJointOutputs();

        // Use only results that are needed for the current LOD (see getJointVariableAttributeIndices).
        // The below example accesses the attributes of Joint-0 (all attributes, regardless if they're part of the variable
        // attribute indices of the current LOD)
        const rl4::fvec3 j0translation = {bindPoseJoints[0] + jointDeltas[0],
                                          bindPoseJoints[1] + jointDeltas[1],
                                          bindPoseJoints[2] + jointDeltas[2]};
        const rl4::fquat j0BindPoseRotation =
            rl4::fquat{bindPoseJoints[3], bindPoseJoints[4], bindPoseJoints[5], bindPoseJoints[6]};
        const rl4::fquat j0DeltaRotation = rl4::fquat{jointDeltas[3], jointDeltas[4], jointDeltas[5], jointDeltas[6]};
        const rl4::fquat j0Rotation = j0BindPoseRotation * j0DeltaRotation;
        const rl4::fvec3 j0scale = {bindPoseJoints[7] + jointDeltas[7],
                                    bindPoseJoints[8] + jointDeltas[8],
                                    bindPoseJoints[9] + jointDeltas[9]};

        rl4::ConstArrayView<float> blendShapeChannels = rigInstance->getBlendShapeOutputs();
        rl4::ConstArrayView<float> animatedMapChannels = rigInstance->getAnimatedMapOutputs();

        ++frame;
    }

    return 0;
}
// *INDENT-ON*
