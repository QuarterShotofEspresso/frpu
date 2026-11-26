`timescale 1ns/1ps

module fpu_tb;

localparam int  FRAC = 32;
localparam real LSB  = 1.0 / (2.0 ** FRAC);
localparam real MAXR =  8.0 - LSB;
localparam real MINR = -8.0;

logic clk = 1'b0;
complex_pkg::mac_t a, b, c;
int errors = 0;
int tests  = 0;

fpu_u dut (.clk(clk), .a(a), .b(b), .c(c));

always #5 clk = ~clk;

function automatic complex_pkg::mac_t to_fx(real r);
    if (r > MAXR) r = MAXR;
    if (r < MINR) r = MINR;
    return complex_pkg::mac_t'(longint'(r * (2.0 ** FRAC)));
endfunction

function automatic real to_real(complex_pkg::mac_t x);
    return real'(x) / (2.0 ** FRAC);
endfunction

task automatic check(real x, real y);
    real expected, got;
    a = to_fx(x);
    b = to_fx(y);
    @(posedge clk);
    #1;
    expected = to_real(a) * to_real(b);
    if (expected > MAXR) expected = MAXR;
    if (expected < MINR) expected = MINR;
    got = to_real(c);
    tests++;
    if (got > expected + LSB || got < expected - LSB) begin
        $error("%f * %f: expected %.12f, got %.12f", x, y, expected, got);
        errors++;
    end
endtask

initial begin
    $dumpfile("build/fpu.vcd");
    $dumpvars(0, fpu_tb);

    a = '0; b = '0;
    @(posedge clk);

    check( 2.0,   2.0);
    check(-1.25, -1.25);
    check( 0.001, 0.001);
    check( 4.0,   4.0);
    check(-4.0,   4.0);

    repeat (1000)
        check((int'($urandom_range(0, 8000)) - 4000) / 1000.0,
              (int'($urandom_range(0, 8000)) - 4000) / 1000.0);

    if (errors == 0) $display("PASS: %0d tests", tests);
    else             $display("FAIL: %0d of %0d tests", errors, tests);
    $finish;
end

endmodule : fpu_tb
