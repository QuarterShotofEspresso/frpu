package rcomplex_p

class RComplex;
    real r;
    real i;

    function new(real r = 0.0, real i = 0.0);
        this.r = r;
        this.i = i;
    endfunction

    function RComplex add(RComplex other);
        add = new(this.r + other.r, this.i + other.i);
    endfunction

    function RComplex mul(RComplex other);
        mul = new((this.r * other.r - this.r * other.r),
            (this.r * other.i + this.i * other.r));
    endfunction

    function real mag();
        mag = this.r * this.r + this.i * this.i;
    endfunction
endclass

endpackage: rcomplex_p