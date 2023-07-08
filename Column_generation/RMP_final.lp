\ Model RMP
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  137.4 y_0 + 141.2 y_1 + 132.2 y_2 + 136.2 y_3 + 130.3 y_4 + 138 y_5
   + 132 y_6 + 136.2 y_7 + 140.2 y_8 + 133.5 y_9 + 139.3 y_10 + 176.2 y_11
   + 161.6 y_12 + 178.7 y_13 + 172.1 y_14 + 180.6 y_15 + 166.6 y_16
   + 170.7 y_17 + 178.1 y_18 + 120 y_19 + 203.21 cg_1 + 237.27 cg_2
   + 159.49 cg_3 + 210.27 cg_4 + 200.6 cg_5 + 209.75 cg_6 + 220.58 cg_7
   + 199.17 cg_8 + 210.06 cg_9 + 191.92 cg_10 + 195.93 cg_11 + 198.16 cg_12
   + 189.26 cg_13 + 190.98 cg_14 + 193.8 cg_15 + 198.82 cg_16
   + 183.16 cg_17 + 188.33 cg_18 + 226.64 cg_19 + 192.36 cg_20
   + 193.72 cg_21 + 146.85 cg_22 + 185.9 cg_23 + 158.06 cg_24
   + 197.19 cg_25 + 165.48 cg_26 + 203.42 cg_27 + 205.66 cg_28
   + 152.48 cg_29 + 154.82 cg_30 + 148.36 cg_31 + 201.12 cg_32
   + 149.31 cg_33 + 149.04 cg_34 + 198.81 cg_35 + 157.58 cg_36
   + 151.57 cg_37 + 196.99 cg_38 + 193.72 cg_39 + 167.18 cg_40
   + 194.26 cg_41 + 148.23 cg_42 + 195.88 cg_43 + 195.88 cg_44
   + 149.11 cg_45 + 178.42 cg_46 + 199.48 cg_47 + 189.62 cg_48
   + 194.97 cg_49 + 176.57 cg_50 + 183.08 cg_51 + 192.55 cg_52
   + 196.41 cg_53 + 197.18 cg_54 + 148 cg_55 + 196.08 cg_56 + 191.83 cg_57
   + 156.04 cg_58 + 189.65 cg_59 + 195.42 cg_60 + 200.06 cg_61
   + 196.41 cg_62 + 192.29 cg_63 + 194.93 cg_64 + 187.88 cg_65
   + 194.27 cg_66 + 168.86 cg_67 + 198.26 cg_68 + 196.27 cg_69
   + 196.35 cg_70 + 157.25 cg_71 + 172.55 cg_72 + 191.48 cg_73
   + 194.19 cg_74 + 183.86 cg_75 + 164.4 cg_76 + 158.68 cg_77
