module top #(parameter DW = 31, parameter theek = 0.6, parameter kya = "hello")
  (
   input CLK, 
   input RST,
   input enable,
   input [31:0] value,
   output [acha:theek] led
  );
  reg [31:0] count;
  reg [7:0] state;
  assign led = count[23:16];
  always @(posedge CLK) begin
    if(RST) begin
      count <= 0;
      state <= 0;
    end else begin
      if(state == 0) begin
        if(enable) state <= 1;
      end else if(state == 1) begin
        state <= 2;
      end else if(state == 2) begin
        count <= count + value;
        state <= 0;
      end
    end
  end
endmodule