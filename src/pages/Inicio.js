import React from 'react';
import { FiGithub, FiMail, FiLinkedin } from 'react-icons/fi';
import { IconContext } from 'react-icons';
import '../css/inicio.css';
export const Inicio = () => {
  return (
    <div className="card animate__animated animate__fadeInDown">
      <div className="card-header">
        <p className="nombre">Byron Antonio Orellana Alburez</p>
        <p className="carnet">201700733</p>
      </div>
      <IconContext.Provider value={{ size: '1em', className: 'react-icons' }}>
        <div className="card-contact">
          <ul>
            <li>
              <a
                href="https://github.com/ByLy23?tab=repositories"
                target="_blank"
              >
                <FiGithub />
                https://github.com/ByLy23?tab=repositories
              </a>
            </li>
            <li>
              <a
                href="mailto:3018080310101@ingenieria.usac.edu.gt?subject=Contacto%20de%20Trabajo"
                target="_blank"
              >
                <FiMail />
                3018080310101@ingenieria.usac.edu.gt
              </a>
            </li>
            <li>
              <a
                href="https://www.linkedin.com/in/byronorellana-byly23/"
                target="_blank"
              >
                <FiLinkedin />
                https://www.linkedin.com/in/byronorellana-byly23/
              </a>
            </li>
          </ul>
        </div>
      </IconContext.Provider>
    </div>
  );
};
