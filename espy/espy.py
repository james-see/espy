# -*- coding: utf-8 -*-

"""bootstrap.bootstrap: provides entry point main()."""

__version__ = "0.0.1"
# Espy 
#
# Espy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Espy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with espy. If not, see <http://www.gnu.org/licenses/>.
import os  
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options 

import sys
cur_version = sys.version_info.major
from time import sleep
import argparse, requests
from random import random, randint
import random
from clint.textui import progress # for the dots!
from bs4 import BeautifulSoup, SoupStrainer # parse the html!
try: from urllib.parse import urlparse # get domain names!
except:
    from urlparse import urlparse
    cur_version = 2.7
    #sys.path.append(PYTHONPATH)
from termcolor import *

if int(cur_version) < 3:
    try:
        # from .modules import stuff
        # from .modules import core
        # from .modules.pdf_maker import *
        from .modules.useragents import *
    except:
        # from modules import stuff
        # from modules import core
        # from modules.pdf_maker import *
        from modules.useragents import *
        #exit('your python version is too old, please install python 3+ to get espy to work')
else:
    try:
        # from modules import stuff
        # from modules import core
        # from modules.pdf_maker import *
        from modules.useragents import *
    except:
        # from espy.modules import stuff
        # from espy.modules import core
        # from espy.modules.pdf_maker import *
        from espy.modules.useragents import *


welcomer = '\n++++++++++++++++++++++++++++\n+++ ESPY +++ WELCOME +++++++\n+++ ESPN SCORE GRABBER +++\n++++++++++++++++++++++++++++\n'
usingtor = False

def test_selenium():
    """Selenium tester."""
    chrome_options = Options()  
    chrome_options.add_argument("--headless")  
    chrome_options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'

    driver = webdriver.Chrome(executable_path=os.path.abspath("/usr/local/bin/chromedriver"), chrome_options=chrome_options)  
    driver.get("http://www.duo.com")

    magnifying_glass = driver.find_element_by_id("js-open-icon")  
    if magnifying_glass.is_displayed():  
        magnifying_glass.click()  
    else:  
        menu_button = driver.find_element_by_css_selector(".menu-trigger.local")  
        menu_button.click()

    search_field = driver.find_element_by_id("site-search")  
    search_field.clear()  
    search_field.send_keys("Olabode")  
    search_field.send_keys(Keys.RETURN)  
    assert "Looking Back at Android Security in 2016" in driver.page_source 
    print(driver.page_source)  
    driver.close() 

def get_espn(selected_sport):
    """Selenium scraper."""
    chrome_options = Options()  
    chrome_options.add_argument("--headless")  
    chrome_options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'

    driver = webdriver.Chrome(executable_path=os.path.abspath("/usr/local/bin/chromedriver"), chrome_options=chrome_options)  
    driver.get(f"http://www.espn.com/{selected_sport}/scoreboard")

    soup = BeautifulSoup(driver.page_source, features="lxml")
    cprint("This week's lineup\n", "blue")
    teamsthisweek = soup.find_all('span', attrs={"class":"sb-team-short"}) 
    for (index, thing) in enumerate(teamsthisweek[:-1]):
        current, next_ = thing, teamsthisweek[index + 1]
        print(f'{current.string} vs. {next_.string}')
    driver.close() 


def main():
    # welcome to the danger zone
    #test_selenium()
    #exit()
    parser = argparse.ArgumentParser(
        # random comment here for no reason ;)
        formatter_class=argparse.RawTextHelpFormatter,
        prog='espy',
        description='++++++++++++++++++++++++++++\n+++ espy +++++++++++++++++++\n+++ nfl scores +++\n++++++++++++++++++++++++++++',
        epilog = '''EXAMPLE: \n get scores \n espy -s nfl \n ''')

    parser.add_argument('-s','--sport', help='sport, like nfl', dest='sport', required=True)

    parser.add_argument('-p', '--proxy', help='proxy in the form of 127.0.0.1:8118',
                        nargs=1, dest='setproxy', required=False)

    parser.add_argument('-w', '--wait', help='max random wait time in seconds, \n5 second default (randomly wait 1-5 seconds)',
                        dest='setwait', nargs='?',const=3,type=int,default=3)
    parser.add_argument('-u', '--user-agent', help='override random user-agent\n(by default randomly selects between \n+8500 different user agent strings',
                        dest='useragent', nargs='?',const='u',default='u')
    parser.add_argument('-v','--verbose-useragent',dest='vu',action='store_true')
    parser.add_argument('--version', action='version',
                    version='%(prog)s {version}'.format(version='Version: '+__version__))
    parser.set_defaults(reporting=True,vu=False)
    args = parser.parse_args()
    cprint(welcomer,'red')
    # args strings
    setproxy = args.setproxy
    # note, the correct way to check if variable is NoneType
    if setproxy != '' and setproxy is not None:
        proxyoverride = True
        if '9050' in setproxy[0] or '9150' or 'tor' in setproxy[0]:
            usingtor = True
        else:
            usingtor = False
    else:
        proxyoverride = False
    setwait = args.setwait
    reporting = args.reporting
    useragent = args.useragent
    vu = args.vu
    if useragent == 'u':
        overrideuseragent = False
        useragent = random.choice(useragents) # if user agent override not set, select random from list
    if vu:
        cprint('\nUseragent set as %s\n' % (useragent,),'blue')
    headers = {'User-Agent': useragent}

    # print useragent to make sure it is working - jc
    # print(f'Useragent: {useragent}')

    # get nfl scores example url: http://www.espn.com/nfl/scoreboard/_/year/2018/seasontype/2/week/3
    get_espn(args.sport)

if __name__ == '__main__':
    main()

exit()