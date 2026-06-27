
package complex_pkg;


typedef logic signed [35:0] mac_t;

typedef struct packed {
    mac_t r;
    mac_t i;
} complex_t;


endpackage: complex_pkg
