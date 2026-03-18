/*
 * File Name:         hdl_prj\ipcore\rgb_filte_ip_v1_0\include\rgb_filte_ip_addr.h
 * Description:       C Header File
 * Created:           2025-03-25 10:25:07
*/

#ifndef RGB_FILTE_IP_H_
#define RGB_FILTE_IP_H_

#define  IPCore_Reset_rgb_filte_ip                          0x0  //write 0x1 to bit 0 to reset IP core
#define  IPCore_Enable_rgb_filte_ip                         0x4  //enabled (by default) when bit 0 is 0x1
#define  AXI4_Stream_Video_Slave_ImageWidth_rgb_filte_ip    0x8  //Active pixels per line in each video frame for "AXI4-Stream Video Slave" interface, the default value is 1920.
#define  AXI4_Stream_Video_Slave_ImageHeight_rgb_filte_ip   0xC  //Active video lines in each video frame for "AXI4-Stream Video Slave" interface, the default value is 1080.
#define  AXI4_Stream_Video_Slave_HPorch_rgb_filte_ip        0x10  //Horizontal porch length in each video frame for "AXI4-Stream Video Slave" interface, the default value is 280.
#define  AXI4_Stream_Video_Slave_VPorch_rgb_filte_ip        0x14  //Vertical porch length in each video frame for "AXI4-Stream Video Slave" interface, the default value is 45.
#define  IPCore_Timestamp_rgb_filte_ip                      0x18  //contains unique IP timestamp (yymmddHHMM): 2503251024
#define  red_Data_rgb_filte_ip                              0x100  //data register for Inport red
#define  green_Data_rgb_filte_ip                            0x104  //data register for Inport green
#define  blue_Data_rgb_filte_ip                             0x108  //data register for Inport blue

#endif /* RGB_FILTE_IP_H_ */
