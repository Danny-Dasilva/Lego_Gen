const {BrowserWindow, app} = require("electron");
const pie = require("puppeteer-in-electron")
const puppeteer = require("puppeteer-core");
const fs = require('fs');


var colors = {
    'Medium Stone Grey': '#materials-overview > div:nth-child(1) > div:nth-child(2)',
    'White': '#materials-overview > div:nth-child(1) > div:nth-child(1)',
    'Dark Stone Grey': '#materials-overview > div:nth-child(1) > div:nth-child(3)',
    'Black': '#materials-overview > div:nth-child(1) > div:nth-child(4)',
    'Brick Yellow': '#materials-overview > div:nth-child(1) > div:nth-child(11)',
    'Reddish Brown': '#materials-overview > div:nth-child(1) > div:nth-child(8)',
    'Bright Red': '#materials-overview > div:nth-child(1) > div:nth-child(6)',
    'Sand Yellow': '#materials-overview > div:nth-child(1) > div:nth-child(10)',
    'Bright Yellow': '#materials-overview > div:nth-child(1) > div:nth-child(18)',
    'Bright Blue': '#materials-overview > div:nth-child(1) > div:nth-child(30)',
};

const url = 'https://www.mecabricks.com/en/login'
const workshop = 'https://www.mecabricks.com/en/workshop'
const part = '3004'


const main = async () => {
  await pie.initialize(app);
  const browser = await pie.connect(app, puppeteer);
  


  

  const window = new BrowserWindow({ width: 1200, height: 800 })
  await window.loadURL(url);
 
  const page = await pie.getPage(browser, window);
  
  //login
  
//   await page.type('#field-identifier', 'heliothryxaurita@gmail.com')
//   await page.type('#field-password', '123yhs321')
//   await page.click('#remember-me')
//   await page.click('#button')
 
  await page.goto('http://niftyindices.com/resources/holiday-calendar');
  await page._client.send('Page.setDownloadBehavior', {behavior: 'allow', 
  downloadPath: './downloads'})
  await page.click('#exportholidaycalender');
  await page.waitFor(5000);
  
  console.log(page.url());
//   window.destroy();
};

main();