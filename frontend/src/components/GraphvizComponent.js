import Graphviz from 'graphviz-react';
import React from 'react';

export const GraphvizComponent = () => {
  const options = { fit: false, zoom: true, width: '100%', height: '100vh' };
  const dot = JSON.parse(localStorage.getItem('ARBOL_AST'));
  return <Graphviz dot={dot} options={options} />;
};
