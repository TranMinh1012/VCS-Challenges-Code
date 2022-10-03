#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pwd.h>
#include <shadow.h>
#include <unistd.h>
#include <crypt.h>
#include <time.h>

int check_passwd(char passwd[], char user[]) {
    struct spwd* shadow = getspnam(user);
    if (shadow != NULL) {
        return strcmp(shadow->sp_pwdp, crypt(passwd, shadow->sp_pwdp));
    }        
}

char* generate_salt(char salt[]) {
    const char *const seed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789./";
    int i, seed_length = strlen(seed);
    srand(time(NULL));
    for (i = 0; i < 16; i++) {
        int seed_rand = rand() % seed_length;
        salt[3+i] = seed[seed_rand];
    }
    return salt;
}

int main() {
    char current_passwd[128], new_passwd[128], user[] = "svminhtt";
    char salt[20] = "$6$";
    struct spwd *shadow_entry;
    printf("Enter a current password: ");
    scanf("%s", current_passwd);
    char shadow_entry_name[128];
    if (!check_passwd(current_passwd, user)) {
        while ((shadow_entry = getspent()) != NULL) {
            strcpy(shadow_entry_name, shadow_entry->sp_namp);
            if(!strcmp(shadow_entry_name, user)) {
                break;
            }
        }       
        printf("Enter a new password: ");
        scanf("%s", new_passwd);
        strcpy(salt, generate_salt(salt));
        char* hash_char = crypt(new_passwd, salt);
        shadow_entry->sp_pwdp = hash_char;        
        printf("Password updated successfully!!!\n");
        return 1;
    }   
    printf("Password authentication failure\n");
    return 1;
}