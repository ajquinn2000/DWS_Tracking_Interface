import general_funcs
import igs_funcs as igs
from new_project import *

# create_new_project()

# general_funcs.gotoTracking()
#
slip_button_thang_majiger = igs.IGS_Generate_Update_Logs(
    shipping_loc='1234 ur mum\n @ earf',
    proj=112140,
    itms=['300L Tank', '150L Tank', 'Modular Body', 'Modular Firing Assembly'],
    qtys=[2, 5, 15, 69]
)

slip_button_thang_majiger.CheckandUpdate()

# AddDataToExcel(
#     excel_loc='Projects\\112139\\D2-7.0-112139 - Packing Slip.xlsx',
#     sheet_name='INPUT',
#     row_list_data=[['a', 'b', 'c'], ['a', 'b', 'c']],
#     place_loc=(0, 0),
#     scan_max=(7, 2)
# )
#
# AddDataToExcel('Projects\\112139\\D2-7.0-112139 - Packing Slip.xlsx', 'INPUT', [['a', 'b', 'c'], ['a', 'b', 'c']], (0, 7), (10, 2))
