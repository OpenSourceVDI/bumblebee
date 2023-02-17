from novaclient.v2 import servers as nova_servers

LINUX = "linux"

SCRIPT_ERROR = 0
SCRIPT_OKAY = 1

ERROR = -1

# These are Openstack Nova server status values that the
# python client library doesn't define constants for.
ACTIVE = "ACTIVE"
BUILD = "BUILD"
REBOOT = "REBOOT"
REBUILD = "REBUILD"
RESCUE = "RESCUE"
RESIZE = "RESIZE"
SHUTDOWN = "SHUTOFF"
VERIFY_RESIZE = "VERIFY_RESIZE"
MISSING = "MISSING"
# (There are more ...)

# These are Openstack Cinder status values that the
# python client library doesn't define constants for.
VOLUME_AVAILABLE = "available"
VOLUME_IN_USE = "in-use"
VOLUME_CREATING = "creating"
VOLUME_MAINTENANCE = "maintenance"

BACKUP_AVAILABLE = "available"
BACKUP_CREATING = "creating"
# (There are more ...)

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

LAUNCH_WAIT_SECONDS = 300

REBOOT_WAIT_SECONDS = 180
REBOOT_CONFIRM_WAIT_SECONDS = 10
REBOOT_CONFIRM_RETRIES = 5
REBOOT_COMPLETE_SECONDS = 60

RESIZE_WAIT_SECONDS = 240
RESIZE_CONFIRM_WAIT_SECONDS = 240

FORCED_DOWNSIZE_WAIT_SECONDS = 600
FORCED_SHELVE_WAIT_SECONDS = 600

SHELVE_WAIT_SECONDS = 180

ARCHIVE_WAIT_SECONDS = 18000
ARCHIVE_POLL_SECONDS = 60

CLOUD_INIT_FINISHED = "finished"
CLOUD_INIT_STARTED = "started"

DELETION_RETRY = 5
DELETION_TIMEOUT = 30
INSTANCE_DELETION_RETRY_WAIT_TIME = 30
INSTANCE_DELETION_RETRY_COUNT = 5
INSTANCE_CHECK_SHUTOFF_RETRY_WAIT_TIME = 10
INSTANCE_CHECK_SHUTOFF_RETRY_COUNT = 5
BACKUP_DELETION_RETRY_WAIT_TIME = 30
BACKUP_DELETION_RETRY_COUNT = 5
VOLUME_DELETION_RETRY_WAIT_TIME = 30
VOLUME_DELETION_RETRY_COUNT = 5

VOLUME_CREATION_TIMEOUT = 120
INSTANCE_LAUNCH_TIMEOUT = 120


# Workflow outcomes.  These are returned by function calls that
# (may) start workflows involving rqworker.  We will progressively
# switch to these (replacing True / False or other responses) starting
# with the workflows performed by the expirers.
#
# Workflow completed
WF_SUCCESS = 'succeeded'
# Workflow continues
WF_CONTINUE = 'continue'
# Workflow failed - retryable
WF_RETRY = 'failed_retryable'
# Workflow failed - non-retryable
WF_FAIL = 'failed'


# Button names

REBOOT_BUTTON = "REBOOT_BUTTON"
SHELVE_BUTTON = "SHELVE_BUTTON"
UNSHELVE_BUTTON = "UNSHELVE_BUTTON"
DELETE_BUTTON = "DELETE_BUTTON"
BOOST_BUTTON = "BOOST_BUTTON"
DOWNSIZE_BUTTON = "DOWNSIZE_BUTTON"
EXTEND_BUTTON = "EXTEND_BUTTON"
EXTEND_BOOST_BUTTON = "EXTEND_BOOST_BUTTON"
