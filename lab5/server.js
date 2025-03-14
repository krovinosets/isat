const express = require('express');
const path = require('path');
const app = express();

app.use(express.static(path.join(__dirname, 'public')));

// Запускаем сервер на порту 80
app.listen(80, () => {
    console.log('Сервер запущен на http://localhost:80');
});