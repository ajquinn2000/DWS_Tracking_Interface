from tkinter import messagebox
from pandas import read_excel

# random edit


class Generate_Update_Logs:
    """Handles logging file management and Packing Slip creation"""


    def __init__(self, inv_loc, proj, itms: list, prt_nums: list, qtys: list):
        super().__init__()

        # location of IGS inventory tracking
        self.inventory_loc = inv_loc
        # project number that it is for
        self.project = proj
        # indexes of the items chosen

        self.items = itms
        self.part_numbers = prt_nums
        self.quantitties = qtys
        self._i = len(self.items)

        self.LoadData()

        self.indexes = [self.description.index(item) for item in self.items]

        self.CheckPreviousSlips()
        self.CheckandUpdate()


    def LoadData(self):
        """Loads the information from the IGS inventory file"""
        # Gettting the info from the file
        inv_data = read_excel(self.inventory_loc)
        # print(inv_data)

        self.description = inv_data['Description'].values.tolist()
        self.part_num = inv_data['IGS Part Num'].values.tolist()
        self.igs_inv = inv_data['IGS Inventory'].values.tolist()
        self.dws_inv = inv_data['DWS Inventory'].values.tolist()

    def CheckPreviousSlips(self):
        

    def CheckandUpdate(self):
        """Will check IGS and DWS inventories to make sure what action to take and if it is alright."""
        # cycling through the indexes of items chosen to get condition
        for i, given_chosen_index in enumerate(self.indexes):
            # getting a given line's quntities: amount asked, amount igs has amount dws has
            amount_shipping = int(self.quantitties[i])
            igs_amnt = self.igs_inv[given_chosen_index]
            dws_amnt = self.dws_inv[given_chosen_index]
            product = self.description[given_chosen_index]

            approved, checked_message = self.check_inventory(amount_shipping, igs_amnt, dws_amnt, product)

            # if the changes are approved from the check_inventory func then it will amend the current numbers
            if approved:
                self.igs_inv[given_chosen_index] = igs_amnt






        self.Generate_Packing_Slip()

    def check_inventory(self, a_s, i_a, d_a, prod):
        """Checks the inventories of IGS and DWS. It outputs a string message declaring what will be done with the
        current amount in both inventories."""
        a: str
        b: str
        c: str

        # if igs has nothing in their inventory
        if i_a == "":
            a = f'>IGS has no inventory for ct. {a_s}: \n' \
                f'>> {prod} \n' \
                f'>They currently have {i_a}. They are {a_s} over.\n'

        # if igs has some inventory, but not enough to complete the order
        elif i_a < a_s:
            # the amount in igs inventory is subtracted from the amount being sent
            a_s = a_s - i_a
            a = f'>IGS does not have enough inventory for {a_s + i_a}   :\n' \
                f'  >> {prod} \n' \
                f'>They currently have {i_a}. They are {a_s} over.\n'
            i_a = 0

            # since igs did not have enough, it is checking it against how much we have in our inventory
            # if we do not have enough in our inventory, calculating how much we need to build
            if d_a < a_s:
                need_to_build = a_s - d_a
                b = f'>We do not have enough in our inventory either.\n' \
                    f'>We will need to build {need_to_build} more for this job.\n' \
                    f'>We have {d_a} currently in our inventory.'
                d_a = 0

            # if we do have enough in our inventory and igs does not
            else:
                a = a + f'\n>We will need to use {a_s} of our own inventory.\n'
                b = f'>We have {d_a} currently in our inventory.\n'
                d_a = d_a - a_s

        # if igs has enough in their inventory
        else:
            i_a = i_a - a_s

        # summary comment after figuring out what needs to be taken out of who's inventory
        c = f'\n>After completing this order for: \n' \
            f'    >>>{prod} + \n' \
            f'  >>IGS will have: {i_a} + \n' \
            f'  >>DWS will have: {d_a}'

        output_message = a + b + c

        title = f'Add {prod} to Slip?'
        print(f'{title}\n{output_message}')
        approve = messagebox.askyesnocancel(title=title, message=output_message)

        return approve, output_message

    def Generate_Packing_Slip(self):
        pass
