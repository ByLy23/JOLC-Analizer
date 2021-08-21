import React from 'react';
import { tableData } from '../components/tableData';
import '../css/tabla.css';

export const TablaErrores = () => {
  let contador = 0;
  return (
    <div className="table-container animate__animated animate__fadeInUp">
      <table className="table">
        <thead>
          <tr>
            <th className="second">No.</th>
            <th className="first">Descripcion</th>
            <th className="second">Linea</th>
            <th className="second">Columna</th>
            <th>fecha</th>
          </tr>
        </thead>
        {tableData.map(
          ({ columnaError, lineaError, descErrores, fechaError }, index) => {
            return (
              <tbody key={index}>
                <tr>
                  <td>{contador++}</td>
                  <td>{descErrores}</td>
                  <td>{lineaError}</td>
                  <td>{columnaError}</td>
                  <td>{fechaError}</td>
                </tr>
              </tbody>
            );
          }
        )}
      </table>
    </div>
  );
};
