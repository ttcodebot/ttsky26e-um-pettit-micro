// render.v - dump frames of the demo as PPM files (plain Icarus, no cocotb):
//   see test/render/Makefile.  +UI=<n> sets ui_in, +T0=<n> the first frame's
//   frame count, +N=<n> the number of frames, +STEP=<n> frames skipped between.
`default_nettype none
`timescale 1ns / 1ps
module render;
  reg clk = 0, rst_n = 0;
  reg [7:0] ui_in = 0;
  wire [7:0] uo_out;
  tt_um_pettit_micro dut (.ui_in(ui_in), .uo_out(uo_out), .clk(clk), .rst_n(rst_n));
  always #20 clk = ~clk;

  wire hs = uo_out[7], vs = uo_out[3];
  wire [1:0] r = {uo_out[0], uo_out[4]}, g = {uo_out[1], uo_out[5]}, b = {uo_out[2], uo_out[6]};

  integer fd, n, t0, step, k, i, col, row, ui;
  reg [255:0] name;
  initial begin
    if (!$value$plusargs("UI=%d", ui)) ui = 0;
    if (!$value$plusargs("T0=%d", t0)) t0 = 0;
    if (!$value$plusargs("N=%d", n)) n = 1;
    if (!$value$plusargs("STEP=%d", step)) step = 16;
    ui_in = ui[7:0];
    repeat (4) @(posedge clk);
    rst_n = 1;
    for (k = 0; k < n; k = k + 1) begin
      @(negedge clk);
      // jump: start of frame k (the registered output lags the counters by one clock)
      force dut.hc = 0; force dut.vc = 0; force dut.t = t0 + k * step;
      @(negedge clk);
      release dut.hc; release dut.vc; release dut.t;
      $sformat(name, "frame_%0d_%0d.ppm", ui, k);
      fd = $fopen(name, "w");
      $fwrite(fd, "P3\n640 480\n3\n");
      for (row = 0; row < 480; row = row + 1) begin
        for (col = 0; col < 800; col = col + 1) begin
          if (col < 640) $fwrite(fd, "%0d %0d %0d\n", r, g, b);
          @(negedge clk);
        end
      end
      $fclose(fd);
    end
    $finish;
  end
endmodule
