import re
from datetime import datetime

# Define the regex pattern to match the syslog entries with flexible space between month and day
log_pattern = re.compile(
    r'^(?P<month>\w{3})\s{1,2}(?P<day>\d{1,2}) (?P<time>\d{2}:\d{2}:\d{2}) (?P<host>\S+) (?P<process>[^\[]+)(?:\[(?P<pid>\d+)\])?: (?P<message>.*)$'
)
# INFO : manage one and 2 space between month and day (syslog and auth.log

def parse_syslog(log_entry):
    match = log_pattern.match(log_entry)
    if match:
        log_dict = match.groupdict()

        # Convert the log entry to a dictionary
        log_dict['datetime'] = datetime.strptime(
            f"{log_dict.pop('month')} {log_dict.pop('day')} {log_dict.pop('time')}", "%b %d %H:%M:%S")
        # Warning if year not specified -> 1900

        # Ensure PID is an integer if present, otherwise set to None
        log_dict['pid'] = int(log_dict['pid']) if log_dict['pid'] else None
        return log_dict
    else:
        print("Failed to parse log entry:", log_entry)
        return None


if __name__ == '__main__':
    # Sample syslog entries
    log_entries = [
        "May 2 14:12:08 fargas systemd-modules-load[362]: Inserted module 'lp'",
        "May 2 14:12:08 fargas systemd-modules-load[362]: Inserted module 'ppdev'client2-virtual-machine",
        "May 2 14:12:08 fargas systemd-modules-load[362]: Inserted module 'parport_pc'",
        "May 2 14:12:08 fargas systemd-modules-load[362]: Inserted module 'msr'",
        "May 2 14:12:08 fargas systemd-modules-load[362]: Inserted module 'ipmi_devintf'",
        "May 2 14:12:08 fargas systemd-modules-load[362]: Module 'fuse' is built in",
        "May 2 14:12:08 fargas systemd-modules-load[362]: Inserted module 'vmwgfx'",
        "May 2 14:12:08 fargas systemd[1]: Starting Flush Journal to Persistent Storage...",
        "May 2 14:12:08 fargas systemd[1]: Finished Apply Kernel Variables.",
        "May 2 14:12:08 fargas systemd[1]: Finished Flush Journal to Persistent Storage.",
        "May 2 14:12:08 fargas systemd[1]: Finished Coldplug All udev Devices.",
        "May 2 14:12:08 fargas systemd[1]: Started Rule-based Manager for Device Events and Files.",
        "May 2 14:12:08 fargas systemd[1]: Starting Show Plymouth Boot Screen...",
        "May 2 14:12:08 fargas systemd[1]: Received SIGRTMIN+20 from PID 419 (plymouthd).",
        "May 2 14:12:08 fargas systemd[1]: Started Show Plymouth Boot Screen.",
        "May 2 14:12:08 fargas systemd[1]: Condition check resulted in Dispatch Password Requests to Console Directory Watch being skipped.",
        "May 2 14:12:08 fargas systemd[1]: Started Forward Password Requests to Plymouth Directory Watch.",
        "May 2 14:12:08 fargas systemd[1]: Reached target Local Encrypted Volumes.",
        "May 2 14:12:08 fargas mtp-probe: checking bus 2, device 2: \"/sys/devices/pci0000:00/0000:00:11.0/0000:02:00.0/usb2/2-1\"",
        "May 2 14:12:08 fargas mtp-probe: bus: 2, device: 2 was not an MTP device",
        "May 2 14:12:08 fargas systemd-udevd[408]: sda: Process '/usr/bin/unshare -m /usr/bin/snap auto-import --mount=/dev/sda' failed with exit code 1.",
        "May 2 14:12:08 fargas systemd-udevd[418]: Using default interface naming scheme 'v249'.",
        "May 2 14:12:08 fargas systemd-udevd[408]: sda1: Process '/usr/bin/unshare -m /usr/bin/snap auto-import --mount=/dev/sda1' failed with exit code 1.",
        "May 2 14:12:08 fargas systemd-udevd[418]: sda2: Process '/usr/bin/unshare -m /usr/bin/snap auto-import --mount=/dev/sda2' failed with exit code 1.",
        "May 2 14:12:08 fargas systemd[1]: Found device Virtual_disk EFI\\x20System\\x20Partition.",
        "May 2 14:12:08 fargas systemd[1]: Starting File System Check on /dev/disk/by-uuid/1FF4-1FA5...",
        "May 2 14:12:08 fargas systemd[1]: Started File System Check Daemon to report status.",
        "May 2 14:12:08 fargas systemd-fsck[502]: fsck.fat 4.2 (2021-01-31)",
        "May 2 14:12:08 fargas systemd-fsck[502]: /dev/sda2: 11 files, 1341/131063 clusters",
        "May 2 14:12:08 fargas systemd[1]: Finished File System Check on /dev/disk/by-uuid/1FF4-1FA5.",
        "May 2 14:12:08 fargas systemd[1]: Mounting /boot/efi...",
        "May 2 14:12:08 fargas systemd[1]: Mounted /boot/efi.",
        "May 2 14:12:08 fargas systemd[1]: Reached target Local File Systems.",
        "May 2 14:12:08 fargas systemd[1]: Starting Load AppArmor profiles...",
        "May 2 14:12:08 fargas systemd[1]: Starting Set console font and keymap...",
        "May 2 14:12:08 fargas systemd[1]: Starting Tell Plymouth To Write Out Runtime Data..."
    ]

    # Parse and print the log entries
    for log in log_entries:
        parsed_log = parse_syslog(log)
        print(parsed_log)
