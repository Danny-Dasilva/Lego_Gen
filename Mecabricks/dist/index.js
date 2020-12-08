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
let partList = [
  '4073',
  '3023',
  '3024',
  '2780',
  '98138',
  '3069b',
  '3004',
  '54200',
  '3710',
  '3005',
]
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
  await page.goto(workshop)

  await page.waitForSelector('div.ui-panel-wrapper:nth-child(4)', {
    visible: true,
  });
  await page.waitForTimeout(1000);
  await page.click('div.ui-panel-wrapper:nth-child(4)')
  await page.waitForSelector('.filter-panel > div:nth-child(1) > div:nth-child(1) > label:nth-child(2) > svg:nth-child(1)', {
    visible: true,
  });
  await page.click('.filter-panel > div:nth-child(1) > div:nth-child(1) > label:nth-child(2) > svg:nth-child(1)')
  await page.click('.filter-panel > div:nth-child(3) > div:nth-child(1) > label:nth-child(2) > svg:nth-child(1)')
    //search in loop
  
  console.log('here')

  await page.evaluate( () => document.getElementById(".ui-search-wrapper > input:nth-child(2)").value = "")
  
  // for (var i = 0; i < partList.length; i++) {
  //   console.log(partList[i])
  //   await page.type('.ui-search-wrapper > input:nth-child(2)', partList[i])
  //   await page.click('.search-button')
    
  //   await page.waitForTimeout(1000);

  //   //for loop for colors here
  //   for (const [key, value] of Object.entries(colors)) {
  //     await page.waitForTimeout(1000);
  //     await page.click('.items > div:nth-child(1)')
  //     await page.click(value) 
    
  //   }

  //   await page.click('.ui-search-wrapper > input:nth-child(2)')

  //   for (let i = 0; i < partList[i].length; i++) {
  //     await page.keyboard.press('Backspace');
  //   }
   
  // } 
  

  
  
    // await page.click('#menu-file')
    // await page.click('#menu-export')
    // await page.select('#export-format > select:nth-child(1)', 'mbx')
    // await page.waitForTimeout(500);
    // await page._client.send('Page.setDownloadBehavior', {behavior: 'allow', downloadPath: './my-downloads'})
    // await page.click('#export-button')

    // await page.waitForTimeout(6000);
 
    // fs.rename('./my-downloads/Untitled\ Model.zmbx', `./my-downloads/${key}.zmbx`, () => { 
    //   console.log("\nFile Renamed!\n"); 

    // }); 

  browser.close()
  console.log(page.url());
//   window.destroy();
};

main();
    
  