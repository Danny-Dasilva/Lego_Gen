// Modules to control application life and create native browser window
import { writeFile, readFileSync } from 'fs';
import { app, BrowserWindow } from 'electron';
import { Electrolizer } from '@ugenu.io/electrolizer'


let counter = 0;

const arr:Array<string> = []

app.on('ready', () => {
  const bus = new BrowserWindow({ width: 800, height: 600 })
  let electrolizer = new Electrolizer(bus);


  let urls = read('./data/input.txt')
  // getIps('https://www.blackhatworld.com/seo/gsa-proxies-proxygo.830325/page-76', electrolizer)

  const getIps = async (url: string):Promise<string[]> => {
    counter++;
  
    let response: string[] = await electrolizer
      .goto(url)
      .wait(1000)
      .evaluate(() => document.documentElement.outerHTML)
      .then(filterIP)
      .then(write)
    return response;
  }
  const results = urls.reduce(async (acc, url: string) => {
    const dataArray = await acc;
    let data = await getIps(url);
    dataArray.push(...data);
    return dataArray;
  }, Promise.resolve(arr));
  results.then(data => {
    console.log(data, "\n finished");
    process.exit(0)
  });

});

const filterIP = (input: string) => {
    // var patt = /\d{1,3}(?:.\d{1,3}){3}(?::\d{1,5})?/igm;
    var patt = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?):(6553[0-5]|655[0-2][0-9]|65[0-4][0-9][0-9]|6[0-4][0-9][0-9][0-9][0-9]|[1-5](\d){4}|[1-9](\d){0,3})$/igm;
    var result = input.match(patt);
    return result
}

const read = (path: string) => {
  var array = readFileSync( path, 'utf8').toString().split('\n');
  return array
};


const write = (input: (RegExpMatchArray | null)): string[] => {
  const path = './data/output.txt'
  const coercedinput = input as RegExpMatchArray

  const current = read(path)
  let unique = [...new Set(coercedinput.concat(current))]; 
  writeFile(path, unique.join('\n'), function (err) {
    if (err) return console.log(err);
    console.log('arr > output.txt');
  })
  return unique
};