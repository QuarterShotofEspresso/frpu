`timescale 1ns/1ps

module mndl_tb;

localparam FALSE = 1'b0;
localparam TRUE  = 1'b1;
localparam int RESOL = 25;

logic clk;
logic rst_n;
logic valid;
input complex_pkg::complex_t c;

logic ready;
logic is_member;

// check if point c is a member of the mandelbrot set
function automatic compute_mandle(rcomplex_p::RComplex c);
    rcomplex_p::RComplex z = new(0.0, 0.0);
    for (int i = 0; i < RESOL; ++i) begin
        if (z.mag() > 4) return FALSE;
        z = z.mul(z).add(c);
    end
    return TRUE;
endfunction



task automatic check_value(real cr);

endtask



initial begin

end

endmodule