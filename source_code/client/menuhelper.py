"""
Code created by Sylvester Francis
Student ID : 8735728
Created date : 26 March 2022
Last Modified date : 26 February 2022
Last Modified by  : Sylvester Francis
"""
import sys
sys.path.append("..")
import backend.User as user
import backend.Building as building
import backend.apartment as apartment
from getpass import getpass
from helper import clear,encryptPassword,decryptPassword
from bson.objectid import ObjectId
userTypes = {1:'Tenant',2:'Owner',3:'Staff'}

''' Login helper
Purpose: The below function is used as a helper function for login 
Params : None
Return value : None
'''
def login_helper():
    clear()
    print("\n ********************************************************************************** \n")
    print(" \n Login")
    print("\n ********************************************************************************** \n")
    username = input("\n Enter your username: ")
    password = getpass("\n Enter the password: ")
    q = {}
    data = {}
    q['username'] = username
    current_User = user.get_one_user(q)
    data.update({'username':current_User['username'],'_id':current_User['_id'],'password':current_User['password']})
    if current_User['userType'] == userTypes[1]:
        tenant_path(data,'login')
    elif current_User['userType'] == userTypes[2]:
        owner_path(data,'login')
    elif current_User['userType'] == userTypes[3]:
        staff_path(data,'login')

    



''' Signup helper
Purpose: The below function is used as a helper function for signup
Params : None
Return value : issignedup -> Boolean 
'''
def signup_helper():
    clear()
    data = {}
    print("\n ********************************************************************************** \n")
    print(" \n Signup")
    print("\n ********************************************************************************** \n")
    firstname = input("\nEnter your First Name: ")
    lastname  = input("\nEnter your Last Name:  ")
    email     = input("\nEnter your Email ID:  ") 
    username  = input("\nEnter your preferred username: ")
    password  = getpass("\nEnter your password: ") 
    confirmpassword = getpass("\nRe-enter the password: ")
    if password == confirmpassword:
        password = encryptPassword(password)
    else:
        print("\n Password doesnot match")
    phno = input("\n Enter your phone number: ")
    select_userType = input("\n Please select the type of user: \n1.Tenant \n2.Owner \n3.Staff \n Please type one of the following options(1,2 or 3)")
    userType =''
    if select_userType == '1':
        userType = userTypes[1]
        data.update({'FirstName':firstname,'LastName':lastname,'email':email,'username':username,'password':password,'userType':userType,'phoneNumber':phno})
        issignedUp = tenant_path(data,'signup')
    elif select_userType == '2':
        userType= userTypes[2]
        data.update({'FirstName':firstname,'LastName':lastname,'email':email,'username':username,'password':password,'userType':userType,'phoneNumber':phno})
        owner_path(data,'signup')
    elif select_userType == '3':
        userType= userTypes[3]
        data.update({'FirstName':firstname,'LastName':lastname,'email':email,'username':username,'password':password,'userType':userType,'phoneNumber':phno})
        staff_path(data,'signup')
    else:
        print("\n Invalid option")
    return issignedUp



''' Tenant path
Purpose: The below function is used as a added function  for tenant signup 
Params : data -> Dictionary with all user inputs, typeAction -> [login,signup]
Return value : signedup -> Boolean 
'''  

