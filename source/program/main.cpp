#include "lib.hpp"       // <--- Исправляет ошибку HOOK_DEFINE_TRAMPOLINE
#include "common.hpp"
#include "fs.hpp"
#include <cstring>

#define MOUNT_NAME "ExlSD"

// Объявляем nnMain, чтобы компилятор его видел
extern "C" void nnMain();

void RunFsTest() {
    nn::fs::MountSdCardForDebug(MOUNT_NAME);

    const char* path = MOUNT_NAME ":/hook_nnmain_test.txt";
    nn::fs::CreateFile(path, 0);
    
    nn::fs::FileHandle handle;
    if (R_SUCCEEDED(nn::fs::OpenFile(&handle, path, nn::fs::OpenMode_Write | nn::fs::OpenMode_Append))) {
        const char* text = "Hello from nnMain hook!\n";
        long size = 0;
        nn::fs::GetFileSize(&size, handle);
        
        auto opt = nn::fs::WriteOption::CreateOption(nn::fs::WriteOptionFlag_Flush);
        nn::fs::WriteFile(handle, size, text, std::strlen(text), opt);
        nn::fs::CloseFile(handle);
    }
}

// Хук для void nnMain() без аргументов
HOOK_DEFINE_TRAMPOLINE(MainHook) {
    static void Callback() {
        RunFsTest(); // Наш код
        Orig();      // Оригинальный nnMain
    }
};

extern "C" void exl_main(void* x0, void* x1) {
    exl::hook::Initialize();
    
    // Пытаемся установить хук, используя указатель на функцию
    MainHook::InstallAtFuncPtr(nnMain);
}