Subject To
 R0: y_0 + cg_1 + cg_2 + cg_3 + cg_4 + cg_5 + cg_7 + cg_10 + cg_18 + cg_25
   + cg_26 + cg_28 + cg_29 + cg_30 + cg_32 + cg_45 + cg_46 + cg_49 + cg_51
   + cg_56 + cg_58 + cg_60 + cg_62 + cg_63 = 1
 R1: y_1 + cg_1 + cg_2 + cg_3 + cg_4 + cg_6 + cg_9 + cg_20 + cg_22 + cg_23
   + cg_25 + cg_27 + cg_36 + cg_38 + cg_41 + cg_46 + cg_47 + cg_49 + cg_51
   + cg_53 + cg_54 + cg_56 + cg_57 + cg_58 + cg_59 + cg_60 + cg_61 + cg_62
   + cg_63 + cg_64 + cg_68 + cg_70 + cg_71 + cg_72 + cg_73 + cg_74 + cg_77
   = 1
 R2: y_2 + cg_3 + cg_4 + cg_7 + cg_9 + cg_11 + cg_12 + cg_13 + cg_19
   + cg_20 + cg_22 + cg_24 + cg_31 + cg_33 + cg_34 + cg_37 + cg_40 + cg_42
   + cg_45 + cg_46 + cg_55 + cg_57 + cg_58 + cg_64 + cg_67 + cg_71 + cg_72
   + cg_76 + cg_77 = 1
 R3: y_3 + cg_1 + cg_2 + cg_3 + cg_5 + cg_8 + cg_11 + cg_12 + cg_14 + cg_15
   + cg_16 + cg_40 + cg_45 + cg_57 + cg_58 + cg_63 + cg_68 = 1
 R4: y_4 + cg_3 + cg_4 + cg_6 + cg_11 + cg_12 + cg_13 + cg_22 + cg_29
   + cg_30 + cg_31 + cg_33 + cg_34 + cg_36 + cg_37 + cg_42 + cg_45 + cg_58
   + cg_71 + cg_77 = 1
 R5: y_5 + cg_3 + cg_10 + cg_12 + cg_14 + cg_15 + cg_16 + cg_17 + cg_19
   + cg_20 + cg_22 + cg_23 + cg_24 + cg_25 + cg_26 + cg_30 + cg_31 + cg_34
   + cg_37 + cg_38 + cg_57 + cg_58 + cg_59 + cg_60 + cg_61 + cg_62 + cg_63
   + cg_64 + cg_65 + cg_68 + cg_69 + cg_70 + cg_71 + cg_72 + cg_73 + cg_74
   + cg_76 + cg_77 = 1
 R6: y_6 + cg_3 + cg_7 + cg_9 + cg_11 + cg_13 + cg_18 + cg_22 + cg_24
   + cg_29 + cg_30 + cg_31 + cg_36 + cg_37 + cg_40 + cg_42 + cg_45 + cg_50
   + cg_51 + cg_55 + cg_58 + cg_59 + cg_63 + cg_71 + cg_72 + cg_73 + cg_76
   + cg_77 = 1
 R7: y_7 + cg_3 + cg_9 + cg_11 + cg_13 + cg_17 + cg_18 + cg_19 + cg_20
   + cg_24 + cg_26 + cg_29 + cg_30 + cg_33 + cg_34 + cg_36 + cg_37 + cg_40
   + cg_45 + cg_50 + cg_57 + cg_58 + cg_63 + cg_64 + cg_72 + cg_73 + cg_77
   = 1
 R8: y_8 + cg_3 + cg_9 + cg_10 + cg_12 + cg_14 + cg_15 + cg_16 + cg_18
   + cg_19 + cg_23 + cg_24 + cg_26 + cg_29 + cg_30 + cg_31 + cg_33 + cg_36
   + cg_40 + cg_41 + cg_42 + cg_45 + cg_51 + cg_53 + cg_54 + cg_56 + cg_58
   + cg_60 + cg_63 + cg_64 + cg_65 + cg_68 + cg_70 + cg_71 + cg_72 + cg_73
   + cg_76 + cg_77 = 1
 R9: y_9 + cg_2 + cg_3 + cg_9 + cg_10 + cg_11 + cg_13 + cg_15 + cg_18
   + cg_20 + cg_26 + cg_30 + cg_33 + cg_34 + cg_36 + cg_37 + cg_40 + cg_42
   + cg_59 + cg_63 + cg_64 + cg_71 + cg_72 + cg_73 + cg_76 + cg_77 = 1
 R10: y_10 + cg_3 + cg_9 + cg_10 + cg_12 + cg_13 + cg_15 + cg_17 + cg_23
   + cg_25 + cg_26 + cg_29 + cg_31 + cg_36 + cg_37 + cg_40 + cg_41 + cg_49
   + cg_50 + cg_53 + cg_54 + cg_57 + cg_58 + cg_59 + cg_60 + cg_62 + cg_63
   + cg_64 + cg_65 + cg_68 + cg_71 + cg_72 + cg_73 + cg_74 + cg_76 + cg_77
   = 1
 R11: y_11 + cg_1 + cg_2 + cg_4 + cg_5 + cg_6 + cg_7 + cg_9 + cg_11 + cg_13
   + cg_21 + cg_27 + cg_28 + cg_32 + cg_35 + cg_39 + cg_43 + cg_44 + cg_66
   = 1
 R12: y_12 + cg_1 + cg_2 + cg_5 + cg_8 + cg_10 + cg_14 + cg_15 + cg_16
   + cg_17 + cg_18 + cg_19 + cg_20 + cg_21 + cg_23 + cg_25 + cg_27 + cg_32
   + cg_38 + cg_39 + cg_41 + cg_43 + cg_44 + cg_46 + cg_47 + cg_48 + cg_49
   + cg_50 + cg_51 + cg_52 + cg_53 + cg_54 + cg_56 + cg_57 + cg_59 + cg_60
   + cg_61 + cg_62 + cg_63 + cg_64 + cg_65 + cg_66 + cg_67 + cg_68 + cg_69
   + cg_70 + cg_73 + cg_74 + cg_75 = 1
 R13: y_13 + cg_1 + cg_2 + cg_4 + cg_5 + cg_6 + cg_7 + cg_8 + cg_13 + cg_27
   + cg_32 + cg_35 + cg_38 + cg_39 + cg_44 + cg_47 + cg_48 + cg_52 + cg_61
   + cg_66 + cg_69 = 1
 R14: y_14 + cg_4 + cg_5 + cg_6 + cg_7 + cg_8 + cg_14 + cg_16 + cg_21
   + cg_23 + cg_25 + cg_27 + cg_28 + cg_32 + cg_35 + cg_38 + cg_39 + cg_41
   + cg_43 + cg_44 + cg_48 + cg_49 + cg_52 + cg_54 + cg_56 + cg_60 + cg_61
   + cg_65 + cg_66 + cg_68 + cg_69 + cg_70 + cg_74 + cg_75 = 1
 R15: y_15 + cg_1 + cg_2 + cg_4 + cg_5 + cg_6 + cg_7 + cg_8 + cg_11 + cg_16
   + cg_19 + cg_21 + cg_27 + cg_28 + cg_35 + cg_38 + cg_39 + cg_43 + cg_44
   = 1
 R16: y_16 + cg_1 + cg_2 + cg_5 + cg_6 + cg_8 + cg_10 + cg_14 + cg_15
   + cg_17 + cg_21 + cg_28 + cg_32 + cg_35 + cg_38 + cg_39 + cg_41 + cg_43
   + cg_44 + cg_47 + cg_49 + cg_52 + cg_53 + cg_56 + cg_60 + cg_61 + cg_62
   + cg_65 + cg_66 + cg_69 + cg_70 + cg_74 + cg_75 = 1
 R17: y_17 + cg_1 + cg_2 + cg_4 + cg_5 + cg_6 + cg_8 + cg_10 + cg_12
   + cg_14 + cg_16 + cg_25 + cg_27 + cg_28 + cg_32 + cg_35 + cg_41 + cg_43
   + cg_44 + cg_47 + cg_48 + cg_52 + cg_53 + cg_54 + cg_56 + cg_61 + cg_62
   + cg_65 + cg_66 + cg_68 + cg_69 + cg_70 + cg_74 + cg_75 = 1
 R18: y_18 + cg_1 + cg_4 + cg_6 + cg_7 + cg_8 + cg_12 + cg_14 + cg_15
   + cg_16 + cg_21 + cg_25 + cg_27 + cg_28 + cg_32 + cg_35 + cg_39 + cg_43
   + cg_44 + cg_47 + cg_49 + cg_52 + cg_53 + cg_54 + cg_56 + cg_60 + cg_62
   + cg_66 + cg_68 + cg_69 + cg_70 + cg_75 = 1
 R19: y_19 + cg_7 + cg_9 + cg_24 + cg_26 + cg_28 + cg_35 + cg_40 + cg_55
   + cg_72 + cg_76 = 1
Bounds
End
