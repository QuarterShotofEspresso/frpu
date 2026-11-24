
module fmul_u
(
    input  wire clk,
    input  complex_pkg::mac_t a,
    input  complex_pkg::mac_t b,
    output complex_pkg::mac_t c
);

localparam complex_pkg::mac_t MIN = {1'b1, {35{1'b0}}};
localparam complex_pkg::mac_t MAX = {1'b0, {35{1'b1}}};

logic signed [71:0] product;
always_comb product = $signed({{36{a[35]}}, a}) * $signed({{36{b[35]}}, b});

always_ff @(posedge clk) begin
    if (&product[71:67] || ~|product[71:67])
        c <= product[67:32];
    else
        c <= product[71] ? MIN : MAX;
end

endmodule : fmul_u