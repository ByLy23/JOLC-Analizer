export const getConsola = async ({ estado }) => {
  const requestOps = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ peticion: estado }),
  };
  // const response = await fetch('https://backend-jolc.herokuapp.com/interpretar', requestOps);
  const response = await fetch('http://localhost:5000/optimizar', requestOps).catch('Error'); //CAMBIAR EL OPTIMIZAR POR EL INTERPRETAR
  const data = await response.json().catch('error');
  return data;
};
