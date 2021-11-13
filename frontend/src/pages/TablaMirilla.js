import React from 'react';
import { MirillaData } from '../components/MirillaData';
import '../css/tabla.css';
export const TablaMirilla = () => {
  const mirilla = MirillaData();
  return (
    <div className="table-container animate__animated animate__fadeInUp">
      <table className="table">
        <thead>
          <tr>
            <th>Descripcion</th>
            <th>Regla</th>
            <th>Original</th>
            <th>Nuevo</th>
            <th className="second">Linea</th>
          </tr>
        </thead>
        {mirilla.map(({ Tipo, Regla, Original, Optimizado, Linea }, index) => {
          return (
            <tbody key={index}>
              <tr>
                <td>{Tipo}</td>
                <td>{Regla}</td>
                <td>{Original}</td>
                <td>{Optimizado}</td>
                <td>{Linea}</td>
              </tr>
            </tbody>
          );
        })}
      </table>
    </div>
  );
};
