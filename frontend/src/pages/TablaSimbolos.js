import React from 'react';
import { tableData } from '../components/tableData';
import '../css/tabla.css';
export const TablaSimbolos = () => {
  return (
    <div className="table-container animate__animated animate__fadeInUp">
      <table className="table">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Tipo</th>
            <th>Ambito</th>
            <th className="second">Fila</th>
            <th className="second">Columna</th>
          </tr>
        </thead>
        {tableData.map(({ nombre, tipo, ambito, fila, columna }, index) => {
          return (
            <tbody key={index}>
              <tr>
                <td>{nombre}</td>
                <td>{tipo}</td>
                <td>{ambito}</td>
                <td>{fila}</td>
                <td>{columna}</td>
              </tr>
            </tbody>
          );
        })}
      </table>
    </div>
  );
};
