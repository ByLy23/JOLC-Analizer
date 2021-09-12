export const getConsola = async ({ estado }) => {
  console.log(estado);
  const requestOps = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ peticion: estado }),
  };
  const response = await fetch('http://127.0.0.1:8000/interpretar', requestOps);
  const data = await response.json();

  return data;
};
