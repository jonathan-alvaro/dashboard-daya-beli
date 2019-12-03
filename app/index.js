const express = require('express');
const http = require('http');
const fs = require('fs');
const path = require('path');
const cors = require('cors');

const app = express();
const port = 4000;

const json_path = path.join(__dirname, '../', 'data', 'harga_pangan', 'output', 'data.json');
const json_string = fs.readFileSync(json_path, {'encoding':'utf-8'});

const data = JSON.parse(json_string);

app.use(cors());

app.get('/data/food/:year/:month', (req, res) => {
    res.setHeader('Content-Type', 'application/json');
    res.status(200).write(JSON.stringify(data[req.params.month+'-'+req.params.year]));
    res.end();
})

app.listen(port);
