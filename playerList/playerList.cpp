#include <Windows.h>
#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <iomanip>
#include <cstdint>

//Define a constant char array to find empty lines.
const unsigned char empty_line[16] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};

//A function to parse a runtime arg as a ULONGLONG for the pointer type
ULONGLONG parseHexArgument(const char* arg)
{
    // Create an input string stream from the argument
    std::istringstream iss(arg);

    // Read the value as a hexadecimal number
    ULONGLONG value;
    iss >> std::hex >> value;

    // Check for errors during parsing
    if (iss.fail() || !iss.eof()) {
        throw std::invalid_argument("Invalid hexadecimal string: " + std::string(arg));
    }

    // Return the parsed value
    return value;
}

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

//Prints the list of player names given the memory address
void printList(HANDLE hProcess, ULONGLONG memAddressLocation){
    char* pBuffer = new char[65536];
    SIZE_T bytesRead = 0;
    std::cout << "Printing list at: 0x" << std::hex << std::setw(16) << std::setfill('0') << memAddressLocation << std::endl;
    if (ReadProcessMemory(hProcess, (LPCVOID)memAddressLocation, pBuffer, 65536, &bytesRead)) {
        //Offset the initial output by 21 bytes
        for (ULONGLONG i = 21; i < bytesRead; i++) {
            char* outputPtr = &pBuffer[i];
            //Stops on meeting an empty line
            if (!memcmp(&pBuffer[i], empty_line, 16)){
                i = bytesRead;
                std::cout << "EOL";
            }
            else {
                //Ends name output when meeting '\0'
                while (*outputPtr != '\0')
                {
                    std::cout << *outputPtr;
                    outputPtr++;
                }
                std::cout << std::endl;
                i+=95; //Offset by 95 bytes to the next name
            }
        }
    }
    else {
        std::cout << "Error: ReadProcessMemory failed, Error code: " << GetLastError() << std::endl;
    }
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cout << "Usage: " << argv[0] << " <process ID> <memory address>" << std::endl;
        return 1;
    }

    DWORD pid = std::atoi(argv[1]);

    HANDLE hToken = NULL;
    if (!OpenProcessToken(GetCurrentProcess(), TOKEN_ADJUST_PRIVILEGES, &hToken)) {
        std::cout << "Error: OpenProcessToken failed, Error code: " << GetLastError() << std::endl;
        return 1;
    }

    if (!SetPrivilege(hToken, SE_DEBUG_NAME, TRUE)) {
        std::cout << "Error: SetPrivilege failed, Error code: " << GetLastError() << std::endl;
        CloseHandle(hToken);
        return 1;
    }
    CloseHandle(hToken);


    HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);
    if (hProcess == NULL) {
        std::cout << "Error: OpenProcess failed, Error code: " << GetLastError() << std::endl;
        return 1;
    }
    try {
    // Parse the argument as an ULONGLONG
        ULONGLONG value = parseHexArgument(argv[2]);
        printList(hProcess, value);
    } 
    catch (const std::exception& e) {
        // Print the error message
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
 
    CloseHandle(hProcess);

    return 0;
}
