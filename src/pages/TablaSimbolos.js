import React from 'react';
import { tableData } from '../components/tableData';
import '../css/tabla.css';
export const TablaSimbolos = () => {
  return (
    <div className="table-container animate__animated animate__fadeInUp">
      <table className="table">
        <tr>
          <th>Header1</th>
          <th>Header2</th>
          <th>Header3</th>
          <th>Header4</th>
        </tr>
        {tableData.map(({ header1, header2, header3, header4 }) => {
          return (
            <tr>
              <td>{header1}</td>
              <td>{header2}</td>
              <td>{header3}</td>
              <td>{header4}</td>
            </tr>
          );
        })}
      </table>
    </div>
  );
};
