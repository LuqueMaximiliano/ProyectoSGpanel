const fetch = require('node-fetch');
const db = require('./db'); // Asegúrate de tener el archivo db.js con la configuración de la base de datos

async function fetchData() {
  try {
    const response = await fetch('https://api.slidegroup.superpanel.app/profiles/list?expand=operator,pause_operator,dia_summary,mes_summary&agencyId=8');
    const data = await response.json();
    // Guardar los datos en la base de datos
    // Por ejemplo, si los datos son un array de perfiles, puedes iterar sobre ellos y ejecutar una inserción en la base de datos para cada perfil
    for (const profile of data) {
      await db.query('INSERT INTO tabla (nombre, edad) VALUES (?, ?)', [profile.name, profile.age]);
    }
    console.log('Datos guardados en la base de datos correctamente.');
  } catch (error) {
    console.error('Error al obtener datos o guardar en la base de datos:', error);
  }
}

fetchData();
