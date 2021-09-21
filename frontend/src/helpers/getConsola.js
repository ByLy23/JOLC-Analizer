export const getConsola = async ({ estado }) => {
  const requestOps = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ peticion: estado }),
  };
  const response = await fetch('https://backend-jolc.herokuapp.com/interpretar', requestOps);
  const data = await response.json();
  return data;
};
