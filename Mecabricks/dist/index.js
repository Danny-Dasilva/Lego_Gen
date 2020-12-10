const {BrowserWindow, app} = require("electron");
const pie = require("puppeteer-in-electron")
const puppeteer = require("puppeteer-core");
const fs = require('fs');


var colors = {
    'Medium_Stone_Grey': '#materials-overview > div:nth-child(1) > div:nth-child(2)',
    'White': '#materials-overview > div:nth-child(1) > div:nth-child(1)',
    'Dark_Stone_Grey': '#materials-overview > div:nth-child(1) > div:nth-child(3)',
    'Black': '#materials-overview > div:nth-child(1) > div:nth-child(4)',
    'Brick_Yellow': '#materials-overview > div:nth-child(1) > div:nth-child(11)',
    'Reddish_Brown': '#materials-overview > div:nth-child(1) > div:nth-child(8)',
    'Brigh_Red': '#materials-overview > div:nth-child(1) > div:nth-child(6)',
    'Sand_Yellow': '#materials-overview > div:nth-child(1) > div:nth-child(10)',
    'Bright_Yellow': '#materials-overview > div:nth-child(1) > div:nth-child(18)',
    'Bright_Blue': '#materials-overview > div:nth-child(1) > div:nth-child(30)',
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

let names = [] 

const main = async () => {
  await pie.initialize(app);
  const browser = await pie.connect(app, puppeteer);
  


  

  const window = new BrowserWindow({ width: 1200, height: 800 })
  await window.loadURL(url);
 
  const page = await pie.getPage(browser, window);
  
  //login
  
//   await page.type('#field-identifier', '')
//   await page.type('#field-password', '')
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
  await page.waitForTimeout(1000);
 
 

  for (var i = 0; i < partList.length; i++) {
    let partname = partList[i]
    await page.type('.ui-search-wrapper > input:nth-child(2)', partList[i])
    await page.click('.search-button')
    
    await page.waitForTimeout(1000);

    //for loop for colors here
    for (const [color_name, color] of Object.entries(colors)) {
      await page.waitForTimeout(1000);
      // click on part

      await page.evaluate((partname) => {
        let elements = document.getElementsByClassName("reference")
        console.log(partname, 'working')
        for (let element of elements) {
          let name = element.innerHTML
          if (name === partname) {
            element.click();
          }
        }   
      }, partname)
      await page.click(color) 
      names.push(`${partname}-${color_name}`);
    
    }

    await page.click('.ui-search-wrapper > input:nth-child(2)')

    for (let i = 0; i < partList[i].length; i++) {
      await page.keyboard.press('Backspace');
    }
   
  } 
  

  console.log(names)
  const fs = require('fs');
  fs.writeFile('./my-downloads/filenames.json', JSON.stringify(names), err => err ? console.log(err): null);
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
    
  