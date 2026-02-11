#pragma once
#include "lib.hpp"
#define FIX(addr)           ((addr) - 0x100)
#define ADDR_LOOP_PATCH_1   FIX(0x4C1444)
#define ADDR_LOOP_PATCH_2   FIX(0x4C1374)
#define ADDR_NOP_2    FIX(0x5D1CE0)
#define ADDR_NOP_3    FIX(0x5D2B38)
#define ADDR_NOP_4    FIX(0x5D1CEC)
#define ADDR_UNLOCK_PATCH   FIX(0x0CA400)
#define OFFSET_SATURATION_1   FIX(0x5D1B64)
#define OFFSET_SATURATION_2   FIX(0x5D29B0)
#define ADDR_MOD_CSEL_1 FIX(0x000C4E58)
#define ADDR_MOD_CSEL_2 FIX(0x000C835C)
#define ADDR_COS_LIMIT_1 FIX(0x000C6F0C)
#define ADDR_COS_LIMIT_2 FIX(0x0076D9C4)
#define ADDR_COS_LIMIT_3 FIX(0x00519CA0)
#define ADDR_EFF_LIMIT FIX(0x0017B710)

inline void ApplyCustomPatches() {
    exl::patch::CodePatcher(ADDR_LOOP_PATCH_1).Write<uint32_t>(0xF1400EBF);
    exl::patch::CodePatcher(ADDR_LOOP_PATCH_2).Write<uint32_t>(0xF1400EBF);
    exl::patch::CodePatcher(ADDR_NOP_2).Write<uint32_t>(0xD503201F);
    exl::patch::CodePatcher(ADDR_NOP_3).Write<uint32_t>(0xD503201F);
    exl::patch::CodePatcher(ADDR_NOP_4).Write<uint32_t>(0xD503201F);
    exl::patch::CodePatcher(OFFSET_SATURATION_1).Write<uint32_t>(0x710F951F);
    exl::patch::CodePatcher(OFFSET_SATURATION_2).Write<uint32_t>(0x710F903F);
    exl::patch::CodePatcher(ADDR_UNLOCK_PATCH).Write<uint32_t>(0x52800020);
    exl::patch::CodePatcher(ADDR_MOD_CSEL_1).Write<uint32_t>(0x2A0103E8);
    exl::patch::CodePatcher(ADDR_MOD_CSEL_2).Write<uint32_t>(0x2A0803E0);
    exl::patch::CodePatcher(ADDR_COS_LIMIT_1).Write<uint32_t>(0x14000004);
    exl::patch::CodePatcher(ADDR_COS_LIMIT_2).Write<uint32_t>(0x2A0003F8);
    exl::patch::CodePatcher(ADDR_EFF_LIMIT).Write<uint32_t>(0x7103FC3F);
    exl::patch::CodePatcher(ADDR_COS_LIMIT_3).Write<uint32_t>(0x2A1F03E9);
}
