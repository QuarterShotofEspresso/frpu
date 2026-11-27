
module mndl_u (
    // Input Ports
    input wire rst_n,
    input wire clk,
    input wire valid,
    input complex_pkg::complex_t c,

    output logic ready,
    output logic is_member
);

localparam RESOLUTION = 25;

complex_pkg::complex_t z;
logic [31:0] i;
wire valid;
wire terminate;

complex_pkg::mac_t z_rr, z_ii, z_ri, length,
    z_r_prime, z_i_prime;


initial begin
    z = '0;
    i = '0;
end

fmul_u mul_rr
(
    .clk(clk),
    .a(z.r),
    .b(z.r),
    .c(z_rr)
);

fmul_u mul_ii
(
    .clk(clk),
    .a(z.i),
    .b(z.i),
    .c(z_ii)
);

fmul_u mul_ir
(
    .clk(clk),
    .a(z.i),
    .b(z.r),
    .c(z_ri)
);




assign length = z_rr + z_ii;
assign terminate = (length > 4) || (i >= RESOLUTION) || !ready;
assign is_member = (length > 4);


always_ff @(posedge clk) begin

    z_r_prime <= length + c.r;
    z_i_prime <= {{z_ri[34:0]}, 1'b0} + c.i;

    z.r <= z_r_prime;
    z.i <= z_i_prime;

end

endmodule