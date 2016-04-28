from random import randint
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from main.BogusFormBuilder import BogusFormBuilder


class VPSBuyer(object):
    '''
    This is the standard class to buy a VPS host. By itself, it does nothing; this class is supposed to be extended by other classes, each for a specific VPS Provider
    '''
    def __init__(self):
        self.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.FIREFOX)
        self.generator = BogusFormBuilder()
        
        self.email = self.generator.getEmail()
        #password = generator.getPassword()
        self.password = self.generator.getRAString(32)
        pass
    
    def getFormValue(self, name):
       "function_docstring"
       return "To be implemented: " + name
    
    
    '''
    Automatically fills ina form element by executing a piece of javascript that sets the value attribute of the form element
    '''
    def fillInElement(self, fieldname, value):
        #driver.find_element_by_css_selector("input[name='" + fieldname + "']").send_keys(value)
        
        # ^ send_keys has some issues, using javascript to set an attribute instead:
        self.driver.execute_script('arguments[0].setAttribute("value", "' + value + '")', self.driver.find_element_by_css_selector("input[name='" + fieldname + "']"))
        
    '''
    Chooses one of the elements in a select list randomly, except for the first element
    '''
    def clickRandomSelectElement(self, fieldId):
        el = self.driver.find_element_by_id(fieldId)
        options = el.find_elements_by_tag_name('option')
        num = randint(1, len(options) - 1)
        option = options[num]
        option.click()
    
    
class ZappiehostBuyer(VPSBuyer):
    '''
    This class orders a VPS from zappiehost.com
    '''
    def __init__(self, email = "", password = "", SSHPassword = ""):
        super(ZappiehostBuyer, self).__init__()
        self.email = email
        if self.email == "":
            self.email = self.generator.getEmail()
            
        self.password = password
        if self.password == "":
            self.password = self.generator.getRAString(32)
            
        self.SSHPassword = SSHPassword
        if self.SSHPassword == "":
            self.SSHPassword = self.generator.getRAString(32)
        pass
        
        
    def buy(self):
        self.placeOrder() # places the order
        # pay the amount here
        self.setSSHPassword()
        return self.SSHPassword
        
        
    def placeOrder(self):
        try:
            
            self.driver.get("https://billing.zappiehost.com/cart.php?a=confproduct&i=0")
            
            #Click the to cart button for the cheapest VPS
            self.driver.find_element_by_css_selector('.cartbutton.ui-button.ui-widget.ui-state-default.ui-corner-all').click()
            
            #Click the continue button
            self.driver.find_element_by_css_selector('.cartbutton.green.ui-button.ui-widget.ui-state-default.ui-corner-all').click()
            
            
            #Click the pay by bitcoin button
            self.driver.find_element_by_css_selector("input[type='radio'][value='bitpay']").click()
            
            
            #driver.find_element_by_css_selector("input[name='firstname']").send_keys(getFormValue('firstname'))
            
            
            self.fillInElement('firstname', self.generator.getFirstName())
            self.fillInElement('lastname', self.generator.getSurname())
            self.fillInElement('email', self.email)
            self.fillInElement('address1', self.generator.getRAString(randint(8, 15)) + ' ' + self.generator.getRNString(randint(1, 2)))
            self.fillInElement('city', self.generator.getCity())
            self.fillInElement('postcode', self.generator.getZipcode())
            
            self.clickRandomSelectElement('country')
            
            select = Select(self.driver.find_element_by_id('country'))
            selected_text = select.first_selected_option.text;
            
            if selected_text == 'United States' or selected_text == 'Spain' or selected_text == 'Australia' or selected_text == 'Brazil' or selected_text == 'Canada' or selected_text == 'France' or selected_text == 'Germany' or selected_text == 'India' or selected_text == 'Italy' or selected_text == 'Netherlands' or selected_text == 'New Zealand' or selected_text == 'United Kingdom':
                # For US, Brazil, Canada, France, Germany, India, Italia, Netherlands, New Zealand and United Kingdom select state option in a select
                self.clickRandomSelectElement('stateselect')
            else:
                # For all other countries, fill in string
                self.fillInElement('state', self.generator.getRAString(randint(6, 12)))
                
            
            self.fillInElement('phonenumber', self.generator.getPhoneNum())
            
            # password =  # Generate a password
            self.fillInElement('password', self.password)
            self.fillInElement('password2', self.password)
            
            self.driver.find_element_by_css_selector("input[type='submit'][class='cartbutton green ui-button ui-widget ui-state-default ui-corner-all']").click() # Submit the form
            
            self.driver.find_element_by_css_selector("input[type='submit'][value='Pay Now']").click()
            
            
            self.driver.implicitly_wait(10)
            
            bitcoinAmount = self.driver.find_element_by_css_selector(".ng-binding.payment__details__instruction__btc-amount").text
            toWallet = self.driver.find_element_by_css_selector(".payment__details__instruction__btc-address.ng-binding").text
            
            print "Bitcoin amount to transfer: " + bitcoinAmount
            
            print "To wallet: " + toWallet
        
        except Exception as e:
            print "Could not complete the transaction because an error occurred:"
            print e
            #raise # Raise the exception that brought you here 
    
    def setSSHPassword(self):
        try:
            
            self.driver.get("https://billing.zappiehost.com/clientarea.php")
            
            #Click the to cart button for the cheapest VPS
            self.fillInElement('username', self.email)
            self.fillInElement('password', self.password)
            
            self.driver.find_element_by_id('login').click()
            
            self.driver.get("https://billing.zappiehost.com/clientarea.php?action=products")
            self.driver.find_element_by_css_selector(".table.table-striped.table-framed").find_element_by_css_selector(".btn-group").find_element_by_css_selector(".btn").click()
            
            self.driver.find_element_by_css_selector(".icon-btn.icon-reinstall").click()
            
            
            #driver.find_element_by_id('password')._execute(command, params)
            self.driver.find_element_by_id('password').send_keys(self.SSHPassword)
            #fillInElement("rebuild[password]", SSHPassword)
            
            self.driver.find_element_by_css_selector("input[value='local:vztmpl/ubuntu-14.04-64bit.tar.gz']").click()
            
            self.driver.find_element_by_css_selector(".form-actions").find_element_by_css_selector(".btn.btn-primary").click()
        
            print "New SSH Password: " + self.SSHPassword
            
        except Exception as e:
            print "Could not complete the transaction because an error occurred:"
            print e
            #raise # Raise the exception that brought you here 





#temporary, for testing:
email = "ncb21992@hotmail.com"
password = "2Rxub#21l8oR#$niEd#L08J9*MK3IiLP"

generator = BogusFormBuilder()

SSHPassword = generator.getRAString(32)

zhb = ZappiehostBuyer(email, password)
#zhb.placeOrder('abc', 'def')

zhb.setSSHPassword()
