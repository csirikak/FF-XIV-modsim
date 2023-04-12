#include <Windows.h>
#include <iostream>
#include <string>
#include <vector>
#include <condition_variable>

// Define a constant array of unsigned char to be searched for in memory
const unsigned char list_start[13] = {0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x95, 0x01, 0x95, 0x01}; //Seraph
const unsigned char count_start[4] = {0x2F, 0x32, 0x30, 0x30};
bool playerList = FALSE;
bool playerCount = FALSE;

// Define a structure to represent a chunk of memory
struct MemoryChunk {    
    ULONGLONG baseAddress;
    SIZE_T size;
};

// Define a function to enable/disable a privilege for the current process token.
BOOL SetPrivilege(HANDLE hToken, LPCTSTR lpszPrivilege, BOOL bEnablePrivilege) {
    TOKEN_PRIVILEGES tp;
    LUID luid;

    if (!LookupPrivilegeValue(NULL, lpszPrivilege, &luid)) {
        return FALSE;
    }

    tp.PrivilegeCount = 1;
    tp.Privileges[0].Luid = luid;
    tp.Privileges[0].Attributes = bEnablePrivilege ? SE_PRIVILEGE_ENABLED : 0;

    if (!AdjustTokenPrivileges(hToken, FALSE, &tp, sizeof(TOKEN_PRIVILEGES), NULL, NULL)) {
        return FALSE;
    }

    if (GetLastError() == ERROR_NOT_ALL_ASSIGNED) {
        return FALSE;
    }

    return TRUE;
}

// Define a function to search for the specified byte pattern in the memory chunk provided.
void searchMemory(HANDLE hProcess, const unsigned char (&list_start)[13], const unsigned char (&count_start)[4], const MemoryChunk& chunk) {
    //std::cout << "Searching memory from 0x" << std::hex << chunk.baseAddress << " to 0x" << chunk.baseAddress + chunk.size << std::endl;
    char* pBuffer = new char[chunk.size];
    SIZE_T bytesRead = 0;
    if (ReadProcessMemory(hProcess, (LPCVOID)chunk.baseAddress, pBuffer, chunk.size, &bytesRead)) {
        for (ULONGLONG i = 0; i < bytesRead; i++) {
            if (!playerList){ 
                if (!memcmp(&pBuffer[i], list_start, 13)) {
                    std::cout << "Found playerList at address: 0x" << std::hex << (chunk.baseAddress + i) << std::endl;
                    playerList = true;
                }
            }
            if (!playerCount){
                if (!memcmp(&pBuffer[i], count_start, 4)) {
                    std::cout << "Found playerCount at address: 0x" << std::hex << (chunk.baseAddress + i - 2) << std::endl;
                    playerCount = true;
                }
            }
        }
    }
    delete[] pBuffer;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "Usage: " << argv[0] << " <process ID>" << std::endl;
        return 1;
    }

    DWORD pid = std::atoi(argv[1]);

    HANDLE hToken = NULL;
    // Get the process token for the current process.
    if (!OpenProcessToken(GetCurrentProcess(), TOKEN_ADJUST_PRIVILEGES, &hToken)) {
        std::cout << "Error: OpenProcessToken failed, Error code: " << GetLastError() << std::endl;
        return 1;
    }
    // Set the priviledge of the current process.
    if (!SetPrivilege(hToken, SE_DEBUG_NAME, TRUE)) {
        std::cout << "Error: SetPrivilege failed, Error code: " << GetLastError() << std::endl;
        CloseHandle(hToken);
        return 1;
    }

    CloseHandle(hToken);

    // Creates a handle to the target process
    HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);
    if (hProcess == NULL) {
        std::cout << "Error: OpenProcess failed, Error code: " << GetLastError() << std::endl;
        return 1;
    }

    SYSTEM_INFO sysInfo;
    GetSystemInfo(&sysInfo);

    //Creates a Vector of memory chunks to be searched. 
    std::vector<MemoryChunk> memoryChunks;
    ULONGLONG dwAddress = 0;
    while (dwAddress < (ULONGLONG)sysInfo.lpMaximumApplicationAddress) {
        MEMORY_BASIC_INFORMATION64 memInfo;
        ZeroMemory(&memInfo, sizeof(MEMORY_BASIC_INFORMATION64));
        if (VirtualQueryEx(hProcess, (LPCVOID)dwAddress, (PMEMORY_BASIC_INFORMATION)&memInfo, sizeof(MEMORY_BASIC_INFORMATION64)) == sizeof(MEMORY_BASIC_INFORMATION64)) {
            if ((memInfo.State == MEM_COMMIT) && (memInfo.Type == MEM_PRIVATE)) {
                MemoryChunk chunk;
                chunk.baseAddress = (ULONGLONG)memInfo.BaseAddress;
                chunk.size = memInfo.RegionSize;
                memoryChunks.push_back(chunk);
            }
        }
        dwAddress = (ULONGLONG)memInfo.BaseAddress + memInfo.RegionSize;
    }


    //Iterates through the vector of chunks.
    for (int i = 0; i < memoryChunks.size(); i++) {
        searchMemory(hProcess, list_start, count_start, memoryChunks[i]);
    }
    
    CloseHandle(hProcess);

    return 0;
}
