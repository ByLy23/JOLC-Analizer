export const ErrData = () => {
  const res = localStorage.getItem('TABLA_ERRORES') === null ? [] : JSON.parse(localStorage.getItem('TABLA_ERRORES'));
  return res;
};
