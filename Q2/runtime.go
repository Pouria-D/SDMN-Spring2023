package main

import (
	"io/ioutil"
	"os"
	"os/exec"
	"path/filepath"
	"strconv"
	"syscall"
)

// go run runtime.go run <hostname> <limit>
// docker run            <hostname> <limit>

func main() {
	switch os.Args[1] {
	case "run":
		run()
	case "child":
		child()
	default:
		panic("invalid command!!")
	}
}

func run() {
	
	// create container foledr
	container_path := filepath.Join("Containers", os.Args[2])
	cmd_cp := exec.Command("cp", "-R", "file_system", container_path)
	cmd_cp.Stdin = os.Stdin
	cmd_cp.Stdout = os.Stdout
	cmd_cp.Stderr = os.Stderr
	cmd_cp.Run()
	
	// run container
	args := append([]string{"child"},  os.Args[2:]...)
  	cmd := exec.Command("/proc/self/exe", args...)
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	cmd.SysProcAttr = &syscall.SysProcAttr{
		Cloneflags: syscall.CLONE_NEWUTS | syscall.CLONE_NEWPID | syscall.CLONE_NEWNS | syscall.CLONE_NEWNET,
		Unshareflags: syscall.CLONE_NEWNS,
	}
	cmd.Run()
	
	// delete limit-memory foledr (cgroup)
	if len(os.Args) > 3 {
		cgPath := filepath.Join("/sys/fs/cgroup/memory", "limit-memory")
		cmd_rm := exec.Command("rmdir", cgPath)
		cmd_rm.Stdin = os.Stdin
		cmd_rm.Stdout = os.Stdout
		cmd_rm.Stderr = os.Stderr
		cmd_rm.Run()
	}
}

func child() {
	
	hostname := os.Args[2]
	
	if len(os.Args) > 3 {
		limit, _ := strconv.Atoi(os.Args[3])
		ControlGroup(limit)
	}
	
	dir, _ := os.Getwd()
	root := filepath.Join(dir, "Containers", hostname)
	
	syscall.Sethostname([]byte(hostname))
	syscall.Chroot(root)
	syscall.Chdir("/")
	syscall.Mount("proc", "proc", "proc", 0, "")

	cmd := exec.Command("/bin/bash")
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	cmd.Run()
	
	syscall.Unmount("/proc", 0)
}

func ControlGroup(limit int) {
	cgPath := filepath.Join("/sys/fs/cgroup/memory", "limit-memory")
	os.Mkdir(cgPath, 0755)
	ioutil.WriteFile(filepath.Join(cgPath, "memory.limit_in_bytes"), []byte(strconv.Itoa(limit * 1000000)), 0700)
	ioutil.WriteFile(filepath.Join(cgPath, "memory.swappiness"), []byte("0"), 0700)
	ioutil.WriteFile(filepath.Join(cgPath, "tasks"), []byte(strconv.Itoa(os.Getpid())), 0700)
}

