// Copyright Epic Games, Inc. All Rights Reserved.

#include <riglogic/RigLogic.h>

#include <cmath>
#include <iostream>

int main(int argc, char** argv) {
    auto stream =
        rl4::makeScoped<rl4::FileStream>("character.dna", rl4::FileStream::AccessMode::Read, rl4::FileStream::OpenMode::Binary);
    auto reader = rl4::makeScoped<rl4::BinaryStreamReader>(stream.get());
    reader->read();
    if (!rl4::Status::isOk()) {
        auto status = rl4::Status::get();
        std::cout << status.message << std::endl;
        return -1;
    }

    auto rigLogic = rl4::makeScoped<rl4::RigLogic>(reader.get());
    auto rigInstance = rl4::makeScoped<rl4::RigInstance>(rigLogic.get());

    std::uint64_t frame = 0ul;

    while (true) {
        for (std::uint16_t ctrlIndex = 0u; ctrlIndex < rigInstance->getRawControlCount(); ++ctrlIndex) {
            const float val = std::fabs(std::sin(frame / 1000.0f));
            rigInstance->setRawControl(ctrlIndex, val);
        }

        rigLogic->calculate(rigInstance.get());
        const auto jointDeltas = rigInstance->getJointOutputs();
        const auto blendShapeChannels = rigInstance->getBlendShapeOutputs();
        const auto animatedMapChannels = rigInstance->getAnimatedMapOutputs();

        ++frame;
    }

    return 0;
}
