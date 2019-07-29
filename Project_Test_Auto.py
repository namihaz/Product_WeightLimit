###########################################################################################################
'''
The business provides customers with a variety of chairs or seats built into a
harness that can be attached to a bungee cord. The chairs come in multiple
colors and sizes suitable for adults, children and infants.   Each chair size
is specified to support both minimum and maximum weight limits for safety
requirements.

Business System Overview:
*Customers choose from a list of products and options
*Customers submit orders for the products
*Orders are matched to the product list to determine sales amounts and manufacturing specifications.
*A sales report is produced to show gross cost, sales and net profit
*A safety report is available on request to review the weight limit testing results
'''
##############################################################################################################
## Modules
import operator
import csv
import sys

##############################################################################################################
def f_read_prod():
    '''
    Read the product csv and load it to dictionary
    Key- Product number
    Value- Quantity
    '''

## Local Variables
    d_prod = {}
    d_row = []
    v_file1 = 'products.csv'
    v_reader = ''
    

## Open file and check if file exists
    try:
        v_file1 = open(v_file1)
    except IOError:
        print("\nError - file not found")
        input("\n\nPress enter key to exit.")
        sys.exit

## Read each row in the file with the values in the first row used as dictionary
 
    v_reader = csv.DictReader(v_file1)
    
    for d_row in v_reader:
        if d_row['prod_nbr'] in d_prod:
            print("\n\nDuplicate key in the product",d_row['prod_nbr'])   # Check for duplicate key product value
        else:    
            d_prod[d_row['prod_nbr']] = [int(d_row['min']), int(d_row['max']), (d_row['size']), (d_row['color'])]

    v_file1.close()

## Check for empty file    
    if not d_prod:
        print("\n\nError-Product File is empty")
        input("\n\nPress enter to exit")
        
        
    return d_prod
      
#############################################################################################################
def f_dict_to_list(p_dict):
    '''
#############################################################################################################
Transfer the contents of the product dictionary to a list.
Input: p_dict - key = product number : value = min, max, size, color
Output: l_list1
#############################################################################################################
'''
    ## Local Variable
    l_list1 = []

    ## Loop through the dictionary
    for key, value in p_dict.items():
        l_list1.append([key,value[0],value[1],value[2],value[3]])
    
    print("\n\nProduct List Loaded")
    return l_list1
    
############################################################################################################
def f_read_test():
    '''
############################################################################################################
Read the test.csv file and load it to list
Input: test id,product number, test
Output: l_list2
#############################################################################################################
'''
    ## Local Variable
    l_list2 = []
    i = 0
    v_file2 = 'tests.csv'
    r = ''                        ## File read iterator
    
## Open file and check if file exist
    
    try:
        v_file2 = open(v_file2)
    except IOError:
        print("Error - file not found")
        input("\n\nPress enter key to exit.")
        sys.exit

## Read each row in the file into a list        
        
    r = csv.reader(v_file2)       ##Return a reader iterator for the file
    for l_row in r:               ## Loop on each row in the file into a list
        if i == 0:
            i += 1                ## skip first row containing column titles
            continue
        l_items = [l_row[0],
                   l_row[1],
                   int(l_row[2])
                   ]
        l_list2.append(l_items)
    v_file2.close()
    
    
    print("\n\nTest List Loaded")
    return l_list2

#############################################################################################################
def f_run_test():
    '''
#############################################################################################################
Create a data structure that combines prouduct and test structure, where each product is associated with a
summary of quantity of the tests that Passed, Failed and Warnings results are displayed 
Input: Product list, Test list
Output:Test Result
#############################################################################################################
'''
        
    ## Local Variables
    L_file = []
    r = ()
  
    for i in l_prod:
        pass_count = 0
        warning_count = 0
        fail_count = 0    
        for j in l_tests:
            if i[0] == j[1]:
                if  int(j[2])   < int((i[1])-(10/100 * (i[1]))):                  # test value < -10% prod(min)
                    test_result = 'Fail'
                    fail_count += 1
                elif int((i[1]) - (10/100 * i[1])) <= int(j[2]) < int(i[1]):      # -10% prod(min) <= test value < prod(min)
                    test_result = 'Warning'
                    warning_count += 1
                elif int(i[1])  <= int(j[2]) <= int(i[2]):                        # prod(min) <= test value <= prod(max)
                    test_result = 'Pass'
                    pass_count  += 1
                elif int(i[2])  < int(j[2]) <= (int(i[2]) + int(10/100 * i[2])):  # prod(max) < test value <= max + 10% prod(max)
                    test_result = 'Warning'
                    warning_count += 1
                elif (int(i[2]) + int(10/100 * i[2])) < int(j[2]):                # max + 10% prod(max)< test value
                    test_result = 'Fail'
                    fail_count  += 1
                else:
                    pass      
                   
            else:
                continue
            
        r = (  i[0]              # 0 Product number
              ,i[3]              # 1 Size
              ,i[4]              # 2 Color
              ,pass_count        # 3 Pass quantity 
              ,warning_count     # 4 Warning quantity 
              ,fail_count        # 5 Fail quantity
              )
    
        L_file.append(r)
   
   
    print("\n\nNew List Processed")
    return L_file

