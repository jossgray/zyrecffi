from cffi import FFI
import os, sys
ffi = FFI()

ffi.cdef('''

// zsock.h

typedef struct _zsock_t zsock_t;

// zmsg.h

typedef struct _zmsg_t zmsg_t;

int zmsg_addstr (zmsg_t* self, const char* string);

char* zmsg_popstr (zmsg_t* self);

// zyre.h

typedef struct _zyre_t zyre_t;

zyre_t* zyre_new (const char *name);

void zyre_destroy (zyre_t **self_p);

const char* zyre_uuid (zyre_t *self);

const char *zyre_name (zyre_t *self);

void zyre_set_header (zyre_t *self, const char *name, const char *format, ...);

void zyre_set_verbose (zyre_t *self);

void zyre_set_port (zyre_t *self, int port_nbr);

void zyre_set_interval (zyre_t *self, size_t interval);

void zyre_set_interface (zyre_t *self, const char *value);

int zyre_set_endpoint (zyre_t *self, const char *format, ...);

void zyre_gossip_bind (zyre_t *self, const char *format, ...);

void zyre_gossip_connect (zyre_t *self, const char *format, ...);

int zyre_start (zyre_t *self);

void zyre_stop (zyre_t *self);

int zyre_join (zyre_t *self, const char *group);

int zyre_leave (zyre_t *self, const char *group);

zmsg_t* zyre_recv (zyre_t *self);

int zyre_whisper (zyre_t *self, const char *peer, zmsg_t **msg_p);

int zyre_shout (zyre_t *self, const char *group, zmsg_t **msg_p);

int zyre_whispers (zyre_t *self, const char *peer, const char *format, ...);

int zyre_shouts (zyre_t *self, const char *group, const char *format, ...);

zsock_t* zyre_socket (zyre_t *self);

void zyre_dump (zyre_t *self);

void zyre_version (int *major, int *minor, int *patch);

void zyre_test (bool verbose);

// zhash.h

typedef struct _zhash_t zhash_t;

// zyre_event.h

typedef struct _zyre_event_t zyre_event_t;

typedef enum {
    ZYRE_EVENT_ENTER = 1,
    ZYRE_EVENT_JOIN = 2,
    ZYRE_EVENT_LEAVE = 3,
    ZYRE_EVENT_EXIT = 4,
    ZYRE_EVENT_WHISPER = 5,
    ZYRE_EVENT_SHOUT = 6
} zyre_event_type_t;

zyre_event_t* zyre_event_new (zyre_t *self);

void zyre_event_destroy (zyre_event_t **self_p);

zyre_event_type_t zyre_event_type (zyre_event_t *self);

char * zyre_event_sender (zyre_event_t *self);

char * zyre_event_name (zyre_event_t *self);

char * zyre_event_address (zyre_event_t *self);

char * zyre_event_header (zyre_event_t *self, char *name);

char * zyre_event_group (zyre_event_t *self);

zmsg_t * zyre_event_msg (zyre_event_t *self);

zhash_t * zyre_event_headers (zyre_event_t *self);

// zsys.h

const char * zsys_interface ();

// zsock_option.h

int zsock_fd (zsock_t *self);

// zpoller.h

typedef struct _zpoller_t zpoller_t;

zpoller_t * zpoller_new (void *reader, ...);

void zpoller_destroy (zpoller_t **self_p);

void * zpoller_wait (zpoller_t *self, int timeout);

int zpoller_add (zpoller_t *self, void *reader);
''')


os.environ['PATH'] = os.environ['PATH'] + ';' + os.path.abspath(os.path.join(os.path.dirname(__file__)))

_zyre_lib_name, _czmq_lib_name = 'zyre', 'czmq'
if sys.platform == 'win32':
    _zyre_lib_name, _czmq_lib_name = 'zyre.dll', 'czmq.dll'

zyre_lib = ffi.dlopen(_zyre_lib_name)
czmq_lib = ffi.dlopen(_czmq_lib_name)

new_int_ptr = lambda val: ffi.new('int*', val)
new_void_ptr = lambda val: ffi.new('void*', val)
c_string_to_py = lambda s: ffi.string(s) if s else None
check_null = lambda val: val if val else None