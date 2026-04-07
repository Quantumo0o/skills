const fs = require('fs');
let r = fs.readFileSync('C:/Users/Administrator/Desktop/singularity/package.json', 'utf8');
r = r.replace('"version": "2.4.2"', '"version": "2.5.0"');
fs.writeFileSync('C:/Users/Administrator/Desktop/singularity/package.json', r);
console.log('done');
