from random import randint
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from BogusFormBuilder import BogusFormBuilder

from src.agent.VPSBuyer import VPSBuyer
from src.agent.OffshoredediBuyer import OffshoredediBuyer


#temporary, for testing:
#email = "ncb21992@hotmail.com"
#password = "2Rxub#21l8oR#$niEd#L08J9*MK3IiLP"

#generator = BogusFormBuilder()

#SSHPassword = generator.getRAString(32)

#zhb = ZappiehostBuyer('xKlupfS@XEF.org', 'qnrmHRNxCZWLskFtiDSUGkSyUoHJBSpj')
#zhb.placeOrder('abc', 'def')

#zhb.setSSHPassword()



# The code here will actually buy a VPS from Zappiehost
buyer = OffshoredediBuyer('MnZaBFeMy@QRYz.org', 'yuezNYsQFSEypMYSJfBDEvQougtahCkx')
#buyer = OffshoredediBuyer()
#result = buyer.placeOrder()
#result = buyer.placeOrder()
result = buyer.setSSHPassword()


if result == True:
    print("VPS BOUGHT! Details:")
    print("Zappiehost email: " + buyer.getEmail())
    print("Zappiehost password: " + buyer.getPassword())
    print("SSH IP: " + buyer.getIP())
    print("SSH Username: " + buyer.getSSHUsername())
    print("SSH Password: " + buyer.getSSHPassword())
else:
    print("Failed to buy VPS from OffshoreDedi...")
