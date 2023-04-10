#include <Windows.h>
#include <iostream>
#include <string>


int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cout << "Usage: " << argv[0] << " <program name> <string>" << std::endl;
        return 1;
    }

    DWORD pid = std::atoi(argv[1]);
    std::string str(argv[2]);

    HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);
    if (hProcess == NULL) {
        std::cout << "Error: OpenProcess failed" << std::endl;
        return 1;
    }

    SYSTEM_INFO sysInfo;
    GetSystemInfo(&sysInfo);

    MEMORY_BASIC_INFORMATION64 memInfo;
    ZeroMemory(&memInfo, sizeof(MEMORY_BASIC_INFORMATION64));

    ULONGLONG dwAddress = 0;
    while (dwAddress < (ULONGLONG)sysInfo.lpMaximumApplicationAddress) {
        if (VirtualQueryEx(hProcess, (LPCVOID)dwAddress, (PMEMORY_BASIC_INFORMATION)&memInfo, sizeof(MEMORY_BASIC_INFORMATION64)) == sizeof(MEMORY_BASIC_INFORMATION64)) {
            if ((memInfo.State == MEM_COMMIT) && (memInfo.Type == MEM_PRIVATE)) {
                char* pBuffer = new char[memInfo.RegionSize];
                SIZE_T bytesRead = 0;
                if (ReadProcessMemory(hProcess, (LPCVOID)memInfo.BaseAddress, pBuffer, memInfo.RegionSize, &bytesRead)) {
                    for (ULONGLONG i = 0; i < bytesRead; i++) {
                        if (memcmp(&pBuffer[i], str.c_str(), str.length()) == 0) {
                            std::cout << "Found string at address: 0x" << std::hex << ((ULONGLONG)memInfo.BaseAddress + i) << std::endl;
                            char* outputPtr = &pBuffer[i];
                            while (*outputPtr != '\0')
                            {
                                std::cout << *outputPtr;
                                outputPtr++;
                            }
                            std::cout << std::endl;
    
                        }
                    }
                }
                delete[] pBuffer;
            }
        }
        dwAddress = (ULONGLONG)memInfo.BaseAddress + memInfo.RegionSize;
    }

    CloseHandle(hProcess);

    return 0;
}