def tenant_path(data,typeAction):
    if typeAction == 'signup':
        signedup = False
        errorApartment = True
        errorBuilding = True
        clear()
        print("\nHere are the list of buildings available: ") 
        buildings = building.get_multiple_buildingInfo()
        building_list = {}
        print("\n ********************************************************************************** \n")
        for index,item in enumerate(buildings):
            print("\n ****************************** General-Details of Building - {0} ********************************************* \n".format(index+1))
            print("\n Name of the building : {0} \n Address: {1} \n City: {2} \n PostalCode: {3} \n Province: {4} ".format(item['buildingName'],item['Address'],item['City'],item['postalCode'],item['province']))
            print("\n ****************************** Facilities of Building - {0} ********************************************* \n".format(index+1))
            print("\n Furnished :{0}, \n Parking : {1}, \n Pet-Friendly: {2}, \n Storage: {3}".format(item['isFurnished'],item['isParkingAvailable'],item['petFriendly'],item['storageAreaAvailable']))
            building_list[index+1] = item['_id']
        print("\n ********************************************************************************** \n")
        while errorBuilding:
            try:
                select_building = int(input("\n Enter the building that you are interested in: "))
                if select_building not in building_list.keys():
                    raise KeyError("Building not found please try again")
                elif select_building in building_list.keys():
                    q = {}
                    q['buildingId'] = ObjectId(building_list[select_building])
                    q['isAvailable'] = True
                    apartmentlist = apartment.get_multiple_apartmentInfo(q)
                    if len(apartmentlist) > 0:
                        errorBuilding = False
                    else:
                        raise KeyError("Sorry,No apartments available in this building,try again")
            except KeyError as ke:
                print("\n{0}".format(ke))
                continue  
            errorBuilding = False      
        apartmentid = {}
        clear()
        print("\n ********************************************************************************** \n")
        for index,item in enumerate(apartmentlist):
            print("\n ****************************** Facilities of Apartment - {0} ********************************************* \n".format(index+1))
            print("\n Furnished :{0}, \n No Of Washrooms : {1}, \n Ensuite Washroom: {2}, \n Ensuite Laundry: {3}, \n Rent Price: {4}".format(item['isFurnished'],item['noOfWashrooms'],item['hasEnsuiteWashroom'],item['hasEnsuiteLaundry'],0))
            apartmentid[index+1] = item['_id']
        print("\n ********************************************************************************** \n")
        print("\n ********************************************************************************** \n")
        while errorApartment:
            try:
                select_apartment = int(input("\n Enter the apartment that you are interested in: "))
                if select_apartment not in apartmentid.keys():
                    raise KeyError("Apartment not found please try again")
            except KeyError as e:
                print("\n {0}".format(e))
                continue
            errorApartment = False
        data['buildingId'] = building_list[select_building]
        data['apartmentId'] = apartmentid[select_apartment]
        user_obj = user.signup(data)
        if user_obj != None:
            print("\n User signed up successfully")
            signedup = True
            return signedup
        else:
            print("\n Error in signing up User, please try again")
            return signedup
    elif typeAction == 'login':
        tenant_menu()



''' Owner path
Purpose: The below function is used as a added function  for owner signup path/login path
Params : data -> Dictionary with all user inputs,typeAction -> [login,signup]
Return value : signedup -> Boolean 
'''  
def owner_path(data,typeAction):
    print("\n Owner path called")
    if typeAction == 'signup':
        print("\n Owner signup path")
    elif typeAction =='login':
        owner_menu()


''' Staff path
Purpose: The below function is used as a added function  for staff signup 
Params : data -> Dictionary with all user inputs,typeAction -> [login,signup]
Return value : signedup -> Boolean 
'''  
def staff_path(data,typeAction):
    print("\n Staff path called")
    if typeAction == 'signup':
        print("\n Staff signup path")
    elif typeAction == 'login':
        staff_menu()
    

def tenant_menu():
    clear()
    menu_selection = True
    print("\n ********************************************************************************** \n")
    print("\n 1. View profile ")
    print("\n 2. View apartment detail ")
    print("\n 3. Raise service request ")
    print("\n 4. Raise sublet request")
    print("\n 5. Pay rent")
    print(" \n Please choose one of the following options to continue")
    while menu_selection:
        try:
            selection = input("\n Enter your choice:")
            if selection == '1':
                viewProfile()
            elif selection == '2':
                viewapartment()
            elif selection == '3':
                raise_service_req()
            elif selection == '4':
                raise_sublet_req()
            elif selection == '5':
                pay_rent()
            else:
                raise KeyError('\n Invalid option, try again')
        except KeyError as ke:
            print('\n{0}'.format(ke))
            continue
        menu_selection = False
        
        

    
def owner_menu():
    pass
def staff_menu():
    pass




    
    

    
