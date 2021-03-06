import pytest
from pageObjects.LoginPage import LoginPage
from utilities.readProperties import ReadConfig
from utilities.customLogger import LogGen
from core.ui.ui_helper import UIHelper
from pageObjects.CreateCardPage import CreateCard
from pageObjects.BoardPage import BoardPage
import os


class Test_Login:
    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()
    logger=LogGen.loggen()
    session_name = ReadConfig.getvaluesfrom_json('create-board_data', 'session_name')
    owner= ReadConfig.getvaluesfrom_json('create-board_data', 'owner')
    success_message = ReadConfig.getvaluesfrom_json('create-board_data', 'success_message')
    board_url= ReadConfig.getvaluesfrom_json('page_urls', 'board_page')
    card_type_went_well = ReadConfig.getvaluesfrom_json('card_type', 'green')
    card_modal_header = ReadConfig.getvaluesfrom_json('header', 'sprint_board_modal')
    well_add_card_title = ReadConfig.getvaluesfrom_json('went_well_data', 'title')
    well_add_card_description = ReadConfig.getvaluesfrom_json('went_well_data', 'description')
    well_card_activity = ReadConfig.getvaluesfrom_json('card_activity','went_well')
    well_like_count = ReadConfig.getvaluesfrom_json('card_activity','like_count')


    @pytest.mark.smoke
    @pytest.mark.ui
    def test_create_card_went_well(self,setup):
        try:
            self.logger.info("****Started Went well Test****")
            self.driver = setup
            self.driver.maximize_window()
            self.driver.get(self.baseURL)
            self.lp=LoginPage(self.driver)
            self.bp = BoardPage(self.driver)
            assert self.lp.login(self.username,self.password)
            self.bp.go_to_create_board()
            bln_final_result = self.bp.create_board(self.session_name,self.owner,self.success_message)
            if bln_final_result:
                self.ui_helper = UIHelper(self.driver)
                self.cp = CreateCard(self.driver)
                self.cp.wait_board_page_to_load()
                pstr_url = self.driver.current_url
                assert self.ui_helper.verify_url(self.board_url, pstr_url)
                self.cp.clickCard(self.card_type_went_well)
                assert self.cp.verify_modal_header(self.card_modal_header)
                self.cp.create_card(self.well_add_card_title,self.well_add_card_description)
                assert self.cp.verify_card(self.card_type_went_well,self.well_add_card_title, self.well_add_card_description)
                self.cp.click_activity(self.card_type_went_well,self.well_card_activity)
                bln_like= self.cp.verify_activity(self.card_type_went_well,self.well_card_activity,pstr_like_count =self.well_like_count)
                if bln_like:
                    self.logger.info("***Test 002 passed****")
                    self.driver.close()
                    assert True
                else:
                    self.logger.error("****Test 002 failed ****")
                    self.driver.close()
                    assert False
        except Exception as exception_msg:
            self.logger.info(exception_msg)
            self.driver.save_screenshot("." + os.sep + "Screenshots" + os.sep + "test_createCard_went_well_exception.png")
            self.driver.close()
            assert False