############################################################################################################
def f_menu_report(p_list):
    '''
############################################################################################################
Display the report option menu of the metrics to sort
* Passed Tests, Warning Tests, Failed Tests
############################################################################################################
    '''
    ## Local Variables
    
    loop1 = True
    m_choice = None
    s_hdr_fmt = "|{0:^9}|{1:^8}|{2:^8}|{3:^10}|{4:^10}|{5:^10}|"
    s_dat_fmt = "|{0:<9}|{1:<8}|{2:<8}|{3:>10}|{4:>10}|{5:>10}|"
     
    
    while loop1:
        print(
            """\n
            ====Test Result Menu=====
            
            1. Passed Test Result
            2. Warning Test Result
            3. Failed Test Result
            4. Exit
            """
            )
        m_choice = input("Select any option to sort: choice[1-4]: ")
        if m_choice != "4":
            print("\n\n\t\t ======Test Result Report==========\n")
            print(s_hdr_fmt.format('---------','--------','--------','----------','----------','----------'))
            print(s_hdr_fmt.format('Product','','','Passed','Warning','Failed'))
            print(s_hdr_fmt.format('Number','Size','Color','Count','Count','Count'))
            print(s_hdr_fmt.format('---------','--------','--------','----------','----------','----------'))
        else:
            pass
            
        if m_choice == "1":
            v_item = int(m_choice) + 2 
            for p,q,r,s,t,u in sorted (p_list, key=operator.itemgetter(v_item), reverse = True):  # Sort the report based on total Pass quantity in descending order
                print(s_dat_fmt.format(p,q,r,s,t,u))
        elif m_choice == "2":
            v_item = int(m_choice) + 2
            for p,q,r,s,t,u in sorted (p_list, key=operator.itemgetter(v_item), reverse = True):  # Sort the report based on total Warn quantity in descending order
                print(s_dat_fmt.format(p,q,r,s,t,u))
        elif m_choice == "3":
            v_item = int(m_choice) + 2
            for p,q,r,s,t,u in sorted (p_list, key=operator.itemgetter(v_item), reverse = True):  # Sort the report based on total Fail quantity in descending order
                print(s_dat_fmt.format(p,q,r,s,t,u))
        elif m_choice == "4":
            loop1 = False
            print("Exited from Test Report Menu")
            
        else:
            print("Sorry, but", m_choice, "isn't a valid choice.")
            
                      
    return            


#############################################################################################################
def main():
    ## Global Variables
    global l_prod                     # Declare global product list
    l_prod = []
    
    global l_tests                    # Declare global test list
    l_tests = []
    
    
    ## Local variables:
    
    l_run_test = []
    choice = None
    loop = True
    
    while loop:
        print(
        """\n\n
        Main Menu
        ================
        1. Load Products
        2. Load Tests
        3. Run Tests
        4. Test Report
        5. Exit
        """
        )

        choice = input("Enter your choice [1-5]: ")
              
        if choice == "1":
            d_prod = f_read_prod()
            l_prod = f_dict_to_list(d_prod)
                        
        elif choice == "2":
            l_tests = f_read_test()
            
        elif choice == "3":
            l_run_test = f_run_test()
            
        elif choice == "4":
            r_test_file = f_menu_report(l_run_test)
            
        elif choice == "5":
            loop = False
            print("Exited from Main Menu ")
            
        else:
            print("Sorry, but", choice, "isn't a valid choice.")

    return
    input("Press enter to exit")
    
        
        

main()

    
                
                                            





                                             
            
                
                     
    
     


