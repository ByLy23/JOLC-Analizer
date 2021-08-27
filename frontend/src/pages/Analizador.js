import React, { useState } from 'react';
import '../css/analizador.css';
import 'codemirror/theme/cobalt.css';
import 'codemirror/keymap/sublime';
import { PopupAn } from '../components/PopupAn';
import { CodeMirrorComponent } from '../components/CodeMirrorComponent';
import { getConsola } from '../helpers/getConsola';
export const Analizador = () => {
  const [popUp, setpopUp] = useState(false);
  const [state = { outputCode: 'salida' }, setstate] = useState([]);
  const [salida = { outputCode: 'salida' }, setSalida] = useState([]);
  const handleSubmit = () => {
    setSalida({ outputCode: getConsola() });
    console.log(state);
    setpopUp(true);
  };
  const input = (
    <input
      type="submit"
      className="analizar"
      onClick={handleSubmit}
      value="analizar"
    />
  );
  const valor = {
    estado: state.outputCode,
    colocaEstado: setstate,
  };
  const label = React.createElement('h1', { className: 'con-text' }, 'Consola');
  return (
    <div className="analizer-container">
      <CodeMirrorComponent
        input={input}
        codeMirrorValue={valor}
        writable="true"
        clase="editor"
      />
      <CodeMirrorComponent
        input={label}
        codeMirrorOut={salida.outputCode}
        writable="false"
        clase="console"
      />
      {popUp && <PopupAn setpopUp={setpopUp} valor={'Analizado'} />}
    </div>
  );
};
