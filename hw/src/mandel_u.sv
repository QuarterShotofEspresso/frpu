`include "fmul_u.sv"

typedef logic signed [17:0] mac_t;

typedef struct packed {
    mac_t r;
    mac_t i;
} complex_t;

module mandel_u (
    // Input Ports
    input wire rst_n,
    input wire clk,
    input complex_t c,

    output logic valid,
    output logic is_member
);

complex_t z;
logic [31:0] i;

fmul_u fmul_u_A (

);

initial begin
    z <= '0;
    i <= '0;
end

wire valid;
assign valid = (i < 25) && (result < 4);

mac_t result;

always_ff @(posedge clk) begin
    i <= (valid) ? i + 1 : 0;
end

always_ff @(posedge clk) begin

    zr_a <= (z.r * z.r);
    zi_a <= (z.i * z.i);
    zm_a <= (z.r * z.i) << 1;
    z_b  <= zr_a - zi_a;
    z.r  <= zr_a + c.r;
    z

    zra <= (z.creal * z.creal) - (z.cimag * z.cimag);
    zia <= (z.creal * z.cimag) << 1;

    z.creal <= zra + c.creal;
    z.cimag <= zia + c.cimag;

    result <= (z.creal * z.creal) + (z.cimag * z.cimag);

end

endmodule