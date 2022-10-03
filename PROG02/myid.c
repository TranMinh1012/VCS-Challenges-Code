#include<stdio.h>
#include<stdlib.h>
#include<sys/types.h>
#include<pwd.h>
#include<grp.h>

int main(){
    struct passwd *pw;
    char username[100];
    printf("Nhap username: ");
    gets(username);

    if((pw == getpwnam(username)) == NULL){
        printf("User khong ton tai trong he thong\n");
        exit(EXIT_FAILURE);
    }
    else {
        printf("ID cua user %s la           : %d\n", pw->pw_name, (int) pw->pw_uid);
        printf("Username cua user %s la     : %s\n", pw->pw_name, pw->pw_name);
        printf("Thu muc home cua user %s la : %s\n", pw->pw_name, pw->pw_dir);
        printf("Cac group cua user %s la    :   \n", pw->pw_name);

        int ngroups = 0;

        getgrouplist(pw->pw_name, pw->pw_gid, NULL, &ngroups);
        __gid_t groups[ngroups];

        getgrouplist(pw->pw_name, pw->pw_gid, groups, &ngroups);

        for(int i = 0; i < ngroups; i++){
            struct group *gr = getgrgid(groups[i]);
            printf("+ %s\n", gr->gr_name);
        }
    }
    return 0;
}