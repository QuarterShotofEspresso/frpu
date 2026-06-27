
module fmul_u
    import complex_pkg::mac_t;
(
    input  wire  clk,
    input  mac_t a,
    input  mac_t b,
    output mac_t c
);

logic signed [71:0] product;
always_comb product = $signed({{36{a[35]}}, a}) * $signed({{36{b[35]}}, b});

always_ff @(posedge clk) begin
    c <= product[71:36];
end

endmodule : fmul_u