from novaclient.v2 import servers as nova_servers

LINUX = "linux"

SCRIPT_ERROR = 0
SCRIPT_OKAY = 1

ERROR = -1

ACTIVE = "ACTIVE"
SHUTDOWN = "SHUTOFF"
VERIFY_RESIZE = "VERIFY_RESIZE"
RESIZE = "RESIZE"

NO_VM = VM_DELETED = "No_VM"
VM_WAITING = VM_CREATING = VM_RESIZING = "VM_Waiting"
VM_OKAY = "VM_Okay"
VM_SUPERSIZED = "VM_Supersized"
VM_SHELVED = "VM_Shelved"
VM_ERROR = "VM_Error"
VM_MISSING = "VM_Missing"
VM_SHUTDOWN = "VM_Shutdown"

ALL_VM_STATES = frozenset([NO_VM, VM_WAITING, VM_OKAY, VM_SUPERSIZED,
                           VM_SHELVED, VM_ERROR, VM_MISSING, VM_SHUTDOWN])

REBOOT_SOFT = nova_servers.REBOOT_SOFT
REBOOT_HARD = nova_servers.REBOOT_HARD

LAUNCH_WAIT_SECONDS = 300  # Five minutes
REBOOT_WAIT_SECONDS = 180  # Three minutes
REBOOT_CONFIRM_WAIT_SECONDS = 120  # Two minutes
RESIZE_WAIT_SECONDS = 120  # Five minutes
RESIZE_CONFIRM_WAIT_SECONDS = 240  # Four minutes
SHELVE_WAIT_SECONDS = 180  # Three minutes

CLOUD_INIT_FINISHED = "finished"
CLOUD_INIT_STARTED = "started"

DELETION_RETRY = 5
DELETION_TIMEOUT = 30
INSTANCE_DELETION_RETRY_WAIT_TIME = 30
INSTANCE_DELETION_RETRY_COUNT = INSTANCE_CHECK_SHUTOFF_RETRY_COUNT = 2
INSTANCE_CHECK_SHUTOFF_RETRY_WAIT_TIME = 10

VOLUME_CREATION_TIMEOUT = 30

DOWNSIZE_PERIOD = 7  # Number of days before downsizing.

REBOOT_BUTTON = "REBOOT_BUTTON"
SHELVE_BUTTON = "SHELVE_BUTTON"
DELETE_BUTTON = "DELETE_BUTTON"
BOOST_BUTTON = "BOOST_BUTTON"
DOWNSIZE_BUTTON = "DOWNSIZE_BUTTON"
