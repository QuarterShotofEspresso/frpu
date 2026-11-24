
module top
(
    /** Input Ports */
    input wire                    clk,
    input complex_pkg::complex_t  z,
    /** Output Ports */
    output complex_pkg::complex_t r
);


fmul_u fmul_inst_1 (
    .clk(clk),
    .a(z.r),
    .b(z.r),
    .c(r.r)
);

// fmul_u fmul_inst_2 (

// );

endmodule