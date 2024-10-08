Question 2

In this process, a container file will be created in "Container" folder with name "hostname". 
The file_system folder is Ubuntu 20.04 and with creating container, this folder will be copied to container folder.
If the 3rd arg is set, a folder with name limit-memory will be created at cgroup and after exiting container, that folder will be removed.

in cmd run the command:

go run runtime.go run "hostname" "limit-memory"

