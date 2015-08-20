import socket
import time

from cloudbot import hook
from plugins.usingBot import getTokens, takeTokens


def scanport(IP, PORT):
	time.sleep(0.005)
	# noinspection PyBroadException
	try:
		s = socket.socket()
		s.connect((IP, PORT))
		return True
	except:
		return False


@hook.command("portscan1", "ps1", "scan1")
def scanOne(reply, text, nick, notice):
	if getTokens(nick) < 1000:
		notice("You don't have enough tokens to do a portscan... Help a little more !")
		return None

	args = text.split()

	try:
		IP = str(args[0])
		PORT = int(args[1])
	except IndexError:
		notice("Syntaxe : !ps1 IP PORT. Utilisez !ps3000 pour les 3000 ports les plus utilisés")
		return None

	takeTokens(10, nick, notice)
	socket.setdefaulttimeout(2)
	reply("Scanning port number " + str(PORT) + " for ip " + str(IP))

	result = scanport(IP, PORT)

	if result:
		reply("Le port " + str(PORT) + " de l'IP " + IP + " est OUVERT !")
	elif not result:
		reply("Le port " + str(PORT) + " de l'IP " + IP + " est FERMÉ ! ")



@hook.command("scan3000", "portscan3000", "ps3000")
def scan3000(reply, text, nick, notice):
	if getTokens(nick) < 1000:
		notice("You don't have enough tokens to do a portscan... Help a little more !")
		return None

	takeTokens(100, nick, notice)
	IP = text
	openPorts = []
	socket.setdefaulttimeout(2)
	reply("Scanning 3000 ports... May take a little bit of a time (1-2 minutes) :x")

	toScan = [80, 23, 443, 21, 22, 25, 3389, 110, 445, 139, 143, 53, 135, 3306, 8080, 1723, 111, 995, 993, 5900, 1025,
			  587, 8888, 199, 1720, 465, 548, 113, 81, 6001, 10000, 514, 5060, 179, 1026, 2000, 8443, 8000, 32768, 554,
			  26, 1433, 49152, 2001, 515, 8008, 49154, 1027, 5666, 646, 5000, 5631, 631, 49153, 8081, 2049, 88, 79,
			  5800, 106, 2121, 1110, 49155, 6000, 513, 990, 5357, 427, 49156, 543, 544, 5101, 144, 7, 389, 8009, 3128,
			  444, 9999, 5009, 7070, 5190, 3000, 5432, 3986, 1900, 13, 1029, 9, 6646, 5051, 49157, 1028, 873, 1755,
			  2717, 4899, 9100, 119, 37, 1000, 3001, 5001, 82, 10010, 1030, 9090, 2107, 1024, 2103, 6004, 1801, 5050,
			  19, 8031, 1041, 255, 3703, 2967, 1065, 1064, 1056, 1054, 1053, 1049, 1048, 17, 808, 3689, 1031, 1071,
			  1044, 5901, 9102, 100, 9000, 8010, 5120, 4001, 2869, 1039, 2105, 636, 1038, 2601, 7000, 1, 1069, 1066,
			  625, 311, 280, 254, 4000, 5003, 1761, 2002, 2005, 1998, 1032, 1050, 6112, 3690, 1521, 2161, 6002, 1080,
			  2401, 902, 4045, 7937, 787, 1058, 2383, 32771, 1059, 1040, 1033, 50000, 5555, 10001, 1494, 593, 3, 2301,
			  7938, 3268, 1234, 1022, 9001, 8002, 1074, 1037, 1036, 1035, 464, 6666, 497, 2003, 1935, 6543, 24, 1352,
			  3269, 1111, 500, 407, 20, 2006, 3260, 15000, 1218, 1034, 4444, 264, 33, 2004, 42510, 1042, 999, 3052,
			  1023, 222, 1068, 888, 7100, 563, 1717, 992, 32770, 2008, 7001, 32772, 8082, 2007, 5550, 5801, 512, 2009,
			  1043, 7019, 50001, 2701, 1700, 4662, 2065, 42, 2010, 9535, 3333, 2602, 161, 5100, 5002, 4002, 2604, 9595,
			  9594, 9593, 9415, 8701, 8652, 8651, 8194, 8193, 8192, 8089, 6789, 65389, 65000, 64680, 64623, 6059, 55600,
			  55555, 52869, 5226, 5225, 4443, 35500, 33354, 3283, 32769, 2702, 23502, 20828, 16993, 16992, 1311, 1062,
			  1060, 1055, 1052, 1051, 1047, 13782, 1067, 5902, 366, 9050, 85, 5500, 1002, 8085, 5431, 51103, 49999,
			  45100, 1864, 1863, 10243, 49, 90, 6667, 6881, 27000, 1503, 8021, 340, 1500, 9071, 8899, 8088, 5566, 2222,
			  9876, 9101, 6005, 5102, 32774, 32773, 1501, 5679, 163, 648, 1666, 146, 901, 83, 9207, 8084, 8083, 8001,
			  5214, 5004, 3476, 14238, 912, 30, 12345, 2605, 2030, 6, 541, 8007, 4, 3005, 1248, 880, 306, 2500, 9009,
			  8291, 52822, 4242, 2525, 1097, 1088, 1086, 900, 6101, 7200, 2809, 987, 800, 32775, 211, 12000, 1083, 705,
			  711, 20005, 6969, 13783, 9968, 9900, 9618, 9503, 9502, 9500, 9485, 9290, 9220, 9080, 9011, 9010, 9002,
			  8994, 8873, 8649, 8600, 8402, 8400, 8333, 8222, 8181, 8087, 8086, 7911, 7778, 7777, 7741, 7627, 7625,
			  7106, 6901, 6788, 6580, 65129, 6389, 63331, 6156, 6129, 6123, 60020, 5989, 5988, 5987, 5962, 5961, 5960,
			  5959, 5925, 5911, 5910, 5877, 5825, 5810, 58080, 57294, 5718, 5633, 5414, 5269, 5222, 50800, 5030, 50006,
			  50003, 49160, 49159, 49158, 48080, 4449, 4129, 4126, 40193, 4003, 3998, 3827, 3801, 3784, 3766, 3659,
			  3580, 3551, 34573, 34572, 34571, 3404, 33899, 3367, 3351, 3325, 3323, 3301, 3300, 32782, 32781, 3211,
			  31038, 30718, 3071, 3031, 3017, 30000, 2875, 28201, 2811, 27715, 2718, 2607, 25734, 2492, 24800, 2399,
			  2381, 22939, 2260, 2190, 2160, 21571, 2144, 2135, 2119, 2100, 20222, 20221, 20031, 20000, 19842, 19801,
			  1947, 19101, 1840, 17988, 1783, 1718, 1687, 16018, 16016, 16001, 15660, 15003, 15002, 14442, 14000, 13456,
			  1310, 1272, 11967, 1169, 1148, 11110, 1108, 1107, 1106, 1104, 1100, 1099, 1098, 1096, 1094, 1093, 1085,
			  1082, 1081, 1079, 1078, 1077, 1075, 1073, 1072, 1070, 1063, 10629, 10628, 10626, 10621, 10617, 10616,
			  1061, 1057, 10566, 1046, 1045, 10025, 10024, 10012, 10002, 89, 691, 32776, 212, 2020, 1999, 1001, 7002,
			  6003, 50002, 2998, 898, 5510, 3372, 32, 2033, 99, 749, 5903, 425, 7007, 6502, 6106, 5405, 458, 43, 13722,
			  9998, 9944, 9943, 9877, 9666, 9110, 9091, 8654, 8500, 8254, 8180, 8100, 8090, 8011, 7512, 7443, 7435,
			  7402, 7103, 62078, 61900, 61532, 5963, 5922, 5915, 5904, 5859, 5822, 56738, 55055, 5298, 5280, 5200,
			  51493, 50636, 5054, 50389, 49175, 49165, 49163, 4446, 4111, 4006, 3995, 3918, 3880, 3871, 3851, 3828,
			  3737, 3546, 3493, 3371, 3370, 3369, 32784, 3261, 3077, 3030, 3011, 27355, 27353, 27352, 2522, 24444, 2251,
			  2191, 2179, 2126, 19780, 19315, 19283, 18988, 1782, 16012, 1580, 15742, 1334, 1296, 1247, 1186, 1183,
			  1152, 1124, 1089, 1087, 10778, 10004, 9040, 32779, 32777, 1021, 700, 666, 616, 32778, 2021, 84, 5802, 545,
			  49400, 4321, 38292, 2040, 1524, 1112, 32780, 3006, 2111, 2048, 1600, 1084, 9111, 6699, 6547, 2638, 16080,
			  801, 720, 667, 6007, 5560, 555, 2106, 2034, 1533, 1443, 9917, 9898, 9878, 9575, 9418, 9200, 9099, 9081,
			  9003, 8800, 8383, 8300, 8292, 8290, 8200, 8099, 8093, 8045, 8042, 8022, 7999, 7921, 7920, 7800, 7676,
			  7496, 7025, 6839, 6792, 6779, 6692, 6689, 6567, 6566, 6565, 6510, 6100, 60443, 6025, 5952, 5950, 5907,
			  5906, 5862, 5850, 5815, 5811, 57797, 5730, 5678, 56737, 5544, 55056, 5440, 54328, 54045, 52848, 52673,
			  5221, 5087, 5080, 5061, 50500, 5033, 50300, 49176, 49167, 49161, 4900, 4848, 4567, 4550, 44501, 4445,
			  44176, 4279, 41511, 40911, 4005, 4004, 3971, 3945, 3920, 3914, 3905, 3889, 3878, 3869, 3826, 3814, 3809,
			  3800, 3527, 3517, 3390, 3324, 3322, 32785, 32783, 3221, 3168, 30951, 3003, 2909, 27356, 2725, 26214, 2608,
			  25735, 2394, 2393, 2323, 19350, 1862, 18101, 18040, 17877, 16113, 16000, 15004, 14441, 1271, 12265, 12174,
			  1201, 1199, 1175, 1151, 1138, 1131, 1122, 1119, 1117, 1114, 11111, 1091, 1090, 10215, 10180, 10009, 10003,
			  981, 777, 722, 714, 70, 6346, 617, 4998, 4224, 417, 2022, 1009, 765, 668, 5999, 524, 301, 2041, 1076,
			  10082, 7004, 6009, 44443, 4343, 416, 259, 2068, 2038, 1984, 1434, 1417, 1007, 911, 9103, 726, 7201, 687,
			  6006, 4125, 2046, 2035, 1461, 109, 1010, 903, 683, 6669, 6668, 481, 2047, 2043, 2013, 1455, 125, 1011,
			  9929, 843, 783, 5998, 44442, 406, 31337, 256, 2045, 2042, 9988, 9941, 9914, 9815, 9673, 9643, 9621, 9600,
			  9501, 9444, 9443, 9409, 9198, 9197, 9191, 9098, 8996, 8987, 8889, 8877, 8766, 8765, 8686, 8676, 8675,
			  8648, 8540, 8481, 8385, 8294, 8293, 8189, 8098, 8097, 8095, 8050, 8019, 8016, 8015, 7929, 7913, 7900,
			  7878, 7770, 7749, 7744, 7725, 7438, 7281, 7278, 7272, 7241, 7123, 7080, 7051, 7050, 7024, 6896, 6732,
			  6711, 6600, 6550, 65310, 6520, 6504, 6500, 6481, 6247, 6203, 61613, 6068, 60642, 6060, 6051, 60146, 60123,
			  5981, 5968, 5940, 5938, 59202, 59201, 59200, 5918, 5914, 59110, 5909, 5905, 5899, 58838, 5869, 5868,
			  58632, 58630, 5823, 5818, 5812, 5807, 58002, 58001, 57665, 55576, 55020, 5501, 53535, 5353, 5339, 53314,
			  53313, 53211, 52853, 52851, 52850, 52849, 52847, 5279, 52735, 52710, 52660, 5242, 5223, 5212, 5151, 51413,
			  51191, 5081, 5074, 5063, 5040, 50050, 4949, 49401, 49236, 49195, 49186, 49171, 49168, 49164, 4875, 47544,
			  46996, 4658, 46200, 4600, 4555, 44709, 4430, 4252, 4200, 4164, 41523, 4147, 4143, 41064, 4096, 40811,
			  4080, 4040, 4009, 40000, 3994, 3993, 3990, 3981, 3972, 3969, 3968, 39659, 3963, 3957, 3944, 3941, 39376,
			  3931, 3929, 3916, 39136, 3907, 3888, 3872, 3870, 3863, 3859, 3853, 3852, 3849, 3848, 3846, 3824, 3820,
			  38188, 38185, 3808, 3792, 37839, 3731, 3700, 3697, 3684, 35513, 3514, 3410, 3400, 3376, 33554, 33453,
			  3307, 3304, 32835, 32822, 32816, 32803, 32792, 32791, 31727, 3162, 3119, 30704, 3050, 3013, 3007, 30005,
			  29831, 2968, 29672, 2920, 2910, 28211, 2800, 27357, 2710, 26470, 26000, 2557, 2382, 23796, 2366, 23052,
			  2288, 22222, 2200, 2196, 21792, 2170, 2099, 20002, 19900, 1974, 1972, 1971, 1914, 1875, 1839, 18264, 1812,
			  1805, 18018, 17595, 1721, 1719, 1688, 16851, 16800, 16705, 1658, 1641, 1594, 1583, 1556, 15402, 15001,
			  13724, 1328, 1322, 1309, 1301, 1300, 1287, 1277, 1259, 12452, 1244, 12380, 1236, 1233, 12262, 12215, 1217,
			  1216, 1213, 12059, 12021, 12006, 1198, 1192, 1187, 1185, 1174, 1166, 1165, 1164, 1163, 1154, 1149, 1147,
			  1145, 1141, 1137, 1132, 1130, 1126, 1123, 1121, 1113, 1105, 1102, 1095, 1092, 10873, 10160, 10058, 10034,
			  10023, 10022, 10011, 10008, 930, 913, 803, 780, 725, 710, 701, 639, 623, 6222, 5680, 502, 4559, 2501,
			  2241, 2232, 2012, 1347, 1220, 1109, 1103, 10005, 9992, 953, 931, 874, 86, 856, 8118, 540, 5010, 475, 447,
			  442, 441, 419, 27, 250, 2044, 18000, 1270, 123, 1222, 1158, 102, 980, 9152, 87, 829, 713, 709, 7003, 6103,
			  6008, 5803, 57, 556, 5520, 55, 3299, 3025, 2628, 251, 2433, 223, 210, 1550, 1212, 1013, 10083, 1008, 943,
			  904, 840, 825, 792, 77, 748, 732, 7010, 684, 674, 657, 610, 557, 523, 4333, 333, 220, 2067, 2011, 157,
			  1547, 1526, 1516, 1351, 1350, 127, 1241, 1020, 1006, 998, 996, 971, 969, 905, 862, 846, 839, 823, 822,
			  795, 790, 786, 782, 778, 757, 731, 730, 729, 6662, 660, 659, 655, 6050, 602, 600, 3632, 3456, 3399, 2903,
			  257, 225, 2201, 2025, 1522, 1357, 1353, 1015, 1014, 1012, 98, 928, 924, 922, 921, 918, 878, 864, 859, 806,
			  805, 802, 758, 754, 740, 728, 715, 690, 669, 6670, 641, 621, 606, 6017, 59, 5011, 44334, 411, 3999, 388,
			  38037, 2600, 252, 2112, 1525, 1414, 1413, 1337, 12346, 1127, 1005, 1004, 9995, 9990, 9979, 9975, 9971,
			  9950, 9919, 9915, 9912, 9911, 9910, 9909, 9908, 9901, 9875, 9844, 9830, 9826, 9825, 9823, 9814, 9812,
			  9777, 9745, 9700, 9694, 9683, 9680, 9679, 9674, 9667, 9665, 9661, 9654, 9648, 9628, 9620, 9619, 9616,
			  9613, 9592, 9583, 9527, 9513, 9493, 9478, 9464, 9454, 9400, 9364, 9351, 9343, 9300, 9287, 9211, 9210,
			  9202, 9183, 9170, 9161, 9160, 9133, 9131, 9130, 9128, 9125, 9084, 9065, 9061, 9044, 9037, 9022, 9021,
			  9020, 9013, 9005, 9004, 8999, 8980, 8954, 8925, 8900, 8898, 8887, 8882, 8880, 8879, 8878, 8865, 8843,
			  8801, 8798, 8790, 8772, 8756, 8752, 8736, 8680, 8673, 8658, 8655, 8644, 8640, 8621, 8601, 8562, 8539,
			  8531, 8530, 8515, 8484, 8479, 8477, 8474, 8472, 8471, 8470, 8455, 8454, 8453, 8452, 8451, 8445, 8409,
			  8403, 8401, 8339, 8308, 8295, 8282, 8273, 8268, 8255, 8248, 8245, 8232, 8202, 8201, 8144, 8133, 8116,
			  8110, 8092, 8064, 8060, 8052, 8037, 8029, 8025, 8023, 8018, 8014, 8006, 8005, 8003, 7998, 7975, 7895,
			  7854, 7853, 7852, 7830, 7813, 7789, 7788, 7780, 7772, 7771, 7688, 7685, 7654, 7637, 7628, 7600, 7555,
			  7553, 7501, 7500, 7456, 7451, 7400, 7345, 7325, 7320, 7300, 7231, 7218, 7184, 7121, 7119, 7104, 7102,
			  7101, 7099, 7092, 7072, 7071, 7068, 7067, 7043, 7033, 6973, 6972, 6956, 6942, 6922, 6920, 6897, 6888,
			  6877, 6780, 6734, 6725, 6710, 6709, 6650, 6647, 6644, 6628, 6606, 6579, 65514, 65488, 6535, 65311, 65048,
			  6503, 64890, 64727, 64726, 64551, 64507, 64438, 64320, 64127, 6412, 64080, 63803, 63675, 6350, 6349,
			  63423, 6324, 6323, 63156, 63105, 6310, 6309, 62866, 6274, 6273, 62674, 6259, 62570, 62519, 6251, 6250,
			  62312, 62188, 62080, 62042, 62006, 61942, 61851, 61827, 61734, 61722, 61669, 61617, 61616, 6161, 61516,
			  61473, 61402, 6126, 6120, 61170, 61169, 61159, 6115, 6113, 60989, 6091, 6090, 6085, 60794, 60789, 60783,
			  60782, 6077, 60753, 60743, 60728, 60713, 6067, 6065, 6063, 60628, 60621, 6062, 60612, 60579, 6055, 60544,
			  6052, 60504, 60492, 60485, 60403, 60401, 60377, 6030, 60279, 60243, 60227, 6021, 60177, 6015, 60111, 6010,
			  60086, 60055, 60003, 60002, 60000, 59987, 59841, 59829, 59810, 59778, 5975, 5974, 5971, 5969, 59684, 5966,
			  5958, 59565, 5954, 5953, 59525, 59510, 59509, 59504, 59499, 5949, 5948, 5945, 5939, 5936, 59340, 5934,
			  5931, 5927, 5926, 5924, 59239, 5923, 5921, 5920, 59191, 5917, 59160, 59149, 59122, 5912, 59107, 59087,
			  5908, 58991, 58970, 58908, 5888, 5887, 5881, 5878, 5875, 5874, 58721, 5871, 58699, 58634, 58622, 58610,
			  5860, 5858, 58570, 58562, 5854, 5853, 5852, 58498, 5849, 5848, 58468, 58456, 5845, 58446, 58430, 5840,
			  5839, 5838, 58374, 5836, 5834, 58310, 5831, 58305, 5827, 5826, 58252, 5824, 5821, 5820, 5817, 58164, 5814,
			  58109, 58107, 5808, 58072, 5806, 5804, 57999, 57988, 57928, 57923, 57896, 57891, 57733, 57730, 57702,
			  57681, 57678, 57576, 57479, 57398, 57387, 5737, 57352, 57350, 57347, 5734, 57335, 57325, 5732, 5723, 5722,
			  5721, 57123, 5711, 57103, 57020, 56975, 56973, 56827, 56822, 56810, 56725, 56723, 5672, 56681, 5667,
			  56668, 5665, 56591, 56535, 56507, 56293, 56259, 5622, 5621, 5620, 5612, 5611, 56055, 56016, 55948, 55910,
			  55907, 55901, 5581, 5580, 55781, 55773, 55758, 55721, 55684, 55652, 55635, 55579, 5557, 55569, 55568,
			  55556, 5554, 5553, 55527, 5552, 55479, 55426, 55400, 55382, 55350, 55312, 55227, 55187, 55183, 5502,
			  55000, 54991, 54987, 54907, 54873, 5475, 54741, 5473, 54722, 54688, 54658, 54605, 5458, 5457, 54551,
			  54514, 5444, 5442, 5441, 5433, 54323, 54321, 54276, 54263, 54235, 5423, 54127, 54101, 54075, 53958, 53910,
			  53852, 53827, 53782, 5377, 53742, 5370, 53690, 53656, 53639, 53633, 53491, 5347, 53469, 53460, 53370,
			  53361, 53319, 53240, 53212, 53189, 53178, 53085, 52948, 5291, 52893, 52675, 52665, 5261, 5259, 52573,
			  5252, 52506, 5250, 52477, 52391, 5235, 5234, 5233, 52262, 52237, 52230, 52226, 52225, 5219, 52173, 52071,
			  52046, 52025, 5202, 5201, 52003, 52002, 52001, 52000, 51965, 51961, 51909, 51906, 51809, 51800, 51772,
			  51771, 51658, 51582, 5152, 51515, 51488, 51485, 51484, 5147, 51460, 51423, 5137, 51366, 51351, 51343,
			  5133, 51300, 5125, 51240, 51235, 51234, 51233, 5122, 5121, 5114, 51139, 51118, 5111, 51067, 51037, 51020,
			  51011, 50997, 5098, 5096, 5095, 50945, 50903, 5090, 50887, 5088, 50854, 50849, 50836, 50835, 50834, 50833,
			  50831, 50815, 50809, 50787, 50733, 5070, 50692, 5066, 50585, 50577, 50576, 5055, 50545, 5053, 50529, 5052,
			  50513, 50356, 50277, 50258, 50246, 5023, 50224, 5021, 50205, 50202, 5020, 50198, 50189, 5017, 5016, 5015,
			  5014, 5013, 5012, 50101, 5005, 50040, 50019, 50016, 4999, 49927, 49803, 49765, 49762, 49751, 49678, 49603,
			  49597, 49522, 49521, 49520, 49519, 49500, 49498, 49452, 49398, 49372, 49352, 4931, 49302, 49275, 49241,
			  49235, 49232, 49228, 49216, 49213, 49211, 49204, 49203, 49202, 49201, 49197, 49196, 49191, 49190, 49189,
			  49179, 49173, 49172, 49170, 49169, 49166, 49132, 4912, 49048, 4903, 49002, 48973, 48967, 48966, 48925,
			  48813, 4881, 48783, 4877, 4876, 48682, 48648, 48631, 48619, 4860, 4859, 48434, 48356, 4819, 48167, 48153,
			  48127, 48083, 48067, 48009, 4800, 47969, 47966, 4793, 47860, 47858, 47850, 47806, 4778, 47777, 4771,
			  47700, 4770, 4767, 47634, 47624, 4760, 47595, 47581, 47567, 4745, 47448, 47372, 47348, 47267, 47197, 4712,
			  47119, 47029, 47012, 4700, 46992, 4689, 4687, 46813, 4665, 46593, 4649, 4644, 46436, 46418, 46372, 46310,
			  46182, 46171, 46115, 4609, 46069, 4606, 46034, 4602, 4601, 4599, 45960, 45864, 45777, 4570, 45697, 45624,
			  45602, 4558, 45463, 4545, 45438, 45413, 4534, 4530, 45226, 45220, 4517, 45164, 4516, 45136, 45050, 45038,
			  44981, 44965, 4476, 44711, 4471, 44704, 4464, 44628, 44616, 44541, 4454, 44505, 44479, 4447, 44431, 4442,
			  44410, 44380, 4433, 44200, 4418, 4415, 4414, 44119, 44101, 4407, 4401, 44004, 4388, 43868, 4384, 43823,
			  4376, 4375, 4374, 43734, 43690, 4369, 43654, 4358, 4357, 4356, 4355, 43425, 4342, 4328, 4325, 43242,
			  43231, 43212, 43143, 43139, 43103, 43027, 4302, 43018, 43002, 43000, 4300, 42990, 4298, 4297, 4294, 42906,
			  42735, 42685, 42679, 42675, 42632, 4262, 42590, 42575, 42560, 42559, 42452, 42449, 4234, 42322, 42276,
			  42251, 4220, 42158, 42127, 4206, 42035, 42001, 4192, 4190, 41808, 41795, 41794, 41773, 4174, 41632, 4161,
			  4158, 41551, 41442, 4141, 41398, 4135, 41348, 41345, 41342, 41318, 41281, 41250, 4121, 4120, 4119, 4118,
			  41142, 4113, 41123, 4112, 4101, 4100, 40951, 4090, 4087, 40834, 40812, 40754, 40732, 40712, 4065, 40628,
			  40614, 4058, 4056, 40513, 40489, 40457, 40400, 40393, 4039, 4036, 4035, 40306, 4029, 4025, 4024, 4022,
			  4020, 4016, 4010, 4007, 40011, 40005, 40003, 40002, 40001, 3997, 3996, 3992, 39917, 3991, 39895, 3989,
			  39883, 39869, 3983, 3982, 3980, 39795, 3979, 39774, 39763, 3975, 39732, 3967, 3964, 39630, 3962, 3961,
			  3956, 3952, 3949, 39489, 39482, 3948, 3946, 39433, 3943, 3940, 39380, 3937, 3936, 3935, 3930, 39293, 3928,
			  39265, 3923, 3922, 3919, 3915, 3913, 39117, 3911, 3909, 3908, 39067, 3906, 3904, 3902, 3901, 3899, 3897,
			  38936, 3890, 3882, 38805, 3879, 38780, 38764, 38761, 3876, 3868, 3860, 38570, 38561, 3856, 38546, 3850,
			  38481, 3847, 38446, 3842, 3839, 3837, 38358, 38331, 38313, 3831, 3830, 38270, 3825, 3823, 38224, 38205,
			  38194, 3817, 3813, 3812, 3811, 3810, 3806, 3803, 38029, 3799, 3798, 3796, 3795, 3793, 3790, 3788, 3787,
			  37855, 37789, 37777, 37674, 3765, 37647, 37614, 37607, 37522, 3749, 3742, 37393, 3728, 37218, 37185,
			  37174, 37151, 37121, 3712, 36983, 36962, 36950, 36914, 3683, 36824, 36823, 3681, 3680, 36748, 3672, 36710,
			  3670, 36694, 3669, 36677, 36659, 3663, 3658, 3656, 36552, 36530, 3653, 3652, 36508, 36436, 3637, 36368,
			  3636, 36275, 36256, 3622, 3621, 36105, 36104, 36046, 3603, 3602, 3600, 3599, 35986, 35929, 35906, 35901,
			  35900, 35879, 3586, 3577, 35731, 35593, 35553, 35506, 35401, 35393, 35392, 35349, 3532, 3530, 35272, 3526,
			  35217, 3520, 3519, 3515, 35131, 3513, 35116, 3511, 3506, 35050, 3505, 35033, 3503, 3497, 34875, 3486,
			  3485, 34833, 3483, 3479, 34783, 34765, 34728, 34683, 34510, 34507, 3443, 34401, 3439, 34381, 34341, 34317,
			  3430, 3425, 3419, 34189, 3415, 3414, 34096, 34036, 34021, 3396, 33895, 33889, 33882, 3388, 33879, 33841,
			  3374, 3368, 3365, 3363, 3362, 33605, 33604, 33550, 33523, 33522, 33444, 33395, 33367, 3334, 33337, 33335,
			  33327, 33277, 33203, 33200, 33192, 3319, 33175, 33124, 3311, 3310, 33087, 33070, 33017, 33011, 33000,
			  32976, 32961, 32960, 32944, 32932, 32911, 32910, 3291, 32908, 32905, 32904, 32898, 32897, 32888, 32871,
			  32869, 32868, 32858, 32842, 32837, 32820, 32815, 32814, 3281, 32807, 3280, 32799, 32798, 32797, 32790,
			  32789, 32788, 32767, 32765, 32764, 3263, 3240, 32261, 32260, 32219, 32200, 3220, 32102, 3210, 32088,
			  32031, 32022, 32006, 3200, 3190, 31728, 3167, 31657, 31522, 3146, 31438, 31386, 31339, 3121, 3118, 31072,
			  31058, 31033, 3103, 3102, 30896, 3089, 3080, 30705, 30659, 30644, 3063, 3062, 30599, 3057, 30519, 30299,
			  3023, 30195, 3014, 30087, 3002, 30001, 2997, 2991, 2988, 2987, 2984, 29810, 2973, 2958, 2957, 29507, 2930,
			  29243, 29152, 2908, 29045, 2902, 2901, 2898, 28967, 28924, 2889, 2888, 28851, 28850, 2882, 28717, 28567,
			  2850, 2847, 28374, 28142, 2812, 28114, 2806, 2804, 27770, 27537, 27521, 27372, 27351, 27350, 2734, 27316,
			  2728, 2723, 27204, 2712, 2711, 27087, 27075, 27074, 2706, 27055, 27016, 27015, 2700, 26972, 2691, 26669,
			  2644, 26417, 26340, 2631, 2623, 2622, 2606, 26007, 26001, 2598, 25847, 2584, 2583, 2580, 25717, 25703,
			  2567, 2558, 25565, 2551, 2550, 25486, 25473, 25445, 25327, 2532, 2531, 25288, 25262, 25260, 25174, 2505,
			  25001, 25000, 24999, 2472, 2463, 24616, 2456, 24554, 24552, 2449, 24416, 24392, 2439, 2438, 2436, 2435,
			  2425, 24218, 2418, 23953, 2391, 23887, 23723, 2372, 2371, 23451, 23430, 2340, 23382, 2335, 23342, 2330,
			  23296, 23270, 2326, 2325, 23228, 23219, 2313, 2312, 23040, 2304, 2302, 23017, 2300, 22969, 22959, 2292,
			  2291, 22882, 2280, 22769, 22727, 22719, 22711, 2271, 2270, 2269, 2265, 2262, 2261, 22563, 22555, 2253,
			  2250, 22350, 22341, 22290, 2224, 22223, 22200, 22177, 22128, 22125, 22100, 22063, 2203, 22022, 2197,
			  21915, 21891, 2187, 21728, 21634, 21631, 2150, 2148, 21473, 2142, 2134, 2124, 2115, 21078, 2104, 21011,
			  2101, 20990, 2096, 2095, 20940, 20934, 20883, 2087, 2086, 2083, 2082, 2081, 2080, 20734, 2070, 2069, 2062,
			  20473, 2031, 20280, 20228, 20227, 20226, 20225, 20224, 20223, 20180, 20179, 20147, 20127, 20125, 20118,
			  20111, 20106, 20102, 20089, 20085, 20080, 20076, 20052]

	for PORT in toScan:
		if scanport(IP, PORT):
			openPorts.append(PORT)

	openPorts.sort()
	reply("Open ports found for " + text + " (" + str(len(openPorts)) + "): " + str(openPorts))
