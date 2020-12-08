
const { app, BrowserWindow } = require("electron");
const { Electrolizer } = require("@ugenu.io/electrolizer");

var colors = {
    'Medium Stone Grey': '#materials-overview > div:nth-child(1) > div:nth-child(2)',
    'White': '#materials-overview > div:nth-child(1) > div:nth-child(1)',
    'Dark Stone Grey': '#materials-overview > div:nth-child(1) > div:nth-child(3)',
    'Black': '#materials-overview > div:nth-child(1) > div:nth-child(4)',
    'Brick Yellow': 'div.item:nth-child(11)',
    'Reddish Brown': 'div.item:nth-child(8)',
    'Bright Red': '#materials-overview > div:nth-child(1) > div:nth-child(6)',
    'Sand Yellow': 'div.item:nth-child(10)',
    'Bright Yellow': 'div.item:nth-child(18)',
    'Bright Blue': 'div.item:nth-child(30)',
};

const url = 'https://www.mecabricks.com/en/login'
const workshop = 'https://www.mecabricks.com/en/workshop'
const part = '3004'
app.on('ready', () => {
    const bus = new BrowserWindow({ width: 1200, height: 800 })
    let electrolizer = new Electrolizer(bus);

    let response = electrolizer
    // .goto(url)
    // .type('#field-identifier', 'heliothryxaurita@gmail.com')
    // .type('#field-password', '123yhs321')
    // .click('#remember-me')
    // .click('#button')
    .goto(workshop)
    .wait('.ui-select-arrow')
    .click('div.ui-panel-wrapper:nth-child(4)')
    .wait('.filter-panel > div:nth-child(1) > div:nth-child(1) > label:nth-child(2) > svg:nth-child(1)')
    .click('.filter-panel > div:nth-child(1) > div:nth-child(1) > label:nth-child(2) > svg:nth-child(1)')
    .click('.filter-panel > div:nth-child(3) > div:nth-child(1) > label:nth-child(2) > svg:nth-child(1)')
    //search in loop
    .type('.ui-search-wrapper > input:nth-child(2)', '3004')
    .click('.search-button')
    .wait('.items > div:nth-child(1)')
    .click('.items > div:nth-child(1)')
    .click('#materials-overview > div:nth-child(1) > div:nth-child(4)')
    .wait(500000)
    .evaluate(() => document.querySelector('#r1-0 a.result__a').href)

    
    console.log(response);
});