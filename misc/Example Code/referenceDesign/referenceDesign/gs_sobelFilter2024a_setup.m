function gs_sobelFilter2024a_setup(hFPGA)
%--------------------------------------------------------------------------
% Host Interface Script Setup
% 
% Generated with MATLAB 24.1 (R2024a) at 16:50:29 on 05/03/2025.
% This function was created for the IP Core generated from design 'sobelFilter2024a'.
% 
% Run this function on an "fpga" object to configure it with the same interfaces as the generated IP core.
%--------------------------------------------------------------------------

%% AXI4-Lite
addAXI4SlaveInterface(hFPGA, ...
	"InterfaceID", "AXI4-Lite", ...
	"BaseAddress", 0x43C60000, ...
	"AddressRange", 0x10000);


end
