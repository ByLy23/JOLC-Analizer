export const MirillaData = () => {
  const res = localStorage.getItem('TABLA_MIRILLA') === null ? [] : JSON.parse(localStorage.getItem('TABLA_MIRILLA'));
  return res;
};
