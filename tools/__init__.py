import subprocess


def get_pid(device_id, package):
    cmd = f'adb -s {device_id} shell "dumpsys activity top | grep ACTIVITY"'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    lines = out.decode().split("\n")
    for line in lines:
        parts = line.split(" ")
        parts = [i.replace('\r', '') for i in parts if i]
        if not parts:
            continue
        if package in parts[1]:
            return parts[3].replace('pid=', '')

    return None


if __name__ == '__main__':
    d = "f9b4ccf9"  # 使用adb devices 获取
    p = "com.tencent.mm/.plugin.appbrand.ui.AppBrandUI"
    pid = get_pid(d, p)
    print(pid)
