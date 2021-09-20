import React from 'react';
import { ErrData } from '../components/ErrData';
import '../css/tabla.css';

export const TablaErrores = () => {
  return (
    <div className="table-container animate__animated animate__fadeInUp">
      <table className="table">
        <thead>
          <tr>
            <th className="second">No.</th>
            <th className="first">Descripcion</th>
            <th className="second">Linea</th>
            <th className="second">Columna</th>
            <th>Hora</th>
          </tr>
        </thead>
        {ErrData.map(({ No, Tipo, Descripcion, Linea, Columna }, index) => {
          return (
            <tbody key={index}>
              <tr>
                <td>{No}</td>
                <td>{Descripcion}</td>
                <td>{Linea}</td>
                <td>{Columna}</td>
                <td>{Tipo}</td>
              </tr>
            </tbody>
          );
        })}
      </table>
    </div>
  );
};
