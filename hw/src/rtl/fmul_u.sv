
module fmul_u
(
    input  wire              clk,
    input  complex_pkg::mac_t a,
    input  complex_pkg::mac_t b,
    output complex_pkg::mac_t c
);

logic signed [71:0] product;
always_comb product = $signed({{36{a[35]}}, a}) * $signed({{36{b[35]}}, b});

always_ff @(posedge clk) begin
    c <= product[67:32];
end

endmodule : fmul_u