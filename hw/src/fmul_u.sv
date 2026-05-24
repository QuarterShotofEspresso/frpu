module fmul_u (
    input  wire clk,
    input  logic signed [35:0] a,
    input  logic signed [35:0] b,
    output logic signed [35:0] c
);

always_ff @(posedge clk) begin
    c <= (a * b)[71:36];
end

endmodule