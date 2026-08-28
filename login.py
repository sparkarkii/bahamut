from playwright.sync_api import Playwright, sync_playwright, expect
import time
import datetime
import os
from utils import emailfunc




id = os.environ['BAHAMUT_ID']
pw = os.environ['BAHAMUT_PW']
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:152.0) Gecko/20100101 Firefox/152.0'




def run(playwright) -> int | Exception:
    try:
        browser = playwright.chromium.launch(headless=True) 
        context = browser.new_context(user_agent=useragent)
        page = context.new_page()
        page.goto("https://www.gamer.com.tw/")
        expect(page.get_by_role("button", name="Close")).to_be_visible()
        page.get_by_role("button", name="Close").click()
        page.get_by_role("link", name="登入").click()
        page.locator("#dialogify_1 iframe").content_frame.get_by_role("textbox", name="帳號或手機").click()
        page.locator("#dialogify_1 iframe").content_frame.get_by_role("textbox", name="帳號或手機").fill(id)
        page.locator("#dialogify_1 iframe").content_frame.get_by_role("textbox", name="密碼").click()
        page.locator("#dialogify_1 iframe").content_frame.get_by_role("textbox", name="密碼").fill(pw)
        time.sleep(3)
        page.locator("#dialogify_1 iframe").content_frame.get_by_role("textbox", name="密碼").press("Enter")
        time.sleep(3)

        if page.locator('.singin-total-days').is_hidden():
            page.locator('.main-nav__dropdown').click()
            page.get_by_role("link", name="每日簽到").click()

        signin_days = int(page.locator('.singin-total-days').inner_text())
        return 'successful', signin_days

    except Exception as e:
        return 'failed', e


def login(report=True, report_success=False) -> None:
    with sync_playwright() as playwright:
        match run(playwright):
            case 'successful', signin_days:
                if report and report_success:
                    subject = f'{datetime.date.today()}: bahamut'
                    emailfunc.send_email(subject, content=str(signin_days)

            case 'failed', e:
                if report:
                    subject = f'{datetime.date.today()}: bahamut (failed)'
                    emailfunc.send_email(subject, content=str(e)

            case _:
                if report:
                    subject = f'{datetime.date.today()}: bahamut (unexpected match/case)'
                    emailfunc.send_email(subject)

    


if __name__ == '__main__':
    login()
