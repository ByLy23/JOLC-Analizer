import React, { useState } from 'react';
import '../css/navBar.css';
import { NavLink } from 'react-router-dom';
import { FiHome, FiEdit, FiList, FiXSquare, FiDownload } from 'react-icons/fi';
import { IconContext } from 'react-icons';
import { PopupAn } from './PopupAn';
export const NavBar = () => {
  const [popUp, setpopUp] = useState(false);
  const handlePop = () => {
    setpopUp(true);
  };
  return (
    <nav className="glass">
      <span className="title">JOLC</span>
      <hr />
      <IconContext.Provider value={{ size: '2em', className: 'react-icons' }}>
        <div className="links">
          <NavLink activeClassName="active" className="link-item" to="/inicio">
            <FiHome /> Inicio
          </NavLink>
          <NavLink
            activeClassName="active"
            className="link-item"
            to="/analizador"
          >
            <FiEdit />
            Analizador
          </NavLink>
          <span className="reporte">Reportes</span>
          <NavLink
            activeClassName="active"
            className="link-item"
            to="/simbolos"
          >
            <FiList />
            Tabla de Simbolos
          </NavLink>
          <NavLink activeClassName="active" className="link-item" to="/errores">
            <FiXSquare />
            Tabla de Errores
          </NavLink>
          <NavLink
            activeClassName=""
            className="link-item"
            to="/inicio"
            onClick={handlePop}
          >
            <FiDownload /> Arbol AST
          </NavLink>
        </div>
        {popUp && <PopupAn setpopUp={setpopUp} valor={'Descargado'} />}
      </IconContext.Provider>
    </nav>
  );
};
