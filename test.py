import general_funcs
import igs_funcs as igs
from new_project import *


general_funcs.gotoTracking()

slip_button_thang_majiger = igs.IGS_Generate_Update_Logs(
    inv_loc='Customers\\IGS\\Inventory\\IGS_Inventory_Tracking.xlsx',
    proj=102105,
    itms=['300L Tank', '150L Tank'],
    qtys=[2, 5]
)

slip_button_thang_majiger.CheckandUpdate()

